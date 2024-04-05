from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from api.transaction_service import api_transaction_service
from api.account_service import api_account_service
from api.auth_service import api_auth_service
from fastapi.security import OAuth2PasswordBearer
import json

oauth2_scheme_token_refresh = OAuth2PasswordBearer(tokenUrl="/refresh_token")

class CredenciaisConta(BaseModel):
    """
    Modelo de credenciais de conta para autenticação de usuários.
    """
    id_conta: str
    agencia_id: str
    senha: str

class InfoConta_Resp(BaseModel):
    """
    Modelo de resposta para fornecer informações sobre a conta bancária do cliente.
    """

    cod_resp: int
    nome_cliente: str
    id_conta: str
    agencia_id: str
    tipo_conta: str
    status_conta: str
    data_criacao: str
    data_fechamento: Optional[str]

class Depositar_Req(BaseModel):
    """ 
    Define o esquema de entrada de dados para o endpoint '/depositar', que é responsável
    por processar solicitações de depósito em uma conta bancária.
    """
    valor: float

class Depositar_Resp(BaseModel):
    """ 
    Define o esquema dos dados de resposta enviados ao cliente após uma solicitação de 
    depósito através do endpoint '/depositar'. 
    """
    cod_resp: int
    text_resp: str
    saldo_atual: Optional[float]

class Sacar_Req(BaseModel):
    """ 
    Define o esquema de entrada esperado pelo endpoint '/sacar'.
    """
    valor: float

class Sacar_Resp(BaseModel):
    """ 
    Modelo utilizado para estruturar a resposta enviada ao usuário da API após uma solicitação
    de saque. O modelo inclui informações sobre o resultado da operação, saldo atual após saque,
    e número de saques diários restantes.
    """
    cod_resp: int
    text_resp: str
    saques_diarios: Optional[int]
    saldo_atual: Optional[float]

class Transferir_Req(BaseModel):
    """ 
    Define o esquema de entrada de dados necessário para realização de uma transferência
    bancária entre duas contas através do endpoint 'transferir'.
    """
    valor: float
    conta_destino: str
    agencia_destino: str

class Transferir_Resp(BaseModel):
    """ 
    Modelo utilizado para estruturar a resposta enviada ao usuário da API após uma solicitação
    de transferência bancária.
    """
    cod_resp: int
    text_resp: str
    saldo_atual: Optional[float]

class ConsultarSaldo_Resp(BaseModel):
    """ 
    Modelo utilizado para estruturar a resposta após uma solicitação para consultar o saldo
    de uma conta bancária. Inclui detalhes da conta, além de informações sobre o saldo.
    """
    cod_resp: int
    nome: str
    id_conta: str
    agencia_id: str
    saldo: float
    saldo_disponivel: float

class Extrato_Req(BaseModel):
    """ 
    Define o esquema de dados de entrada para a operação de consulta de extrato bancário
    através do endpoint '/consultar_extrato'.
    """
    data_consulta: str

class Consultar_Info_Cartao_Resp(BaseModel):
    """ 
    Modelo utilizado para estrutura a resposta enviada após solicitação para consultar informações
    de cartão de crédito/débito associado à conta do usuário.
    """
    cod_resp: int
    num_cartao: Optional[str]
    cod_cvv: Optional[str]
    val_cartao: Optional[str]

class Extrato_Resp_Model(BaseModel):
    """ 
    Utilizado para estruturar a resposta enviado após uma solicitação para consultar o extrato
    bancário de uma conta bancária.
    """
    cod_resp: int
    id_conta: str
    agencia_id: str
    data_consulta: str
    nome: str
    saldo_atual: float
    transacoes: Optional[List] = None

class ConsultaSaquesDiarios_Resp(BaseModel):
    """ 
    Define a estrutura de dados de resposta fornecidos após solicitação de consulta do número de saques
    no dia em que a consulta foi efetuada. Esse modelo fornece o esquema de resposta do endpoint '/consultar_saques_diarios'.
    """
    cod_resp: int
    saques_hoje: Optional[int] = None

app = FastAPI()

"--------------------------------------------- ENDPOINTS DA API ---------------------------------------------------"
@app.get('/status')
def check_status():
    """
    Responsável por checar se a API está online.
    """
    return JSONResponse(content = {'status': 'online'}, status_code = 200)

