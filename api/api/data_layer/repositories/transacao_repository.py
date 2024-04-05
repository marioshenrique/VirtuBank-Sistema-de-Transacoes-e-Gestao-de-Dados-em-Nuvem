from sqlalchemy.orm import Session
from sqlalchemy import text
from api.data_layer.models.transacao_model import Transacao
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from models.transacao_model import Transacao
import datetime

async def get_transacao_by_id_conta_and_data(db_session: AsyncSession, conta_id: str, data_transacao: datetime):
    "Coleta os registros de transações da tabela 'transacao' a partir da coluna 'conta_id' e 'data_transacao'"
    try:
        stmt = select(Transacao).filter(Transacao.conta_id == conta_id, Transacao.data_transacao == data_transacao)
        result = await db_session.execute(stmt)
        consulta = result.scalars().all()
        if not consulta:
            return {'status_code': 404} #Não foram encontradas movimentações
        else:
            return {'status_code': 200, 'resposta': consulta} #Movimentações encontradas
    except:
        return {'status_code': 500} #Erro interno do servidor

async def get_count_saques_diarios(db_session: AsyncSession, conta_id: str, data_transacao: datetime):
    "Conta o número de registros associados à 'conta_id', 'data_transacao' e 'tipo' = 'saque' na tabela 'transacao'."
    try:
        query = text("""
                    SELECT COUNT(*) FROM transacao
                    WHERE conta_id = :conta_id AND tipo = 'saque' AND data_transacao:: date = :data_transacao
                    """)
        resultado = await db_session.execute(query, {'conta_id': conta_id, 'data_transacao': data_transacao})

        contagem = int(resultado.scalar())

        return {'status_code': 200, 'resposta': contagem}
    except:
        return {'status_code': 500} #Erro interno do servidor

async def insert_transacao(db_session: AsyncSession, conta_id: str, tipo: str, data_transacao: datetime, valor: float, saldo_final: float, saldo_inicial: float):
    "Insere um novo registro na tabela 'transacao'."
    try:
        nova_transacao = Transacao(
            conta_id = conta_id,
            tipo = tipo,
            data_transacao = data_transacao,
            valor = valor,
            saldo_final = saldo_final,
            saldo_inicial = saldo_inicial
        )
        db_session.add(nova_transacao)
        return {'status_code': 200} #Operação bem-sucedida
    except:
        return {'status_code': 500} #Erro interno do servidor