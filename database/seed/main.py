from register import Cadastro

class CadastroBancario:
    """
    Classe responsável pelo cadastro de clientes e contas bancárias no sistema.

    Métodos:
    - cadastrar_cliente: Cadastra um novo cliente no banco de dados.
    - cadastro_conta_bancaria: Cadastra uma nova conta bancária para um cliente existente.
    """
    def __init__(self):
        self.cadastro = Cadastro()

    def cadastrar_cliente(self,* ,nome, data_nascimento, cpf, rg, telefone, email):
        """
        Cadastra um novo cliente no sistema.

        Parâmetros:
        - nome (str): Nome completo do cliente.
        - data_nascimento (str): Data de nascimento do cliente (YYYY-MM-DD).
        - cpf (str): CPF do cliente.
        - rg (str): RG do cliente.
        - telefone (str): Telefone de contato do cliente.
        - email (str): Endereço de email do cliente.

        Efeitos:
        - Cadastra o cliente no banco de dados se nãoe xistir um cliente com mesmo CPF ou RG.
        - Imprime uma mensagem de sucesso ou falha após a tentativa de cadastro.
        """

        response = self.cadastro.cadastrar_cliente_bd(cpf = cpf,
                                                      rg = rg,
                                                      nome = nome,
                                                      data_nascimento = data_nascimento,
                                                      telefone = telefone,
                                                      email = email)
        return response

    def cadastro_conta_bancaria(self,*,cpf, rg, id_agencia, tipo_conta, senha_conta, pin_cartao):
        """
        Cadastra uma nova conta para um cliente existente no sistema.

        Parâmetros:
        - cpf (str): CPF do cliente.
        - rg (str): RG do cliente.
        - id_agencia (str): Identificador da agência.
        - tipo_conta (str): Tipo de conta bancária (ex: corrente, poupança).
        - senha (str): Hash da senha da conta bancária.
        - pin_cartao (str): PIN do cartão físico associado à conta bancária.

        Efeitos:
        - Verifica a existência do cliente e da agência;
        - Cadastra a conta bancária e o cartão associado no banco de dados.
        - Imprime informações da conta bancária criada.
        """
        
        response = self.cadastro.cadastrar_conta_bancaria_bd(id_agencia,
                                                             cpf,
                                                             rg,
                                                             tipo_conta,
                                                             senha_conta,
                                                             pin_cartao)
        return response
    
    def cadastro_agencia(self,* ,id_agencia ,nome ,rua ,cidade ,estado):
        """
        Cadastra uma nova agência bancária no banco de dados do sistema.
        """
        response = self.cadastro.cadastro_agencia_bd(id_agencia = id_agencia,
                                                     nome = nome,
                                                     rua = rua,
                                                     cidade = cidade,
                                                     estado = estado)
        return response