@app.post("/token")
async def login_for_access_token(body: CredenciaisConta):
    """ 
    Autentica o usuário com base nas credenciais fornecidas no corpo da solicitação POST e gera um token de acesso JWT e um refresh token JWT.

    Este endpoint recebe as credenciais do usuário ('id_conta', 'agência_id' e 'senha') e realiza a autenticação a partir
    do banco de dados do sistema e, se bem-sucedido, e gera um token JWT para o usuário. Este token é utilizado para autorizar 
    o usuário a realizar operações que exigem autenticação.

    Parâmetros: 
        body (CredenciaisConta): Este objeto contém as credenciais do usuário. Os dados contido no objeto segue o esquema 
            do modelo Pydantic 'CredenciaisConta', sendo validados automaticamente pelo FastAPI.
            O modelo 'CredenciaisConta' espera receber os dados JSON com a seguinte estrutura: 
            {
            'id_conta' (str): número da conta do usuário,
            'agencia_id' (str): número da agência,
            'senha' (str): senha da conta bancária
            }
    Retorna:
        dict: Um dicionário contendo o token de acesso gerado, o tipo de token ('bearer') e um token refresh.
    
    Levanta:
        HTTPException: Exceção gerada quando há falha na autenticação do usuário, que pode ser ocasionado por credenciais
        incorretas ou problemas na conexão com o sistema de banco de dados.
    
    Exemplo de solicitação POST:
        POST /token
        body: {
            'id_conta': '123456789',
            'agencia_id': '12345',
            'senha': 'senha123'
        }
    Exemplo de resposta bem-sucedida:
        {
        'access_token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        'token_type': 'bearer',
        'refresh_token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ10..."
        }
    Notas:
        - Os tokens gerados incluem, como parte de sua carga útil, o id da conta, o id da agência e a senha da conta. Essas informações
        estão contidas na chave 'sub' dos tokens.
        - Os tokens tem um tempo de validade, após o qual o token expira e perde validade para autenticação.
    """
    create_token = await api_auth_service.create_access_token(body.id_conta, body.agencia_id, body.senha)
    create_token = json.loads(create_token)

    if create_token['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor.')
    
    if create_token['status_code'] == 400:
        raise HTTPException(status_code = 400, detail = 'Credenciais de conta incorretas!')

    access_token = create_token['token']
    refresh_token = create_token['token_refresh']
    
    return JSONResponse(content = {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}, status_code = 200)

@app.post('/refresh_token', status_code = 200)
async def refresh_token(refresh_token: str = Depends(oauth2_scheme_token_refresh)):
    """ 
    Este endpoint permite renovar o token de acesso de um usuário quando o atual atual expira. É utilizado um token de refresh
    para obter um novo token de acesso, garantindo que o usuário continue autenticado sem precisar inserir suas credenciais novamente.
    """
    new_token = await api_auth_service.refresh_access_token(refresh_token)
    new_token = json.loads(new_token)

    if new_token['status_code'] == 401:
        raise HTTPException(status_code = new_token['status_code'], detail = new_token['detail']) #Falha na autenticação
    
    if new_token['status_code'] == 500:
        raise HTTPException(status_code = new_token['status_code'], detail = new_token['detail']) #Erro interno do servidor
    
    access_token = new_token['token']
    token_refresh = new_token['token_refresh']

    return JSONResponse(content = {'access_token': access_token, 
                                   'token_type': 'bearer', 
                                   'refresh_token': token_refresh}, 
                                   status_code = 200)

