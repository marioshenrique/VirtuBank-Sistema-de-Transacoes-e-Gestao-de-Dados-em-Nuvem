from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    "A classe Cliente representa o modelo mapeado da tabela 'cliente' do banco de dados."

    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key = True)
    nome = Column(String(255), nullable = False)
    cpf = Column(String(11), nullable = False)
    rg = Column(String(15), nullable = False)
    telefone = Column(String(11), nullable = False)
    email = Column(String(255), unique = True)