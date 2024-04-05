from sqlalchemy.orm import Session
from sqlalchemy import text
from api.data_layer.models.conta_bancaria_model import Conta_Bancaria
from api.data_layer.models.cliente_model import Cliente
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# from models.conta_bancaria_model import Conta_Bancaria
# from models.cliente_model import Cliente

async def get_conta_bancaria_by_id_conta_and_agencia_id(db_session: AsyncSession, id_conta: str, agencia_id: str):
    "Coleta registro com informações sobre uma conta bancária a partir das tabelas 'conta_bancaria' e 'cliente', usando 'id_conta' e 'agencia_id' para filtrar."
    try:
        stmt = select(Conta_Bancaria, Cliente.nome).join(Cliente, Conta_Bancaria.cliente_id == Cliente.id_cliente).filter(Conta_Bancaria.id_conta == id_conta, Conta_Bancaria.agencia_id == agencia_id)
        result = await db_session.execute(stmt)
        consulta = result.first()
        if consulta is None:
            return {'status_code': 404} #Nenhum registro foi encontrado.
        else:
            return {'status_code': 200, 'resposta': consulta} #Registro encontrado.
    except:
        return {'status_code': 500} #Erro interno do servidor.

async def update_saldo_atual(db_session: AsyncSession, id_conta: str, agencia_id: str, novo_saldo: float):
    "Atualizar a informação da coluna 'saldo_atual' da tabela 'conta_bancaria'."
    try:
        stmt = select(Conta_Bancaria).filter(Conta_Bancaria.id_conta == id_conta, Conta_Bancaria.agencia_id == agencia_id)
        result = await db_session.execute(stmt)
        conta = result.scalars().first()
        if conta is None:
            return {'status_code': 404} #Conta não encontrada
        conta.saldo_atual = novo_saldo
        conta.saldo_disponivel = novo_saldo
        return {'status_code': 200} #Conta encontrada e saldo atual atualizado
    except:
        return {'status_code': 500} #Erro interno do servidor

async def count_conta_auth(db_session: AsyncSession, id_conta: str, agencia_id: str, senha: str):
    "Conta o número de registros na tabela 'conta_bancaria' associados à 'id_conta', 'agencia_id' e 'senha'."
    try:
        query = text("""SELECT COUNT(*) FROM conta_bancaria WHERE id_conta = :id_conta AND agencia_id = :agencia_id AND senha_hash = crypt(:senha, senha_hash)""")
        
        resultado = await db_session.execute(query, {'id_conta': id_conta, 'agencia_id': agencia_id, 'senha': senha})

        contagem = int(resultado.scalar_one())

        return {'status_code': 200, 'resposta': contagem} #Operação bem-sucedida
    except:
        return {'status_code': 500} #Erro interno do servidor

async def count_conta_verify(db_session: AsyncSession, id_conta: str, agencia_id: str):
    "Conta o número de registros na tabela 'conta_bancaria' associados à 'id_conta' e 'agencia_id'."
    try:
        query = text("""SELECT COUNT(*) FROM conta_bancaria WHERE id_conta = :id_conta AND agencia_id = :agencia_id""")

        resultado = await db_session.execute(query, {'id_conta': id_conta, 'agencia_id': agencia_id})

        contagem = int(resultado.scalar_one())

        return {'status_code': 200, 'resposta': contagem} #Operação bem-sucedida
    except:
        return {'status_code': 500} #Erro interno do servidor