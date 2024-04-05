from sqlalchemy.orm import Session
from api.data_layer.models.agencia_model import Agencia
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from models.agencia_model import Agencia

async def get_agencia_by_id_agencia(db_session: AsyncSession, id_agencia: str):
    "Coleta um registro da tabela 'agencia' a partir da coluna 'id_agencia'"
    try:
        stmt = select(Agencia).filter(Agencia.id_agencia == id_agencia)
        result = await db_session.execute(stmt)
        consulta = result.scalars().first()
        
        if consulta is None:
            return {'status_code': 404} #Registro não encontrado
        else:
            return {'status_code': 200, 'resposta': consulta} #Registro encontrado
    except:
        return {'status_code': 500} #Erro interno do servidor