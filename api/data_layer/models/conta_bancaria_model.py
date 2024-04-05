from sqlalchemy import Column, String, Integer, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Conta_Bancaria(Base):
    "A classe Conta_Bancaria representa o modelo mapeado da tabela 'conta_bancaria' do banco de dados."

    __tablename__ = 'conta_bancaria'
    id_conta = Column(String(11), primary_key = True)
    agencia_id = Column(String(6), nullable = False)
    cliente_id = Column(Integer, nullable = False)
    saldo_atual = Column(Numeric(15,2), nullable = False)
    saldo_disponivel = Column(Numeric(15,2), nullable = False)
    tipo_conta = Column(String(20), nullable = False)
    status_conta = Column(String(20), nullable = False)
    data_criacao = Column(Date, nullable = False)
    data_fechamento = Column(Date)
    senha_hash = Column(String(100), nullable = False)