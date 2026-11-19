# Rede Raízes do Nordeste - API

## 1. Sobre o projeto

A Rede Raízes do Nordeste é um projeto acadêmico que consiste no desenvolvimento de uma API REST para apoiar o gerenciamento das operações de uma rede de estabelecimentos gastronômicos.

A aplicação foi desenvolvida com o objetivo de organizar o processamento de pedidos, permitindo trabalhar com informações de clientes, unidades, produtos e pagamentos simulados. Também foram implementados mecanismos de autenticação, controle de permissões e registro de auditoria, contribuindo para a segurança e a organização das operações.

O projeto faz parte da disciplina Eletiva IV - Projeto Multidisciplinar de Análise e Desenvolvimento de Sistemas, do curso de Análise e Desenvolvimento de Sistemas da Uninter.

## 2. Objetivos do projeto

O principal objetivo é desenvolver uma API capaz de representar o fluxo de processamento de pedidos da Rede Raízes do Nordeste, desde sua criação até a confirmação ou recusa do pagamento.

A solução busca garantir a integridade das informações, organizar o acesso aos recursos e aplicar regras de negócio durante as operações.

### 2.1. Funcionalidades principais

A API contempla as seguintes funcionalidades:

- Utilização de dados de clientes, unidades e produtos cadastrados inicialmente por meio de scripts.
- Criação e consulta de pedidos.
- Cálculo automático do valor total de cada pedido.
- Simulação do processamento de pagamentos, com possibilidade de aprovação ou recusa.
- Atualização do status do pedido conforme o resultado do pagamento.
- Autenticação de usuários por meio de tokens JWT.
- Controle de acesso conforme o perfil do usuário e sua unidade de vinculação.
- Registro de operações relevantes para fins de auditoria.

### 2.2. Fluxo principal implementado

O fluxo escolhido para o desenvolvimento foi o processamento de pedidos, seguindo as etapas:

1. O usuário autenticado solicita a criação de um pedido, informando o cliente, a unidade e os produtos desejados.
2. A API verifica as informações recebidas e valida os dados necessários.
3. O valor total do pedido é calculado automaticamente com base nos produtos e nas respectivas quantidades.
4. O pagamento é processado de forma simulada.
5. Conforme o resultado do pagamento, o status do pedido é atualizado.

Os resultados possíveis são:

- Pagamento aprovado: o pedido recebe o status `PAGO`.
- Pagamento recusado: o pedido recebe o status `PAGAMENTO_RECUSADO`.

## 3. Tecnologias utilizadas

Para o desenvolvimento da aplicação, foram utilizadas as seguintes tecnologias:

| Tecnologia | Finalidade |
|---|---|
| Python 3.14 | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| PostgreSQL | Gerenciamento do banco de dados relacional |
| SQLAlchemy | Mapeamento objeto-relacional (ORM) |
| Alembic | Controle e execução de migrações do banco |
| Pydantic | Validação dos dados de entrada e saída |
| PyJWT | Geração e validação de tokens JWT |
| Argon2 | Proteção de senhas por meio de hash |
| Uvicorn | Servidor ASGI para execução da API |
| Postman | Testes e validação dos endpoints |
| Git e GitHub | Versionamento e hospedagem do código-fonte |

## 4. Arquitetura do projeto

A aplicação foi organizada em diretórios que separam as responsabilidades relacionadas às rotas da API, à validação dos dados e à infraestrutura.

Essa organização facilita a manutenção do código e permite localizar mais facilmente os componentes responsáveis por cada funcionalidade.

### 4.1. Estrutura de diretórios

