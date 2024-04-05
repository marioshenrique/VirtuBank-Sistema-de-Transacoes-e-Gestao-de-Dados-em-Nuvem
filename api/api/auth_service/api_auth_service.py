from datetime import datetime, timedelta
from fastapi import Depends
import jwt
from api.data_layer import api_data_access
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import json

ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

load_dotenv('api/.env')  # Carrega as variáveis de ambiente de `.env`

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

oauth2_scheme_token = OAuth2PasswordBearer(tokenUrl="/token")

@asynccontextmanager
async def get_session_async_R():
    assyncsession = api_data_access.get_async_session()
    try:
        yield assyncsession
    except:
        await assyncsession.rollback()
        raise
    finally:
        await assyncsession.close()

async def autenticacao_usuario(id_conta: str, agencia_id: str, senha: str):
    """
    Autentica as credenciais fornecidas pelo usuário.

    Esta função verifica as credenciais do usuário comparando-as com as informações armazenadas no
    banco de dados. 
    """
    try:
        async with get_session_async_R() as asyncsession:
            #Verifica se as credenciais estão corretas
            consulta = await api_data_access.get_count_conta_auth(asyncsession, id_conta, agencia_id, senha)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            if consulta['resposta'] == 0:
                return {'status_code': 400, 'detail': 'Credenciais de conta incorretas!'} #credenciais incorretas
            #Se todas as verificações passarem
            return {'status_code': 200,'estado': True, 'id_conta': id_conta, 'agencia_id': agencia_id, 'senha': senha} #Usuário autenticado
    except:
        return  {'status_code': 500, 'detail': 'Não foi possível se conectar ao sistema.'} #Não foi possível se conectar ao sistema

async def create_access_token(id_conta, agencia_id, senha):
    """ 
    Gera um token JWT para autenticação de usuário.

    Esta função cria um token JWT (JSON Web Token) que é usado para autenticar um usuário e um refresh token JWT para atualizar o token de acesso.
    Os tokens gerados incluem informações sobre as credenciais do usuário, especificadas pelo parâmetro 'data'.
    Além das informações de credenciais do usuário (número da conta, número da agência e senha) armazenada no 
    parâmetro 'data', os tokens também contém um campo que determina quando o token irá expirar.
    
    Notas:
        O payload dos tokens contém as seguintes informações: {'sub': id_conta-agencia_id, 'exp': valor de exp}
    """
    try:
        credenciais = await autenticacao_usuario(id_conta, agencia_id, senha)
        if credenciais['status_code'] == 400:
            return json.dumps({'status_code': 400, 'detail': 'Credenciais de conta incorretas!'})
        
        if credenciais['status_code'] == 500:
            return json.dumps({'status_code': 500, 'detail': 'Não foi possível se conectar ao sistema!'})
        
        access_token_expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires_delta = timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)

        data_token = {'sub': credenciais['id_conta']+'-'+credenciais['agencia_id']+'-'+credenciais['senha']}
        data_token_refresh = {'sub': credenciais['id_conta']+'-'+credenciais['agencia_id']+'-'+credenciais['senha']}

        to_encode_token = data_token.copy()
        to_encode_refresh = data_token_refresh.copy()

        expire_token = datetime.utcnow() + access_token_expires_delta

        to_encode_token.update({"exp": expire_token})

        expire_refresh_token = datetime.utcnow() + refresh_token_expires_delta
        to_encode_refresh.update({"exp": expire_refresh_token})

        token_jwt = jwt.encode(to_encode_token, SECRET_KEY, algorithm = ALGORITHM)
        refresh_token_jwt = jwt.encode(to_encode_refresh, SECRET_KEY, algorithm = ALGORITHM)

        return json.dumps({'status_code': 200, 'token': token_jwt, 'token_refresh': refresh_token_jwt})
    except:
        return json.dumps({'status_code': 500, 'detail': 'Falha na obtenção do token de acesso.'})
    
