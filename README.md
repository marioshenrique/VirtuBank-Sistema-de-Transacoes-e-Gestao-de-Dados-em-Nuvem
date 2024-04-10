# Sistema de Transações Simples

## Descrição
O projeto VirtuBank - Simulador Simples de Transações Bancárias é uma aplicação desktop desenvolvida com o intuito de simular operações bancárias básicas, como depósitos, saques, transferências, além de consulta de saldos e extratos. Este sistema foi criado como parte do meu processo de aprendizado pessoal em desenvolvimento de software, servindo como uma oportunidade prática para aplicar e demonstrar as habilidades e conhecimentos que venho adquirindo na área.

Este projeto abrange práticas de desenvolvimento de software, tais como construção de APIs, modelagem e implantação de bancos de dados, implementação de medidas de segurança em aplicações desktop, etc. Este repositório serve como uma vitrine dos métodos, técnicas e tecnologias com as quais venho me familiarizando, demonstrando meu empenho em construir soluções de software robustas, escaláveis e seguras.

As funcionalidades do sistema incluem:
- Realização de saques;
- Efetuação de depósitos;
- Execução de transferências entre contas;
- Consulta de saldos e informações detalhadas da conta;
- Acesso a extratos das transações efetuadas.

## Início Rápido
Este guia fornece instruções rápidas para começar a usar o sistema.
### Pré-requisitos
Antes de iniciar, certifique-se de ter os seguintes softwares instalados em seu sistema:
- Python (versão 3.10 ou superior)
- Visual Studio Code (ou outra IDE de preferência)
- Postman
- Git
- PostgreSQL (versão 12 ou superior)
### Instalação para Desenvolvimento
Siga os passos abaixo para configurar o ambiente e iniciar o projeto:

1. **Clonar o repositório**
Use o Git para clonar o repositório do projeto para o seu ambiente local. Abra um terminal e digite o seguinte comando:
'''bash
https://github.com/marioshenrique/simple_banking_transaction_system.git'''

2. **Configurar o ambiente virtual**
Navegue até a pasta do projeto clonado e crie um ambiente virtual Python para isolar as dependências do projeto. Execute dentro do terminal:
python -m venv venv
Ative o ambiente virtual com o comando:
cd simple_banking_transaction_system
.venv\Scripts\activate

3. **Instalar dependências**
Instale todas as dependências necessárias para o projeto usando o arquivo 'requirements.txt' fornecido dentro da pasta do projeto. Com o ambiente virtual ativado, execute o seguinte comando:

pip install -r requirements.txt

4. **Configurar variáveis de ambiente**
Copie o arquivo '.env.example' contido no diretório 'api' para um novo arquivo chamado '.env' e preencha-o com suas configurações locais.

5. **Reconstruir o banco de dados do PostgreSQL na máquina local**

PENDENTE

6. **Executar o projeto**
Após a instalação das dependências e configurações das variáveis de ambiente, o sistema está pronto para ser executado em um servidor local. Para isso, execute o seguinte comando no terminal:

uvicorn api.api_controller:app --reload    

## Uso
- Instruções detalhadas sobre como usar o sistema, incluindo exemplos de operações bancárias como saque, depósito, transferência, etc.
- Adicionar capturas de tela ou gifs demonstrando a utilização.

## Tecnologias Utilizadas
- Lista das principais tecnologias e bibliotecas utilizadas no projeto (FastAPI, SQLAlchemy, JWT, etc.)

## Estrutura do Projeto
### API Controller
- Descrição: explicar a função da API dentro do sistema, como ela é utilizada para manipular transações bancárias e autenticação de usuários.
- Endpoints Principais: Listar os principais endpoints disponíveis na API e uma breve descrição de sua funcionalidade.
- Tecnologias Utilizadas: Detalhar as tecnologias usadas na construção da API (FastAPI, SQLAlchemy, etc).

### Serviço de Autenticação (auth_service)
- Descrição: Descrever como o serviço de autenticação funciona para proteger as rotas da API e validar os usuários.
- Mecanismo de autenticação: Explicar o mecanismo de autenticação usado (tokem JWT).
- Dependências: Listar as bibliotecas e frameworks utilizados para autenticação.

### Serviço de Conta (account_service)
- Descrição: Descrever como o serviço de conta funciona.

### Serviço de Transações (transaction_service)
- Descrição: Descrever como o serviço de transações funciona.

### Camada de Dados (Data Layer)
- Descrição: Oferecer uma visão geral da camada de dados, explicando como ela interage com o banco de dados para realizar operações CRUD.
- Modelos de Dados: Descrever os modelos de dados usados.
- Repositórios: Explicar a função dos repositórios na abstração das operações do banco de dados.

### Interface do Usuário (UI)
- Descrição: Apresentar informações sobre a interface do usuário, como ela permite interações com o sistema de transações.
- Tecnologias Utilizadas: Detalhar as tecnologias e ferramentas usadas para desenvolver a UI (frameworks e bibliotecas de UI).

### Modelagem do Banco de Dados
#### Esquema do Banco de Dados
- Descrição: Fornecer uma visão geral do esquema do banco de dados, incluindo tabelas e relações entre elas.
- Diagrama ER: Incluir o diagrama Entidade-Relacionamento para ilustrar visualmente o esquema do banco de dados.

#### Modelos de Dados
- Descrição: Descrever os principais modelos de dados e suas funções no sistema. Explicar brevemente cada tabela, suas colunas principais, e como elas se relacionam com outras tabelas.

### Implantação do Banco de Dados
#### Ambiente de Desenvolvimento
- Configuração Local: Instruções sobre como configurar o banco de dados localmente para desenvolvimento e testes.
- Dados de Teste: Explicar como gerar dados de teste para o banco de dados de desenvolvimento.

#### Ambiente de Produção
- Provedor de banco de dados: mencionar o serviço de banco de dados usado na produção (Amazon RDS).

## Configuração
- Incluindo variáveis de ambiente e configurações do banco de dados.

##Autores e Reconhecimentos
- Créditos aos autores e colaboradores do projeto.
