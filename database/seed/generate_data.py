from main import CadastroBancario
from faker import Faker
import random

fake = Faker('pt_BR')

num_registros = 20
cpf_rg_cliente_list = []

"Popular a tabela 'CLIENTE' para testes"
for _ in range(num_registros):

    nome = str(fake.name())
    data_nascimento = fake.date_of_birth(minimum_age = 18, maximum_age = 70).strftime('%Y-%m-%d')
    cpf = fake.cpf().replace('.', '').replace('-', '')
    rg = fake.rg().replace('.', '').replace('-', '')
    telefone = '829' + fake.msisdn()[3:11]
    email = fake.email()

    response = CadastroBancario().cadastrar_cliente(nome = nome,
                                                  data_nascimento = data_nascimento,
                                                  cpf = cpf,
                                                  rg = rg,
                                                  telefone = telefone,
                                                  email = email)
    print(response)
    if response[0] == 1:
        cpf_rg_cliente_list.append((cpf, rg))
    else:
        pass
"Popular a tabela 'AGENCIA' para testes"

agencias_list = []

#agência 1
response = CadastroBancario().cadastro_agencia(id_agencia = '739567',
                                               nome = 'Agência Metropolitana',
                                               rua = 'Av. Rotary',
                                               cidade = 'Campo Grande',
                                               estado = 'AL')
agencias_list.append('739567')
print(response)

#agência 2
response = CadastroBancario().cadastro_agencia(id_agencia = '128563',
                                               nome = 'Agência I',
                                               rua = 'Av. Duarte de Barros',
                                               cidade = 'Belo Jardim',
                                               estado = 'PE')
agencias_list.append('128563')
print(response)

#agência 3
response = CadastroBancario().cadastro_agencia(id_agencia = '962957',
                                               nome = 'Agência II',
                                               rua = 'Rua dos Marechais',
                                               cidade = 'Campo Grande',
                                               estado = 'AL')
agencias_list.append('962957')
print(response)

#agência 4
response = CadastroBancario().cadastro_agencia(id_agencia = '834395',
                                               nome = 'Agência III',
                                               rua = 'Rod. BR104',
                                               cidade = 'Agrestina',
                                               estado = 'PE')
print(response)

"Popular a tabela 'CONTA_BANCARIA' para testes"
for item in cpf_rg_cliente_list:
    id_agencia = random.choice(agencias_list)
    response = CadastroBancario().cadastro_conta_bancaria(cpf = item[0],
                                                          rg = item[1],
                                                          id_agencia = id_agencia,
                                                          tipo_conta = 'corrente',
                                                          senha_conta = 'senha1234',
                                                          pin_cartao = '999999')
    print(response)

