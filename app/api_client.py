import requests
import jwt
from datetime import datetime

URL_BASE = "http://54.173.187.227"

class Sistema:
    """ 
    Representa um sistema que permite autenticação de usuário e acesso a recursos protegidos.
    """
    token_global = None
    refresh_token_global = None

    def get_token(self, id_conta: str, agencia_id: str, senha: str):
        """ 
        Responsável por autenticar o usuário e obter um token de acesso ao sistema e um token de refresh para renovação do token de acesso.
        """
        try:
            dados_credenciais = {
                "id_conta": id_conta,
                "agencia_id": agencia_id,
                "senha": senha
            }
            response = requests.post(f"{URL_BASE}/token", json = dados_credenciais)
            token_response = response.json()
            print(f'get_token status_code: {response.status_code}')
            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get("access_token")
                refresh_token = token_response.get("refresh_token")
                Sistema.token_global = str(access_token)
                Sistema.refresh_token_global = str(refresh_token)
                return {'cod_resp': 200, 'token': access_token, 'refresh_token': refresh_token}

            elif response.status_code == 400:
                return {'cod_resp': 400, 'txt_resp': 'Falha ao obter o token de acesso. Motivo: credenciais de acesso incorretas.'}
        
            elif response.status_code == 500:
                return {'cod_resp': 500, 'txt_resp': 'Falha ao obter o token de acesso. Motivo: erro interno do servidor.'}
            
            else:
                return {'cod_resp': 500, 'text_resp': 'Falha ao obter o token de acesso. Motivo: desconhecido, código de status não tratado.'}

        except requests.exceptions.RequestException as e:
            print(f'Erro ao tentar obter o token de acesso: {e}')
            return {'cod_resp': 500, 'txt_resp': 'Falha na tentativa de requisição de token de acesso.'}

    def check_and_renew_token(self):
        """Responsável por verificar a validade do token e, quando o token estiver expirado, requisitar um novo token de acesso, 
        um novo token de refresh e armazená-los na variável global 'Sistema.token_global' e 'Sistema.refresh_token_global'."""
        try:
            payload = jwt.decode(Sistema.token_global, options = {'verify_signature': False})
            exp = payload.get('exp')
            
            if datetime.utcnow() > datetime.utcfromtimestamp(exp):
                print('Token expirado.')
                headers = {"Authorization": f"Bearer {Sistema.refresh_token_global}"}
                response = requests.post(f"{URL_BASE}/refresh_token", headers = headers)
                if response.status_code == 200:
                    data = response.json()
                    access_token = data['access_token']
                    refresh_token = data['refresh_token']
                    Sistema.token_global = access_token
                    Sistema.refresh_token_global = refresh_token
                    print('Novo token de acesso gerado.')
                    print('Novo refresh token gerado.')
                elif response.status_code == 401:
                    print('Falha na autenticação. Token de refresh inválido ou expirado.')
                elif response.status_code == 500:
                    print('Erro interno do servidor ao tentar renovar o token.')
                else:
                    print(f'Resposta inesperada: {response.status_code}')
            else:
                print('Token válido')
        except:
            print('Erro ao tentar renovar o token de acesso.')
        
    def check_status(self):
        try:
            response = requests.get(url = f'{URL_BASE}/status')
            if response.status_code == 200:
                print('API está online.')
                return True
            else:
                print(f'A API está offline. Código de status: {response.status_code}')
                return False
        except requests.exceptions.RequestException as e:
            print(f'Erro ao tentar acessar a API: {e}')
            return False
     
