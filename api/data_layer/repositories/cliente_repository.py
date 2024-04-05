from sqlalchemy.orm import Session
from api.data_layer.models.cliente_model import Cliente
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from models.cliente_model import Cliente

async def get_cliente_by_cpf_rg(db_session: AsyncSession, cpf: str, rg: str):
    "Coleta um registro da tabela 'cliente' a partir das colunas 'cpf' e 'rg'."
    try:
        stmt = select(Cliente).filter(Cliente.cpf == cpf, Cliente.rg == rg)
        result = await db_session.execute(stmt)
        consulta = result.scalars().first()
        if consulta is None:
            return {'status_code': 404} #Registro não encontrado
        else:
            return {'status_code': 200, 'resposta': consulta} #Registro encontrado
    except:
        return {'status_code': 500} #Erro interno do servidor