```text
raizes-nordeste-api/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── pedidos.py
│   │   └── __init__.py
│   │
│   ├── application/
│   │   └── __init__.py
│   │
│   ├── domain/
│   │   └── __init__.py
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── security.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── pedido.py
│   │
│   └── __init__.py
│
├── docs/
│   └── postman/
│       ├── Rede Raízes - Exemplo.postman_environment.json
│       └── Rede Raízes do Nordeste API.postman_collection.json
│
├── migrations/
│   ├── versions/
│   │   └── 46c96f82e7ee_criacao_inicial_das_tabelas.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── criar_admin.py
├── criar_clientes.py
├── criar_operador.py
├── criar_produtos.py
├── criar_unidades.py
├── main.py
├── seed.py
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
Observação: o `.env` real não aparece na árvore documentada porque não deve ser enviado ao GitHub.

### 4.2. Organização dos componentes

A estrutura do projeto foi organizada em diretórios para separar as responsabilidades e facilitar a manutenção da aplicação.

Cada diretório possui uma finalidade específica:

- API: reúne as rotas responsáveis por receber as requisições e disponibilizar as funcionalidades da aplicação.
- Schemas: contém os modelos utilizados para validar e estruturar os dados recebidos e enviados pela API.
- Infrastructure: concentra os componentes responsáveis pela conexão com o banco de dados, definição dos modelos, segurança e registros de auditoria.
- Migrations: armazena os arquivos utilizados para controlar as alterações na estrutura do banco de dados.
- Application e Domain: são diretórios preparados para uma possível expansão da arquitetura, mas ainda não possuem funcionalidades implementadas.
- Scripts de inicialização: permitem cadastrar os dados iniciais e criar os usuários necessários para utilizar o sistema.

## 5. Requisitos para instalação

Antes de executar o projeto, é necessário possuir:

- Python 3.14 instalado.
- PostgreSQL instalado e em execução.
- Git instalado.
- Acesso ao terminal ou PowerShell.
- Um ambiente virtual Python para instalação das dependências.

### 5.1. Ferramentas recomendadas

As ferramentas abaixo podem facilitar o desenvolvimento e a administração do projeto:

- PyCharm ou Visual Studio Code para edição do código.
- pgAdmin para gerenciamento do PostgreSQL.
- Postman para execução e validação das requisições da API.

## 6. Instalação

### 6.1. Clonar o repositório

Primeiramente, clone o repositório do projeto:

```bash
git clone https://github.com/Selomar/raizes-nordeste-api.git
cd raizes-nordeste-api
```

### 6.2. Criar o ambiente virtual

Na raiz do projeto, execute:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

### 6.3. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
pip install -r requirements.txt
```

Esse comando instala as bibliotecas necessárias para executar a aplicação.

## 7. Configuração do banco de dados

O projeto utiliza o PostgreSQL como sistema gerenciador de banco de dados.

### 7.1. Criar o banco

No PostgreSQL, crie um banco de dados com o seguinte nome:

`raizes_nordeste`

### 7.2. Configurar as variáveis de ambiente

Na raiz do projeto, crie um arquivo chamado `.env`, utilizando o arquivo `.env.example` como referência.

Preencha as variáveis de acordo com a configuração do PostgreSQL instalado na máquina:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=raizes_nordeste
DB_USER=postgres
DB_PASSWORD=sua_senha_do_postgresql