class Sistema_Bancario:

    def __init__(self):
        self.sistema = Sistema()

    def depositar(self, valor: float):
        """ 
        Realiza uma operação de depósito na conta do usuário através de um endpoint da API.

        Esta função envia uma solicitação para o endpoint '/depositar' da API para depositar o valor
        na conta do usuário. A autenticação é feita usando um token JWT.
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            body = {'valor': valor}
            headers = {"Authorization": f"Bearer {Sistema.token_global}"}
            response = requests.put(f"{URL_BASE}/depositar", json = body, headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200, 'text_resp': resposta['text_resp'], 'saldo_atual': resposta['saldo_atual']}
            elif response.status_code == 500:
                return {'status_code': 500, 'text_resp': 'Não foi possível realizar a operação. Erro interno do servidor.'}
        except:
            return {'status_code': 503, 'text_resp': 'Não foi possível realizar a operação. Serviço indisponível no momento.'}
        
    def sacar(self, valor: float):
        """ 
        Envia uma solicitação para sacar um valor da conta do usuário.

        Esta função envia uma solicitação PUT para o endpoint '/sacar' da API para realizar um saque na conta.
        A autenticação é realizada a partir de um token JWT.
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            dados = {'valor': valor}
            headers = {'Authorization': f'Bearer {Sistema.token_global}'}
            response = requests.put(f"{URL_BASE}/sacar", json = dados, headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200,
                         'text_resp': resposta['text_resp'],
                         'saques_diarios': resposta['saques_diarios'],
                         'saldo_atual': resposta['saldo_atual']}
            elif response.status_code == 500:
                return {'status_code': 500, 'text_resp': 'Não foi possível realizar a operação. Erro interno do servidor.'}
        except:
            return {'status_code': 503, 'text_resp': 'Não foi possível realizar a operação. Servidor indisponível no momento.'}
        
    def transferir(self, valor: float, conta_destino: str, agencia_destino: str):
        """ 
        Realiza uma transferência de valor da conta do usuário para uma conta destino.

        Esta função envia uma solicitação PUT ao endpoint '/transferir' da API para transferir um valor da conta do
        usuário autenticado para uma conta destino, especificado pelo id da conta e id da agência. A autenticação é realizada
        utilizando um token JWT fornecido no cabeçalho (headers) da solicitação.
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            dados = {
                'valor': valor,
                'conta_destino': conta_destino,
                'agencia_destino': agencia_destino,
            }
            headers = {'Authorization': f'Bearer {Sistema.token_global}'}
            response = requests.put(f"{URL_BASE}/transferir", json = dados, headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200, 
                        'text_resp': resposta['text_resp'],
                        'saldo_atual': resposta['saldo_atual']}
            elif response.status_code == 500:
                return {'status_code': 500, 
                        'text_resp': 'Não foi possível realizar a operação. Erro interno do servidor.'}
        except:
            return {'status_code': 503,
                    'text_resp': 'Não foi possível realizar a operação. Servidor indisponível no momento.'}

    def consultar_conta(self):
        """ 
        Consulta os dados da conta bancária do usuário.

        Esta função envia uma solicitação GET ao endpoint '/consultar_conta' da API para obter informações
        da conta bancária do usuário. A autenticação é realizada utilizando um token JWT fornecido no cabeçaho
        da solicitação (headers).
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            headers = {"Authorization": f"Bearer {Sistema.token_global}"}
            response = requests.get(f"{URL_BASE}/consultar_conta", headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200,
                        'nome_cliente': resposta['nome_cliente'],
                        'id_conta': resposta['id_conta'],
                        'agencia_id': resposta['agencia_id'],
                        'tipo_conta': resposta['tipo_conta'],
                        'status_conta': resposta['status_conta'],
                        'data_criacao': resposta['data_criacao'],
                        'data_fechamento': resposta['data_fechamento']
                        }
            elif response.status_code == 500:
                return {'status_code': 500,
                        'text_resp': 'Não foi possível realizar a operação.'}
        except:
            return {'status_code': 503,
                    'text_resp': 'Não foi possível realizar a operação. Servidor indisponível no momento.'}

    def consultar_saldo(self):
        """ 
        Consulta as informações de saldo da conta do usuário autenticado.

        Esta função envia uma solicitação GET ao endpoint '/consultar_saldo' da API para obter informações de saldo
        e saldo disponível da conta do usuário. A autenticação é realizada utilizando token JWT fornecido no cabeçalho
        (headers) da solicitação.
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            headers = {'Authorization': f"Bearer {Sistema.token_global}"}
            response = requests.get(f"{URL_BASE}/consultar_saldo", headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200,
                        'nome': resposta['nome'],
                        'id_conta': resposta['id_conta'],
                        'agencia_id': resposta['agencia_id'],
                        'saldo': resposta['saldo'],
                        'saldo_disponivel': resposta['saldo_disponivel']
                        }
            elif response.status_code == 500:
                return {'status_code': 500, 
                        'text_resp': 'Não foi possível realizar a operação. Erro interno do servidor.'}
        except:
            return {'status_code': 503,
                    'text_resp': 'Não foi possível realizar a operação. Servidor indisponível no momento.'}

    def consultar_extrato(self, data_consulta):
        """ 
        Consulta o extrato bancário da conta para uma data esepcificada.

        Esta função envia uma solicitação GET ao endpoint '/consultar_extrato' da API para obter as transações
        bancárias da conta para a data de consulta fornecida. A solicitação inclui a data e um token JWT para autenticação, fornecido no cabeçalho
        da solicitação.
        """
        try:
            #Checar a validade do token e gerar um novo token, se o token estiver expirado.
            self.sistema.check_and_renew_token()

            dados = {'data_consulta': data_consulta}
            headers = {'Authorization': f'Bearer {Sistema.token_global}'}
            response = requests.get(f'{URL_BASE}/consultar_extrato', json = dados, headers = headers)
            if response.status_code == 200:
                resposta = response.json()
                return {'status_code': 200,
                        'id_conta': resposta['id_conta'],
                        'agencia_id': resposta['agencia_id'],
                        'data_consulta': resposta['data_consulta'],
                        'nome': resposta['nome'],
                        'saldo_atual': resposta['saldo_atual'],
                        'transacoes': resposta['transacoes']}
            elif response.status_code == 500:
                return {'status_code': 500, 
                        'text_resp': 'Não foi possível realizar a operação. Erro interno do servidor.'}
        except:
            return {'status_code': 503,
                    'text_resp': 'Não foi possível realizar a operação. Servidor indisponível no momento.'}

    def consultar_info_cartao(self):
        """ 
        Consulta informações do cartão bancário associado à conta do usuário autenticado.

        Esta função envia uma solicitação GET ao endpoint '/consultar_info_cartao' da API para obter informações
        sobre o cartão do usuário. A autenticação é realizada usando um token JWT para autenticar o usuário no sistema.
        """
        #Checar a validade do token e gerar um novo token, se o token estiver expirado.
        self.sistema.check_and_renew_token()

        headers = {'Authorization': f'Bearer {Sistema.token_global}'}
        response = requests.get(f"{URL_BASE}/consultar_info_cartao", headers = headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            return {'cod_resp': 500, 'text_resp': 'Não foi possível realizar a operação.'}
    
    def numero_saques_diarios(self):
        """ 
        Consulta o número de saques realizados pelo usuário no dia atual.

        Esta função envia uma solicitação GET ao endpoint '/consultar_saques_diarios' da API para determinar quantos
        saques foram realizados pela conta no dia atual. A autenticação é realizada usando token JWT fornecida no cabeçalho
        da solicitação (headers).
        """
        #Checar a validade do token e gerar um novo token, se o token estiver expirado.
        self.sistema.check_and_renew_token()

        headers = {'Authorization': f'Bearer {Sistema.token_global}'}
        response = requests.get(f'{URL_BASE}/consultar_saques_diarios', headers = headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            return {'cod_resp': 500, 'text_resp': 'Não foi possível realizar a operação.'}