async def refresh_access_token(refresh_token: str):
    """Esta função é responsável por atualizar o token de acesso JWT e o refresh token JWT do usuário, 
    sendo chamada apenas quando expira-se o token de acesso do usuário."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        credenciais: str = payload.get("sub")
        id_conta = credenciais.split('-')[0]
        agencia_id = credenciais.split('-')[1]
        senha = credenciais.split('-')[2]

        if credenciais is None:
            return json.dumps({'status_code': 401, 
                                'detail': 'Credenciais inválidas no token de acesso'})
        if id_conta is None:
            return json.dumps({'status_code': 401, 
                                'detail': 'Credenciais inválidas no token de acesso'})
        if agencia_id is None:
            return json.dumps({'status_code': 401, 
                                'detail': 'Credenciais inválidas no token de acesso'})
        if senha is None:
            return json.dumps({'status_code': 401, 
                                'detail': 'Credenciais inválidas no token de acesso'})
            
        new_token_jwt = await create_access_token(id_conta, agencia_id, senha)
        new_token_jwt = json.loads(new_token_jwt)

        if new_token_jwt['status_code'] == 400:
            return json.dumps({'status_code': 401, 
                                'detail': 'Falha na autenticação! Credenciais inválidas no token de refresh.'})
        if new_token_jwt['status_code'] == 500:
            return json.dumps({'status_code': 500,
                                'detail': 'Falha na obtenção do token de acesso.'})
            
        token = new_token_jwt['token'] 
        token_refresh = new_token_jwt['token_refresh']

        return json.dumps({'status_code': 200, 'token': token, 'token_refresh': token_refresh})    

    except Exception as e:
        error_message = str(e)
        return json.dumps({'status_code': 500,
                           'detail': f'Falha na obtenção do token de acesso. Erro: {error_message}.'})

async def get_current_user(token: str = Depends(oauth2_scheme_token)):
    """
    Autentica um usuário baseado em um token JWT fornecido como argumento da função.

    Esta função é chamada pelas funções de visualização dos endpoints para autenticar o usuário,
    a partir do token JWT fornecido, e obter as informações das credenciais (número da conta, número
    da agência e senha) armazenadas na carga útil do token (parâmetro 'sub'). A chave 'sub' na carga útil
    é usada para armazenar as credenciais do usuário. A chave contém o 'id_conta', 'agencia_id' e 'senha'
    necessários para as operações realizadas pela API.

    Parâmetros:
        token (str): O token JWT fornecido no cabeçalho (headers) 'Authorization' da solicitação HTTP no
        formato 'Bearer <token>'. O token é automaticamente obtido através da dependência 'oauth2_scheme'.

    Retorna:
        dict: Um dicionário contendo as credenciais do usuário ('id_conta', 'agencia_id', 'senha') se a autenticação
        for bem-sucedida.
    
    Levanta:
        HTTPException: Uma exceção é levantada se a autenticação falhar. A autenticação pode falhar devido a falhas
        na validação do token, informações de credenciais ausentes no token ou incorretas, ou se as credenciais não
        correspondem a um usuário existente no banco de dados do sistema.
    
    Exemplo de uso:
        Esta função é usada pelas funções de visualização de forma indireta:

        @app.get('/user/profile')
        async def user_profile(user: dict = Depends(get_current_user)):
            #A variável 'user' contém das credenciais do usuário autenticado.
            # As  credenciais são acessadas da seguinte forma: 
            # id_conta = user.id_conta
            # agencia_id = user.agencia_id
            # senha = user.senha
            #Considerando que 'get_current_user' retorna {'id_conta': .., 'agencia_id': ..., 'senha':...}
    """
    try:
        async with get_session_async_R() as asyncsession:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            credenciais: str = payload.get("sub")
            id_conta = credenciais.split('-')[0]
            agencia_id = credenciais.split('-')[1]
            senha = credenciais.split('-')[2]

            if credenciais is None:
                return json.dumps({'status_code': 500, 'detail': 'Credenciais inválidas no token de acesso'})
            if id_conta is None:
                return json.dumps({'status_code': 500, 'detail': 'Credenciais inválidas no token de acesso'})
            if agencia_id is None:
                return json.dumps({'status_code': 500, 'detail': 'Credenciais inválidas no token de acesso'})
            if senha is None:
                return json.dumps({'status_code': 500, 'detail': 'Credenciais inválidas no token de acesso'})
            
            #Verificação adicional das credenciais do usuário
            #Verificar se 'id_conta' e 'agencia_id' existem no banco de dados
            consulta = await api_data_access.get_count_conta_verify(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)

            if consulta['status_code'] == 500:
                return json.dumps({'status_code': 500, 'detail': 'Falha na conexão com o banco de dados.'})
            
            return json.dumps({'status_code': 200, 'id_conta': id_conta, 'agencia_id': agencia_id, 'senha': senha})
    except:
        return json.dumps({'status_code': 500})