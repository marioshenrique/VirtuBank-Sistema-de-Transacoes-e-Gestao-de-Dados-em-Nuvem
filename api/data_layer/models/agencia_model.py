from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Agencia(Base):
    "A classe Agencia representa o modelo mapeado da tabela 'agencia' do banco de dados."

    __tablename__ = 'agencia'
    id_agencia = Column(String(6), primary_key = True)
    nome = Column(String(255), nullable = False)
    rua = Column(String(255), nullable = False)
    cidade = Column(String(100), nullable = False)
    estado = Column(String(2), nullable = False)
