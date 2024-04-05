from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

async def get_cartoes_cliente_by_id_conta(db_session: AsyncSession, chave_decript: str, conta_id: str):
    "Coleta um registro da tabela 'cartoes_cliente' a partir da coluna 'conta_id' e descriptografa as informações a partir da senha do usuário, armazenada em 'chave_decript'."
    try:
        sql_query = text("""
                SELECT 
                    pgp_sym_decrypt(cript_num_cartao, :chave_decript, 'cipher-algo=aes256') AS num_cartao_decriptado, 
                    pgp_sym_decrypt(cript_cod_seguranca, :chave_decript, 'cipher-algo=aes256') AS cod_seguranca_decriptado,
                    data_validade
                FROM cartoes_cliente 
                WHERE conta_id = :conta_id AND status = 'ativo'""")
        resultado = await db_session.execute(sql_query, {'chave_decript': chave_decript, 'conta_id': conta_id})

        consulta = resultado.fetchall()

        if not consulta:
            return {'status_code': 404} #Não foram registros no banco de dados
        else: 
            return {'status_code': 200, 'resposta': consulta} #Registros foram encontrados
    except:
        return {'status_code': 500} #Erro interno do servidor