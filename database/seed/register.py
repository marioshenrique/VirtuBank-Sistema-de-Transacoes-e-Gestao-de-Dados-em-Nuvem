import psycopg2
from datetime import datetime
import random
import string
import hashlib

class Cadastro:
    def __conectar_bd(self):
        uri = "postgresql://'[usuário]:[senha]@[host]/[base de dados]'"
        try:
            self.conn = psycopg2.connect(uri)
            return self.conn
        except:
            return None
        
    def __fechar_conexao_bd(self):
        if self.conn is not None:
            self.conn.close()

    def cadastrar_cliente_bd(self, cpf, rg, nome, data_nascimento, telefone, email):
        try:
            self.__conectar_bd() #Abre a conexão com o banco de dados
            self.cursor = self.conn.cursor() #Cria o cursor responsável pelas operações no banco de dados
            #Verificar se o cliente já possui cadastro a partir do CPF
            self.cursor.execute(
                "SELECT COUNT(*) FROM cliente WHERE cpf = %s",
                (cpf,)
            )
            row = self.cursor.fetchone()
            if row[0] > 0:
                return 0, "Já existe um cliente cadastrado com o mesmo CPF."
            #Verificar se o cliente já possui cadastro a partir do RG
            self.cursor.execute(
                "SELECT COUNT(*) FROM cliente WHERE rg = %s",
                (rg,)
            )
            row = self.cursor.fetchone()
            if row[0] > 0:
                return 0, "Já existe um cliente cadastrado com o mesmo RG."
            # Caso o cliente não possua cadastro, prossegue na operação de cadastro
            self.cursor.execute(
                """INSERT INTO cliente (nome, data_nascimento, cpf, rg, telefone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (nome, data_nascimento, cpf, rg, telefone, email)
            )
            #salvar a operação no banco de dados
            self.conn.commit()
            return 1, "Cliente cadastrado com sucesso."
        except:
            self.conn.rollback()
            return 0, "Não foi possível criar a conta do cliente"
        finally:
            self.__fechar_conexao_bd()


    def cadastrar_conta_bancaria_bd(self, id_agencia, cpf, rg, tipo_conta, senha_conta, pin_cartao):
        try:
            self.__conectar_bd() #Abre a conexão com o banco de dados
            self.cursor = self.conn.cursor() #Cria o cursor responsável pelas operações no banco de dados
                
            #Verificar se o usuário possui cadastro como cliente
            self.cursor.execute(
                "SELECT COUNT(*) FROM cliente WHERE cpf = %s AND rg = %s",
                (cpf, rg)
            )
            if self.cursor.fetchone()[0] == 0:
                return 0, "Cliente não encontrado no sistema."
                
            #Verificar se o número da agência está correto
            self.cursor.execute(
                "SELECT COUNT(*) FROM agencia WHERE id_agencia = %s",
                (id_agencia,)
            )
            if self.cursor.fetchone()[0] == 0:
                return 0, "Agência não encontrada."

            #Se o cliente possui cadastro e o número da agência está correto, prossegue na operação

            #coletando a informação "id_cliente" da tabela "cliente"
            self.cursor.execute(
                "SELECT id_cliente FROM cliente WHERE cpf = %s AND rg = %s",
                (cpf, rg)
            )
            cliente_id = self.cursor.fetchone()[0]

            #Definindo as informações iniciais da conta bancária
            saldo_atual = 0
            saldo_disponivel = 0
            status_conta = 'ativo'
            data_criacao = datetime.now().date()
            data_fechamento = None

            #Definindo um valor aleatório para 'id_conta'
            while True:
                #Gerar um número aleatório com 11 dígitos
                id_conta = ''.join(random.choices(string.digits, k = 11))

                #Verificar se o número já existe na tabela 'conta_bancaria'
                self.cursor.execute(
                    "SELECT COUNT(*) FROM conta_bancaria WHERE id_conta = %s",
                    (id_conta,)
                )
                if self.cursor.fetchone()[0] == 0:
                    break
                else:
                    pass

            #Inserindo o cadastro no banco de dados
            self.cursor.execute(
                """
                INSERT INTO conta_bancaria (
                    id_conta,
                    agencia_id,
                    cliente_id, 
                    saldo_atual, 
                    saldo_disponivel, 
                    tipo_conta, 
                    status_conta, 
                    data_criacao, 
                    data_fechamento, 
                    senha_hash )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, crypt(%s, gen_salt('bf')))""",
                (id_conta, id_agencia, cliente_id, saldo_atual, saldo_disponivel, tipo_conta,
                status_conta, data_criacao, data_fechamento, senha_conta)
            )
            #Criar as informações do cartão físico associado a conta"

            #Gerar um id aleatória para o atributo 'id_cartao', chave primário da tabela 'cartoes_cliente'
            while True:
                #Gerar um ID aleatório
                id_cartao = ''.join(random.choices(string.digits, k = 11)) #VARCHAR(11)
                #Verificar se o ID selecionado já existe no banco de dados
                self.cursor.execute('SELECT COUNT(*) FROM cartoes_cliente WHERE id_cartao = %s',
                                    (id_cartao,))
                if self.cursor.fetchone()[0] == 0:
                    break

            #Gerar um número aleatório para o atributo 'cript_num_cartao', que representa o número do cartão
            while True:
                #Gerar um número aleatório de 16 dígitos
                num_cartao = ''.join(random.choices(string.digits, k = 16))
                #Gerar o hash SHA-256 do número do cartão
                hash_num_cartao = hashlib.sha256(num_cartao.encode()).hexdigest()
                #Verificar se o número aleatório selecionado já existe no banco de dados
                self.cursor.execute('SELECT COUNT(*) FROM cartoes_cliente WHERE hash_num_cartao = %s',
                                        (hash_num_cartao,))
                if self.cursor.fetchone()[0] == 0:
                    break
                
            conta_id = id_conta
            data_validade = datetime.now().replace(year = datetime.now().year + 4)
            cod_seguranca = ''.join(random.choices(string.digits, k = 3)) #VARCHAR(3)
            status = 'ativo'
            tipo = 'débito' #Apenas débito
            data_emissao = datetime.now()
            pin = pin_cartao
            data_desativacao = None

            #Cadastrar as informações no banco de dados do PostgreSQL
            self.cursor.execute("""INSERT INTO cartoes_cliente 
                            (id_cartao, conta_id, data_validade, cript_cod_seguranca, status, tipo, data_emissao, cript_pin, data_desativacao, 
                            cript_num_cartao, hash_num_cartao)
                            VALUES 
                            (%s, %s, %s, pgp_sym_encrypt(%s, %s, 'cipher-algo=aes256'), %s, %s, %s, pgp_sym_encrypt(%s, %s, 'cipher-algo=aes256'), %s, pgp_sym_encrypt(%s, %s, 'cipher-algo=aes256'), %s)""",
                            (id_cartao, conta_id, data_validade, cod_seguranca, senha_conta, status, tipo, data_emissao, pin, senha_conta, data_desativacao, num_cartao, senha_conta, hash_num_cartao))
                
            #Salvando a operação no banco de dados
            self.conn.commit()

            return 1, "Conta criada com sucesso", conta_id, id_agencia, data_criacao
        except:
            self.conn.rollback()
            return 0, "Não foi possível criar a conta bancária"
        finally:
            self.__fechar_conexao_bd()
    
    def cadastro_agencia_bd(self,* ,id_agencia, nome , rua, cidade, estado):
        try:
            self.__conectar_bd() #Abre a conexão com o banco de dados
            self.cursor = self.conn.cursor() #Cria o cursor responsável pelas operações no banco de dados
            self.cursor.execute(
                """
                INSERT INTO agencia (id_agencia,
                                    nome,
                                    rua,
                                    cidade,
                                    estado)
                VALUES (%s, %s, %s ,%s ,%s )""",
                        (id_agencia, nome, rua, cidade, estado))
            self.conn.commit()
            return 1, "Agência registrada com sucesso"
        except:
            self.conn.rollback()
            return 0, "Não foi possível registrar a agência"
        finally:
            self.__fechar_conexao_bd()