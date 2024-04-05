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
        await asyncsession.rollback() #reverte todas as transações se ocorrer uma exceção
        raise #propaga a exceção
    finally:
        await asyncsession.close() #garante que a sessão seja fechada

async def depositar_bd(valor: float, id_conta: str, agencia_id: str):
    """
    Realiza o depósito de um valor na conta bancária especificada e registra a transação no banco de dados.

    Esta função é utilizada pelo endpoint '/depositar' para processar o depósito de valores da conta bancária do usuário.
    Ela verifica o valor do depósito, consulta o saldo atual da conta, realiza o depósito atualizando o saldo no banco de dados 
    e registra a transação de depósito.
    """
    try:
        async with get_session_async_CUD() as asyncsession:
            #garantindo que o valor é positivo
            valor = abs(valor)
            #Verificando se o valor a ser depositado é igual a zero
            if valor == 0:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 0, 
                                   'text_resp': 'O valor do depósito deve ser diferente de zero.', 
                                   'saldo': None})

            #consultar o saldo atual
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)

            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            
            if consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            saldo_inicial = consulta['saldo_atual']
            saldo = saldo_inicial
            saldo += valor

            #atualizar o saldo atual
            #Atualizar o saldo disponivel
            atualizar = await api_data_access.put_saldo_atual(asyncsession, id_conta, agencia_id, saldo)
            atualizar = json.loads(atualizar)
            if atualizar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            if atualizar['status_code'] == 404:
                raise ValueError('A conta não foi encontrada no banco de dados.')
                    
            #Registrar a transação no banco de dados
            registrar = await api_data_access.post_transacao(asyncsession, id_conta, 'deposito', datetime.now().date(), valor, saldo, saldo_inicial)
            registrar = json.loads(registrar)
            if registrar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
                    
            return json.dumps({'status_code': 200, 
                               'cod_resp': 1, 
                               'text_resp': f"Depósito de R$ {valor:.2f} realizado com sucesso. Seu saldo é R$ {saldo:.2f}", 
                               'saldo': saldo})
    
    except:
        return json.dumps({'status_code': 500})
    
async def sacar_bd(valor: float, id_conta: str, agencia_id: str):
    """ 
    Processa um saque da conta bancária do usuário especificado pelo 'id_conta' e 'agencia_id'.

    Esta função é usada internamente para realizar o saque de um valor da conta bancária.
    Ela verifica várias condições como o valor do saque, o limite de saque diário, e o saldo disponível na conta.
    Após verificação, ele atualiza o saldo da conta e registra a transação no banco de dados.
    """
    try:
        async with get_session_async_CUD() as asyncsession:
            valor = abs(valor)
            if valor == 0:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 0, 
                                   'text_resp': "O valor a ser sacado deve ser diferente de zero!",
                                   'saques_diarios': None,
                                   'saldo_atual': None}) 
            if valor > 5000:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 1, 
                                   'text_resp': "O valor a ser sacado excede o limite do saque! O valor deve ser menor que R$ 5000,00.",
                                   'saques_diarios': None,
                                   'saldo_atual': None})

            #Consultar saldo atual da conta
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            saldo_atual = consulta['saldo_atual']
            saldo_inicial = saldo_atual

            #Obter o número de saques diários associados a conta
            consulta = await api_data_access.get_saques_diarios(asyncsession, id_conta, datetime.now().date())
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            saques_hoje = consulta['num_saques']

            #Verifica o limite de saques diários
            if saques_hoje >= 3:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 2, 
                                   'text_resp': "Você já realizou três saques hoje. Não é possível realizar mais saques!",
                                   'saques_diarios': None,
                                   'saldo_atual': None})
            
            #Verificar se há saldo suficiente para o saque
            if saldo_atual < valor:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 3, 
                                   'text_resp': "Saldo insuficiente para realizar o saque!",
                                   'saques_diarios': None,
                                   'saldo_atual': None})   
            
            saldo_atual -= valor

            #Atualizar a o saldo da conta bancária no banco de dados
            atualizar = await api_data_access.put_saldo_atual(asyncsession, id_conta, agencia_id, saldo_atual)
            atualizar = json.loads(atualizar)
            if atualizar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            if atualizar['status_code'] == 404:
                raise ValueError('A conta não foi encontrada no banco de dados.')
                    
            #Registrar a transação no banco de dados
            registrar = await api_data_access.post_transacao(asyncsession, id_conta, 'saque', datetime.now().date(), valor, saldo_atual, saldo_inicial)
            registrar = json.loads(registrar)
            if registrar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
        
            return json.dumps({'status_code': 200, 
                               'cod_resp': 4, 
                               'text_resp':f"Saque de R$ {valor:.2f} realizado com sucesso. Seu saldo atual é R$ {saldo_atual:.2f}", 
                               'saques_diarios': saques_hoje + 1, 
                               'saldo_atual': saldo_atual})
    except:
        return json.dumps({'status_code': 500})

