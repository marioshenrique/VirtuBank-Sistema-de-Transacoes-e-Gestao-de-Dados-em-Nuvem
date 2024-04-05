from sqlalchemy.ext.asyncio import AsyncSession
from api.data_layer.repositories.cliente_repository import get_cliente_by_cpf_rg
from api.data_layer.repositories.agencia_repository import get_agencia_by_id_agencia
from api.data_layer.repositories.transacao_repository import get_transacao_by_id_conta_and_data
from api.data_layer.repositories.conta_bancaria_repository import get_conta_bancaria_by_id_conta_and_agencia_id
from api.data_layer.repositories.cartao_cliente_repository import get_cartoes_cliente_by_id_conta
from api.data_layer.repositories.transacao_repository import get_count_saques_diarios
from api.data_layer.repositories.conta_bancaria_repository import update_saldo_atual
from api.data_layer.repositories.transacao_repository import insert_transacao
from api.data_layer.repositories.conta_bancaria_repository import count_conta_auth
from api.data_layer.repositories.conta_bancaria_repository import count_conta_verify
from api.data_layer.database_config.database_config import AsyncSessionLocal
import datetime
import json

def get_async_session():
    return AsyncSessionLocal()

async def get_cliente(session: AsyncSession, cpf: str, rg: str):
    "Responsável por extrair um registro da tabela 'cliente' do banco de dados."
    try:
        consulta = await get_cliente_by_cpf_rg(session, cpf, rg)
        if consulta['status_code'] == 200: #Registro encontrado no banco de dados
            return json.dumps({
                'status_code': 200,
                'id_cliente': consulta['resposta'].id_cliente,
                'nome': consulta['resposta'].nome,
                'cpf': consulta['resposta'].cpf,
                'rg': consulta['resposta'].rg,
                'telefone': consulta['resposta'].telefone,
                'email': consulta['resposta'].email
            })
        elif consulta['status_code'] == 404: #Registro não encontrado no banco de dados
            return json.dumps({'status_code': 404})
        elif consulta['status_code'] == 500: #Erro interno do servidor.
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor.

async def get_agencia(session: AsyncSession, id_agencia: str):
    "Responsável por extrair um registro da tabela 'agencia' do banco de dados."
    try:
        consulta = await get_agencia_by_id_agencia(session, id_agencia)
        if consulta['status_code'] == 200:
            return json.dumps({
                'status_code': 200,
                'id_agencia': consulta['resposta'].id_agencia,
                'nome': consulta['resposta'].nome,
                'rua': consulta['resposta'].rua,
                'cidade': consulta['resposta'].cidade,
                'estado': consulta['resposta'].estado
            })
        elif consulta['status_code'] == 404: #Registro não encontrado no banco de dados
            return json.dumps({'status_code': 404})
        elif consulta['status_code'] == 500: #Erro interno do servidor.
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor.

