from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
import os

load_dotenv('api/.env')  # Carrega as variáveis de ambiente de `.env`

"Responsável por configurar a sessão de acesso ao banco de dados."

"Operações síncronas"
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind = engine, autocommit=False)

"Operações assíncronas"
DATABASE_URL_ASYNC = os.environ.get("DATABASE_URL_ASYNC")

engine_async = create_async_engine(DATABASE_URL_ASYNC, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)