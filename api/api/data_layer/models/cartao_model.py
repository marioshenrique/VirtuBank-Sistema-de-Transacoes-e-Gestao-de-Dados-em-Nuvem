from sqlalchemy import Column, String, Date, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CartaoCliente(Base):
    "A classe CartaoCliente representa o modelo mapeado da tabela 'cartoes_cliente' do banco de dados."

    __Tablename__ = 'cartoes_cliente'
    id_cartao = Column(String(11), primary_key = True, nullable = False)
    conta_id = Column(String(11), nullable = False)
    data_validade = Column(Date, nullable = False)
    cript_cod_seguranca = Column(LargeBinary) #ByTea
    status = Column(String(20), nullable = False)
    tipo = Column(String(20), nullable = False)
    data_emissao = Column(Date, nullable = False)
    cript_pin =  Column(LargeBinary) #ByTea
    data_desativacao = Column(Date)
    cript_num_cartao = Column(LargeBinary) #ByTea