async def get_transacao(session: AsyncSession, conta_id: str, data_transacao: datetime):
    "Responsável por extrair os registros da tabela 'transacao' associados à 'conta_id' e à 'data_transacao'."
    try:
        transacoes = await get_transacao_by_id_conta_and_data(session, conta_id, data_transacao)
        #Checar as transações e processá-las
        if transacoes['status_code'] == 200: #Foram encontradas movimentações
            dict_transacoes = []
            for transacao in transacoes['resposta']:
                dict_transacoes.append({
                    'id_transacao': str(transacao.id_transacao),
                    'conta_id': str(transacao.conta_id),
                    'tipo': str(transacao.tipo),
                    'data_transacao': transacao.data_transacao.strftime('%d/%m/%Y'),
                    'valor': float(transacao.valor),
                    'saldo_final': float(transacao.saldo_final),
                    'saldo_inicial': float(transacao.saldo_inicial)
                })
            return json.dumps({'status_code': 200, 'resposta': dict_transacoes})
        elif transacoes['status_code'] == 404: #Não foram encontradas movimentações
            return json.dumps({'status_code': 404}) 
        elif transacoes['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except: 
        return json.dumps({'status_code': 500}) #Erro interno do servidor
        
async def get_conta(session: AsyncSession, id_conta: str, agencia_id: str):
    "Responsável por extrair um registro da tabela 'conta_bancaria' do banco de dados."
    try:
        resultado = await get_conta_bancaria_by_id_conta_and_agencia_id(session, id_conta, agencia_id)

        if resultado['status_code'] == 200: #Registro encontrado.
            conta_bancaria, nome_cliente = resultado['resposta']
            return json.dumps({
                'status_code': 200,
                'nome':str(nome_cliente),
                'id_conta': str(conta_bancaria.id_conta),
                'agencia_id': str(conta_bancaria.agencia_id),
                'cliente_id': str(conta_bancaria.cliente_id),
                'saldo_atual': float(conta_bancaria.saldo_atual),
                'saldo_disponivel': float(conta_bancaria.saldo_disponivel),
                'tipo_conta': str(conta_bancaria.tipo_conta),
                'status_conta': str(conta_bancaria.status_conta),
                'data_criacao': conta_bancaria.data_criacao.strftime('%d/%m/%Y'),
                'data_fechamento': conta_bancaria.data_fechamento.strftime('%d/%m/%Y') if conta_bancaria.data_fechamento else None,
                'senha_hash': str(conta_bancaria.senha_hash)
            })
        elif resultado['status_code'] == 404:
            return json.dumps({'status_code': 404}) #O registro não foi encontrado.
        elif resultado['status_code'] == 500:
            return json.dumps({'status_code': 500}) #Erro interno do servidor.
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor.

async def get_cartao(session: AsyncSession, senha: str, conta_id: str):
    "Responsável por extrair um registro da tabela 'cartao_cliente' do banco de dados."
    try:
        consulta  = await get_cartoes_cliente_by_id_conta(session, senha, conta_id)
        if consulta['status_code'] == 200: #Registro encontrado
            return json.dumps({
                'status_code': 200,
                'num_cartao': consulta['resposta'][0][0],
                'val_cartao': consulta['resposta'][0][2].strftime('%m/%Y'),
                'cod_cvv': consulta['resposta'][0][1]
            })
        elif consulta['status_code'] == 404: #Registro não encontrado
            return json.dumps({'status_code': 404})
        elif consulta['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor
    
async def get_saques_diarios(session: AsyncSession, conta_id: str, data_transacao: datetime):
    "Responsável por extrair a quantidade de registros associados à 'conta_id' e 'data_transacao'."
    try:
        resultado = await get_count_saques_diarios(session, conta_id, data_transacao)
        if resultado['status_code'] == 200:
            return json.dumps({
                'status_code': 200,
                'num_saques': resultado['resposta']})
        elif resultado['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor

async def put_saldo_atual(session: AsyncSession, id_conta: str, agencia_id: str, novo_saldo: float):
    "Responsável por atualizar a coluna 'saldo_atual' da tabela 'conta_bancaria' do banco de dados."
    try:
        resultado = await update_saldo_atual(session, id_conta, agencia_id, novo_saldo)
        if resultado['status_code'] == 200: #Contra encontrada e saldo atualizado
            return json.dumps({'status_code': 200})
        elif resultado['status_code'] == 404: #Conta não encontrada
            return json.dumps({'status_code': 404})
        elif resultado['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor

async def post_transacao(session: AsyncSession, conta_id: str, tipo: str, data_transacao: datetime, valor: float, saldo_final: float, saldo_inicial: float):
    "Responsável por inserir um novo registro na tabela 'transacao' do banco de dados."
    try:
        resultado = await insert_transacao(session, conta_id, tipo, data_transacao, valor, saldo_final, saldo_inicial)
        if resultado['status_code'] == 200: #Operação bem-sucedida
            return json.dumps({'status_code': 200})
        elif resultado['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor
    
async def get_count_conta_auth(session: AsyncSession, id_conta: str, agencia_id: str, senha: str):
    "Responsável por verificar se as credenciais de acesso do usuário estão corretas"
    try:
        resultado = await count_conta_auth(session, id_conta, agencia_id, senha)
        if resultado['status_code'] == 200: #Operação bem-sucedida
            return json.dumps({'status_code': 200, 'resposta': resultado['resposta']})
        elif resultado['status_code'] == 500:
            return json.dumps({'status_code': 500}) #Erro interno do servidor
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor

async def get_count_conta_verify(session: AsyncSession, id_conta: str, agencia_id: str):
    "Responsável por verificar se existe um registro com 'id_conta' e 'agencia_id' no banco de dados."
    try:
        resultado = await count_conta_verify(session, id_conta, agencia_id)
        if resultado['status_code'] == 200: #Operação bem-sucedida
            return json.dumps({'status_code': 200, 'resposta': resultado['resposta']})
        elif resultado['status_code'] == 500: #Erro interno do servidor
            return json.dumps({'status_code': 500})
    except:
        return json.dumps({'status_code': 500}) #Erro interno do servidor
