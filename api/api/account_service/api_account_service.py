from api.data_layer import api_data_access
from datetime import datetime
from contextlib import asynccontextmanager
import json

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

@asynccontextmanager
async def get_session_async_CUD():
    asyncsession = api_data_access.get_async_session()
    try:
        yield asyncsession #passa a sessão para o bloco with e pausa a execução do gerenciador de contexto
        await asyncsession.commit() #tenta comitar as transações se todas as operações foram bem-sucedidas
    except:
        asyncsession.rollback() #reverte todas as transações se ocorrer uma exceção
        raise #propaga a exceção
    finally:
        await asyncsession.close() #garante que a sessão seja fechada

async def consultar_info_conta_db(id_conta: str, agencia_id: str):
    """
    Consulta informações detalhadas da conta bancária.
    """
    try:
        async with get_session_async_R() as asyncsession:
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            return json.dumps({
                'status_code': 200,
                'nome': consulta['nome'],
                'id_conta': consulta['id_conta'],
                'agencia_id': consulta['agencia_id'],
                'cliente_id': consulta['cliente_id'],
                'saldo_atual': consulta['saldo_atual'],
                'saldo_disponivel': consulta['saldo_disponivel'],
                'tipo_conta': consulta['tipo_conta'],
                'status_conta': consulta['status_conta'],
                'data_criacao': consulta['data_criacao'],
                'data_fechamento': consulta['data_fechamento'],
                'senha_hash': consulta['senha_hash']
            })
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor
    
async def consultar_saldo_db(agencia_id: str, id_conta: str):
    """ 
    Consulta informações sobre o saldo total e o saldo disponível da conta bancária.
    """
    try:
        async with get_session_async_R() as asyncsession:
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            return json.dumps({'status_code': 200,
                               'cod_resp': 0,
                               'nome': consulta['nome'], 
                               'id_conta': consulta['id_conta'], 
                               'agencia_id': consulta['agencia_id'], 
                               'saldo': consulta['saldo_atual'], 
                               'saldo_disponivel': consulta['saldo_disponivel']})
    
    except:
        return json.dumps({'status_code': 500})

async def consultar_extrato_bd( agencia_id: str, id_conta: str, data_consulta: str):
    """ 
    Consulta o extrato bancário de uma conta bancária para uma data especificada.
    """
    try:
        async with get_session_async_R() as asyncsession:
            data_consulta = datetime.strptime(data_consulta, '%Y-%m-%d')
            transacoes = await api_data_access.get_transacao(asyncsession, id_conta, data_consulta)
            transacoes = json.loads(transacoes)
            if transacoes['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')

            data_consulta = data_consulta.strftime('%d/%m/%Y')

            if transacoes['status_code'] == 404:
                return json.dumps({'status_code': 404, 
                                   'cod_resp': 0, 
                                   'id_conta': id_conta, 
                                   'agencia_id': agencia_id, 
                                   'data_consulta': data_consulta, 
                                   'nome': consulta['nome'], 
                                   'saldo_atual': consulta['saldo_atual'], 
                                   'transacoes': None})
            
            return json.dumps({'status_code': 200, 
                               'cod_resp': 1, 
                               'id_conta': id_conta, 
                               'agencia_id': agencia_id, 
                               'data_consulta': data_consulta, 
                               'nome': consulta['nome'], 
                               'saldo_atual': consulta['saldo_atual'], 
                               'transacoes': transacoes['resposta']})
    except:
        return json.dumps({'status_code': 500})
    
async def consultar_info_cartao_db(id_conta: str, senha: str):
    """
    Consulta informações criptografadas do cartão associado à conta bancária.
    """
    try:
        async with get_session_async_R() as asyncsession:
            consulta = await api_data_access.get_cartao(asyncsession, senha, id_conta)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Não foram encontrados registros no banco de dados.')

            numero_cartao = consulta['num_cartao']
            ultimos_digitos_cartao = numero_cartao[-4:]
            oculto = '*' * 4
            numero_cartao = oculto + ultimos_digitos_cartao

            return json.dumps({'status_code': 200, 
                               'cod_resp': 0, 
                               'num_cartao': numero_cartao, 
                               'cod_cvv': consulta['cod_cvv'], 
                               'val_cartao': consulta['val_cartao']})
    except:
        return json.dumps({'status_code': 500, 
                           'cod_resp': 1, 
                           'num_cartao': None, 
                           'cod_cvv': None, 
                           'val_cartao': None})
    
async def consultar_saques_diarios_bd(id_conta: str):
    """ 
    Consulta a quantidade de saques realizados na conta no dia atual.
    """
    try:
        async with get_session_async_R() as asyncsession:
            consulta = await api_data_access.get_saques_diarios(asyncsession, id_conta, datetime.now().date())
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            return json.dumps({'status_code': 200, 
                               'cod_resp': 0, 
                               'saques_hoje': consulta['num_saques']})
    except:
        return json.dumps({'status_code': 500, 
                           'cod_resp': 1, 
                           'saques_hoje': None})