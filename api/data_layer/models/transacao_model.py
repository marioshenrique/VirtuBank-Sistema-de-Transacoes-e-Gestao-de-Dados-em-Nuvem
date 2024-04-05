from sqlalchemy import Column, String, Integer, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transacao(Base):
    "A classe Transacao representa o modelo mapeado da tabela 'transacao' do banco de dados."

    __tablename__ = 'transacao'
    id_transacao = Column(Integer, primary_key = True)
    conta_id = Column(String(11), nullable = False)
    tipo = Column(String(25), nullable = False)
    data_transacao = Column(Date, nullable = False)
    valor = Column(Numeric(15,2), nullable = False)
    saldo_final = Column(Numeric(15,2), nullable = False)
    saldo_inicial = Column(Numeric(15,2), nullable = False)