async def transferir_bd(valor: float, conta_destino: str, agencia_destino: str, id_conta: str, agencia_id: str):
    """ 
    Processa uma transferência de valor da conta do usuário para uma conta destino.

    Esta função é usada pelo endpoint '/transferir' do controller para realizar a transferência entra a conta do
    usuário (conta origem). Ela verifica a existência da conta a e da agência destinatárias, o valor da transferência,
    e o saldo disponível na conta de origem antes de proceder com a operação.
    """
    try:
        async with get_session_async_CUD() as asyncsession:
            #Verificar se agencia_destino existe
            resultado = await api_data_access.get_agencia(asyncsession, agencia_destino)
            resultado = json.loads(resultado)
            if resultado['status_code'] == 404:
                return json.dumps({'status_code': 404, 
                                   'cod_resp': 0,
                                   'text_resp': "Não foi possível realizar a operação! A agência destinatária não existe.",
                                   'saldo_atual': None})
            elif resultado['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            #Verificar se conta_destino existe
            resultado = await api_data_access.get_conta(asyncsession, conta_destino, agencia_destino)
            resultado = json.loads(resultado)
            if resultado['status_code'] == 404:
                return json.dumps({'status_code': 404, 
                                   'cod_resp': 1,
                                   'text_resp': "Não foi possível realizar a operação! A conta destinatária não existe.",
                                   'saldo_atual': None})
            elif resultado['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
                
            #Tratando valores negativos
            valor = abs(valor)
            #Verificar se o valor é igual a zero
            if valor == 0:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 2,
                                   'text_resp': "O valor a ser transferido deve ser diferente de zero.",
                                   'saldo_atual': None})
                    
            #Consultar o saldo da conta origem a partir do banco de dados
            consulta = await api_data_access.get_conta(asyncsession, id_conta, agencia_id)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            saldo_conta_origem = consulta['saldo_atual']
            saldo_inicial_conta_origem = saldo_conta_origem

            #Consultar o saldo da conta destino a partir do banco de dados
            consulta = await api_data_access.get_conta(asyncsession, conta_destino, agencia_destino)
            consulta = json.loads(consulta)
            if consulta['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            elif consulta['status_code'] == 404:
                raise ValueError('Registro não encontrado no banco de dados.')
            saldo_conta_destino = consulta['saldo_atual']
            saldo_inicial_conta_destino = saldo_conta_destino

            #Verificando se o saldo da conta origem é suficiente para a transferência
            if (saldo_conta_origem - valor) < 0:
                return json.dumps({'status_code': 400, 
                                   'cod_resp': 3,
                                   'text_resp': "Saldo insuficiente para transferência!",
                                   'saldo_atual': None})
            #Atualizar o saldo da conta origem com o novo valor
            saldo_conta_origem -= valor

            #Registrar o novo saldo da conta origem no banco de dados
            atualizar = await api_data_access.put_saldo_atual(asyncsession, id_conta, agencia_id, saldo_conta_origem)
            atualizar = json.loads(atualizar)
            if atualizar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            if atualizar['status_code'] == 404:
                raise ValueError('A conta não foi encontrada no banco de dados.')
                
            #Registrar a transação na conta origem como 'transferência' no banco de dados
            registrar = await api_data_access.post_transacao(asyncsession, id_conta, 'transferência', datetime.now().date(), -valor, saldo_conta_origem, saldo_inicial_conta_origem)
            registrar = json.loads(registrar)
            if registrar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
                    
            #Atualizar o saldo da conta destino com o novo valor
            saldo_conta_destino += valor
                    
            #Registrar o novo saldo da conta destino no banco de dados
            atualizar = await api_data_access.put_saldo_atual(asyncsession, conta_destino, agencia_destino, saldo_conta_destino)
            atualizar = json.loads(atualizar)
            if atualizar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
            if atualizar['status_code'] == 404:
                raise ValueError('A conta não foi encontrada no banco de dados.')
                    
            #Registrar a transação na conta destino como 'transferência' no banco de dados
            registrar = await api_data_access.post_transacao(asyncsession, conta_destino, 'transferência', datetime.now().date(), valor, saldo_conta_destino, saldo_inicial_conta_destino)
            registrar = json.loads(registrar)
            if registrar['status_code'] == 500:
                raise ValueError('Operação falhou no banco de dados.')
                    
            return json.dumps({'status_code': 200, 
                               'cod_resp': 4,
                               'text_resp': f"Transferência realizada com sucesso! Foi transferido o valor de R$ {valor} para a conta corrente {conta_destino} da agência {agencia_destino}.",
                               'saldo_atual': saldo_conta_origem})
    except:
        return json.dumps({'status_code': 500})