@app.get('/consultar_conta', response_model = InfoConta_Resp, status_code = 200)
async def consultar_info_conta(credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Consulta informações relevantes da conta bancária do usuário.

    Este endpoint é protegido e requer que o usuário esteja autenticado. A função extrai as credenciais do usuário
    a partir do token JWT fornecido no cabeçalho (headers) da solicitação e utiliza as informações das
    credenciais para consultar os dados da conta no banco de dados.
    
    Exemplo de uso:
        GET /consultar_conta
        Headers: {"Authorization": "Bearer <token_jwt>"}
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')
    
    try:
        consulta = await api_account_service.consultar_info_conta_db(credenciais['id_conta'], credenciais['agencia_id'])
        consulta = json.loads(consulta)

        if consulta['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_account_service.consultar_info_conta_db'")
        
        elif consulta['status_code'] == 200:
            return InfoConta_Resp(cod_resp = 0, nome_cliente = consulta['nome'], id_conta = credenciais['id_conta'], agencia_id = credenciais['agencia_id'], tipo_conta = consulta['tipo_conta'], status_conta = consulta['status_conta'], data_criacao = consulta['data_criacao'], data_fechamento = consulta['data_fechamento'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.put('/depositar', response_model = Depositar_Resp)
async def depositar(body: Depositar_Req, credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Realiza uma operação de depósito na conta do usuário.

    Esta endpoint permite ao usuário depositar um valor especificado A autenticação é feita através de token JWT fornecido no cabeçalho
    da solicitação (headers). O valor a ser depositado é especificado no corpo da solicitação (body).
    
    Exemplo de uso:
        PUT /depositar
        Headers: {'Authorization': 'bearer <token_jwt>'}
        Body: {'valor': 100.00}
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        deposito = await api_transaction_service.depositar_bd(body.valor, id_conta = credenciais['id_conta'], agencia_id = credenciais['agencia_id'])
        deposito = json.loads(deposito)

        if deposito['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_transaction_service.depositar_bd'")
        
        return Depositar_Resp(cod_resp = deposito['cod_resp'], text_resp = deposito['text_resp'], saldo_atual = deposito['saldo'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.put('/sacar', response_model = Sacar_Resp)
async def sacar(body: Sacar_Req, credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Realiza um saque da conta do usuário.

    Este endpoint permite ao usuário realizar um saque. A função recebe o valor a ser sacado e as credenciais do
    usuário, verifica se o saque poderá ser realizado (observando critérios de saldo disponível, limite de saques diários
    e limite de valor que pode ser sacado por dia) e atualiza o saldo da conta no banco de dados quando o saque é 
    realizado com sucesso.
    
    Exemplo de uso:
        PUT /sacar
        Headers: {'Authorization': 'Bearer <token_jwt>'}
        Body: {'valor': 50.00}
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        saque = await api_transaction_service.sacar_bd(body.valor, credenciais['id_conta'], credenciais['agencia_id'])
        saque = json.loads(saque)

        if saque['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_transaction_service.sacar_bd'")
        
        return Sacar_Resp(cod_resp = saque['cod_resp'], text_resp = saque['text_resp'], saques_diarios = saque['saques_diarios'], saldo_atual = saque['saldo_atual'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.put('/transferir', response_model = Transferir_Resp)
async def transferir(body: Transferir_Req, credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Realiza uma operação de transferência de valor entre a conta do usuário e uma conta destino.

    Este endpoint permite ao usuário transferir um valor especificado para uma outra conta, identificada por seu id de conta e id de agência.
    A autenticação é feita através de token JWT fornecido no cabeçalho da solicitação, e a operação é realizada apenas se o usuário
    possui saldo suficiente.
    
    Exemplo de uso:
        PUT /transferir
        Headers: {'Authorization': 'Bearer <token_jwt>'}
        Body: {
            'valor': 100.00,
            'conta_destino': '1234567890',
            'agencia_destino': '123456,
        }    
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        transferencia = await api_transaction_service.transferir_bd(body.valor, body.conta_destino, body.agencia_destino, credenciais['id_conta'], credenciais['agencia_id'])
        transferencia = json.loads(transferencia)

        if transferencia['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_transaction_service.transferir_bd'")
        
        return Transferir_Resp(cod_resp = transferencia['cod_resp'], text_resp = transferencia['text_resp'], saldo_atual = transferencia['saldo_atual'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.get('/consultar_saldo', response_model = ConsultarSaldo_Resp)
async def consultar_saldo(credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Realiza a consulta do saldo total e saldo disponível da conta bancária do usuário.

    Este endpoint permite ao usuário consultar o saldo total e o saldo disponível de sua conta bancária. A autenticação é feita através
    de um token JWT fornecido no cabeçalho da solicitação.

    Exemplo de uso:
        GET /consultar_saldo
        Headers: {'Authorization': 'Bearer <token_jwt>'}
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        consulta = await api_account_service.consultar_saldo_db(credenciais['agencia_id'], credenciais['id_conta'])
        consulta = json.loads(consulta)

        if consulta['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_account_service.consultar_saldo_db'")
        
        return ConsultarSaldo_Resp(cod_resp = consulta['cod_resp'], nome = consulta['nome'], id_conta = consulta['id_conta'], agencia_id = consulta['agencia_id'], saldo = consulta['saldo'], saldo_disponivel = consulta['saldo_disponivel'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.get('/consultar_extrato', response_model = Extrato_Resp_Model)
async def consultar_extrato(body: Extrato_Req, credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Consulta o extrato bancário da conta do usuário para a data especificado no corpo da solicitação.

    Este endpoint permite ao usuário consultar o extrato de sua conta bancária, incluindo todas as transações realizadas na data especificada.
    A autenticação é realizada através do token JWT fornecido na solicitação.

    Exemplo de uso:
        GET /consultar_extrato
        Headers: {'Authorization': 'Bearer <token_jwt>'}
        body: {
            'data_consulta': '2024-03-31'
        }
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        extrato = await api_account_service.consultar_extrato_bd(credenciais['agencia_id'], credenciais['id_conta'], body.data_consulta)
        extrato = json.loads(extrato)

        if extrato['status_code'] == 500:
            raise HTTPException(status_code = 500, detail = "Operação indisponível no momento, devido a falha ao tentar realizar a operação em 'api_account_service.consultar_saldo_db'")
        
        return Extrato_Resp_Model(cod_resp = extrato['cod_resp'], id_conta = credenciais['id_conta'], agencia_id = credenciais['agencia_id'], data_consulta = extrato['data_consulta'], nome = extrato['nome'], saldo_atual = extrato['saldo_atual'], transacoes = extrato['transacoes'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.get('/consultar_info_cartao', response_model = Consultar_Info_Cartao_Resp)
async def consultar_info_cartao(credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Consulta informações do cartão associado à conta do usuário.

    Este endpoint fornece detalhes do cartão físico vinculado à conta bancária do usuário. As informações incluem
    o número do cartão, código CVV e data de validade. A autenticação do usuário é realizada através de token JWT fornecido no cabeçalho
    da solicitação.

    Exemplo de uso:
        GET /consultar_info_cartao
        Headers: {'Authorization': 'Bearer <token_jwt>'}    
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        consulta = await api_account_service.consultar_info_cartao_db(credenciais['id_conta'], credenciais['senha'])
        consulta = json.loads(consulta)

        return Consultar_Info_Cartao_Resp(cod_resp = consulta['cod_resp'], num_cartao = consulta['num_cartao'], cod_cvv = consulta['cod_cvv'], val_cartao = consulta['val_cartao'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.get('/consultar_saques_diarios', response_model = ConsultaSaquesDiarios_Resp)
async def consultar_saques_diarios(credenciais: str = Depends(api_auth_service.get_current_user)):
    """ 
    Consulta o número de saques realizados pelo usuário no dia atual.

    Este endpoint verifica a quantidade de saques que foram realizados no dia da solicitação, ajudando a gerenciair o limite
    diário de saques. A autenticação é realizada através de token JWT enviado no cabeçalho da solicitação.

    Exemplo de uso:
        GET /consultar_saques_diarios
        Headers: {'Authorization': 'Bearer <token_jwt>'}
    """
    credenciais = json.loads(credenciais)

    if credenciais['status_code'] == 500:
        raise HTTPException(status_code = 500, detail = 'Erro na operação de autorização/obtenção das credenciais a partir do token de acesso.')

    try:
        consulta = await api_account_service.consultar_saques_diarios_bd(credenciais['id_conta'])
        consulta = json.loads(consulta)

        return ConsultaSaquesDiarios_Resp(cod_resp = consulta['cod_resp'], saques_hoje = consulta['saques_hoje'])
    
    except:
        raise HTTPException(status_code = 500, detail = 'Erro interno do servidor. Falha ao tentar executar o bloco de código do endpoint.')

@app.post('/cadastrar_cliente')
async def cadastrar_cliente():
    "Responsável pelo cadastro de clientes"
    pass

@app.post('/cadastrar_conta_bancaria')
async def cadastrar_conta_bancaria():
    "Responsável pelo cadastro de contas bancárias"
    pass