SECRET_KEY=sua_chave_secreta
```

Algumas informações importantes:

- `DB_HOST`: endereço do servidor do banco de dados.
- `DB_PORT`: porta utilizada pelo PostgreSQL.
- `DB_NAME`: nome do banco de dados.
- `DB_USER`: usuário utilizado para acessar o PostgreSQL.
- `DB_PASSWORD`: senha do usuário do banco.
- `SECRET_KEY`: chave utilizada na geração e validação dos tokens JWT.

Substitua os valores de exemplo pelas configurações do seu ambiente.

Atenção: o arquivo `.env` contém informações sensíveis e não deve ser compartilhado nem enviado ao GitHub. Ele já está incluído no arquivo `.gitignore`.

## 8. Migrações e dados iniciais

Depois de configurar o banco de dados, é necessário criar as tabelas e inserir os dados iniciais utilizados pela aplicação.

Todos os comandos desta seção devem ser executados na raiz do projeto, com o ambiente virtual ativado.

### 8.1. Criar as tabelas

Execute:

```bash
alembic upgrade head
```

Esse comando aplica as migrações disponíveis e cria a estrutura necessária no banco de dados.

### 8.2. Cadastrar os dados iniciais

Execute:

```bash
python seed.py
```

O script realiza o cadastro inicial das unidades, dos produtos e dos clientes utilizados no sistema.

### 8.3. Criar o usuário administrador

Execute:

```bash
python criar_admin.py
```

O terminal solicitará as informações necessárias para cadastrar o usuário administrador.

### 8.4. Criar um usuário operador

Execute:

```bash
python criar_operador.py
```

Informe os dados solicitados, incluindo o identificador da unidade à qual o operador ficará vinculado.

Observação: os scripts de criação de usuários solicitam as senhas durante a execução. As senhas são armazenadas no banco de dados em formato de hash, utilizando Argon2.

## 9. Executando a aplicação

Com o ambiente virtual ativado e o banco de dados configurado, inicie a API com o comando:

```bash
uvicorn main:app --reload
```

Por padrão, a aplicação ficará disponível no endereço:

`http://127.0.0.1:8000`

### 9.1. Documentação interativa (Swagger)

Para visualizar e testar os endpoints da API, acesse:

`http://127.0.0.1:8000/docs`

A documentação interativa permite consultar as rotas disponíveis, visualizar os parâmetros necessários e executar requisições diretamente pelo navegador.

### 9.2. Documentação alternativa (ReDoc)

Também é possível consultar a documentação por meio do ReDoc:

`http://127.0.0.1:8000/redoc`

Para encerrar a execução da aplicação, pressione `Ctrl + C` no terminal.

## 10. Endpoints disponíveis

A API disponibiliza os seguintes endpoints principais:

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| POST | `/auth/login` | Realiza o login e retorna o token JWT | Não |
| GET | `/auth/me` | Consulta os dados do usuário autenticado | Sim |
| GET | `/pedidos/` | Lista os pedidos conforme as permissões do usuário | Sim |
| POST | `/pedidos/` | Cria um novo pedido | Sim |
| POST | `/pedidos/{pedido_id}/pagamento` | Processa o pagamento simulado e atualiza o status do pedido | Sim |

### 10.1. Autenticação

As rotas protegidas utilizam autenticação por token JWT.

Para acessar essas funcionalidades, o usuário deve primeiro realizar o login por meio da rota:

`POST /auth/login`

Após receber o token, deverá enviá-lo nas requisições protegidas utilizando o cabeçalho HTTP:

`Authorization: Bearer SEU_TOKEN`

O token possui um prazo de validade definido pela aplicação. Após sua expiração, será necessário realizar um novo login.

### 10.2. Perfis de acesso

O sistema possui dois perfis de usuário:

**ADMIN**

Possui acesso administrativo e pode consultar pedidos de todas as unidades.

**OPERADOR**

Possui acesso restrito à unidade à qual está vinculado. As operações realizadas pelo operador devem respeitar essa limitação.

As permissões são verificadas pela API durante a execução das operações.

## 11. Testes da API com Postman

Para validar o funcionamento da aplicação, foi desenvolvida uma coleção de testes no Postman. Ela reúne requisições que verificam os principais fluxos do sistema, incluindo autenticação, criação de pedidos, processamento de pagamentos e controle de permissões.

### 11.1. Arquivos da coleção

Os arquivos necessários para executar os testes estão disponíveis no diretório `docs/postman/`:

- `Rede Raízes do Nordeste API.postman_collection.json`: contém as requisições e os testes automatizados da API.
- `Rede Raízes - Exemplo.postman_environment.json`: contém as configurações necessárias para executar os testes no ambiente local.

### 11.2. Como executar os testes

Para executar os testes em um ambiente preparado para essa finalidade, siga as etapas abaixo:

1. Instale e inicie o PostgreSQL.
2. Crie um banco de dados separado para os testes.
3. Configure o arquivo `.env` para utilizar esse banco.
4. Execute as migrações com `alembic upgrade head`.
5. Cadastre os dados iniciais com `python seed.py`.
6. Crie um usuário administrador com `python criar_admin.py`.
7. Crie um usuário operador com `python criar_operador.py`.
8. Durante a criação do operador, informe o ID de uma unidade existente no banco de dados. Esse vínculo será utilizado pela aplicação para controlar as permissões de acesso aos pedidos de cada unidade.
9. Inicie a API com `uvicorn main:app --reload`.
10. Importe a coleção e o ambiente JSON no Postman.
11. Selecione o ambiente `Rede Raízes - Exemplo`.
12. Execute a coleção utilizando o Collection Runner.

A utilização de um banco separado permite realizar os testes sem interferir nos dados de outras instalações da aplicação.

**Preparação das credenciais de teste:** durante a criação dos usuários, utilize o mesmo e-mail e a mesma senha configurados nas requisições de login da coleção do Postman. Dessa forma, os testes de autenticação poderão ser executados em uma instalação nova sem depender dos usuários cadastrados anteriormente no ambiente de desenvolvimento.

### 11.3. Cenários validados

A coleção contempla testes relacionados a:

- Autenticação e consulta do usuário autenticado.
- Criação e consulta de pedidos.
- Aprovação e recusa de pagamentos.
- Tentativa de processamento duplicado de pagamento.
- Envio de dados inválidos.
- Consulta de produtos, clientes e unidades inexistentes.
- Bloqueio de acesso sem autenticação.
- Restrição de permissões entre perfis e unidades.

Durante o desenvolvimento, foi realizada uma execução da coleção que apresentou o seguinte resultado:

**42 testes aprovados e nenhum teste reprovado.**

Os testes devem ser executados com a API conectada a um banco de dados de teste ou a uma base preparada especificamente para essa finalidade, evitando alterações indesejadas nos dados utilizados em outros ambientes.

## 12. Segurança e proteção de dados

A segurança foi considerada durante o desenvolvimento da aplicação, principalmente no controle de acesso aos recursos e na proteção das informações armazenadas.

### 12.1. Autenticação e autorização

Foram implementados os seguintes mecanismos:

- Autenticação de usuários por meio de tokens JWT.
- Armazenamento de senhas utilizando hash com Argon2.
- Tokens com tempo de validade definido.
- Controle de acesso baseado nos perfis ADMIN e OPERADOR.
- Restrição de acesso dos operadores aos pedidos de suas respectivas unidades.

### 12.2. Proteção das informações

A aplicação também utiliza medidas para reduzir a exposição de informações sensíveis:

- Validação dos dados recebidos pela API.
- Utilização de variáveis de ambiente para armazenar configurações sensíveis.
- Exclusão do arquivo `.env` do controle de versão por meio do `.gitignore`.
- Respostas estruturadas para apresentar erros sem expor informações internas desnecessárias.

### 12.3. Auditoria

O sistema possui registros de auditoria para acompanhar operações relevantes realizadas durante sua utilização.

Entre as informações armazenadas estão:

- Usuário responsável pela operação, quando identificado.
- Ação executada.
- Entidade afetada.
- Identificador do registro.
- Resultado da operação.
- Data e horário do registro.

Esses registros auxiliam no acompanhamento das atividades e permitem consultar informações importantes sobre as operações realizadas na aplicação.

## 13. Considerações finais

O desenvolvimento da API permitiu aplicar conhecimentos relacionados à construção de aplicações back-end, integração com banco de dados relacional, organização de código, autenticação, controle de permissões e testes de software.

A implementação priorizou o fluxo de processamento de pedidos, contemplando a criação, a validação das informações, a simulação de pagamento e a atualização do status.

Com isso, o projeto apresenta uma solução funcional para o fluxo escolhido, além de uma estrutura que permite compreender e reproduzir o funcionamento da aplicação em um ambiente local.