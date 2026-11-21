# Plano de Testes
## Projeto Rede Raízes do Nordeste

### 1. Objetivo
Esse plano de testes tem como finalidade verificar os seguintes itens:
O funcionamento da autenticação, a criação e consulta de pedidos, o processamento de pagamentos aprovados e recusados, as regras de autorização e o tratamento de erros e dados inválidos.

### 2. Ambiente de testes
Esses testes foram feitos no seguinte ambiente:
| Item | Configuração |
|---|---|
| Sistema operacional | Windows |
| Linguagem | Python 3.14.4 |
| Framework | FastAPI |
| Banco de dados | PostgreSQL |
| Ferramenta de testes | Postman |
| Servidor | Uvicorn |
| Endereço local | `http://127.0.0.1:8000` |
| Banco de testes | `raizes_nordeste_teste` |

### 3. Estratégia de testes
Os testes foram realizados utilizando o Postman e o Swagger, por meio de requisições HTTP aos endpoints da API. Também foram realizadas consultas diretamente no PostgreSQL para verificar a persistência dos dados e as alterações no estoque.

Foram executados testes positivos, para verificar o funcionamento esperado das funcionalidades, e testes negativos, para validar o tratamento de erros, dados inválidos, acessos não autorizados e situações de estoque insuficiente. Também foram utilizadas verificações automatizadas para conferir os códigos HTTP e o conteúdo das respostas.


### 4. Cenários de testes

| ID | Cenário | Tipo | Pré-condição | Endpoint | Entrada | Resultado esperado | Resultado obtido | Evidência |
|---|---|---|---|---|---|---|---|---|
| CT01 | Login do administrador com credenciais válidas | Positivo | Administrador cadastrado no banco | POST /auth/login | E-mail e senha válidos | HTTP 200 e token JWT | Aprovado: HTTP 200 e token JWT retornado | Postman: Login administrador / Evidencia_02_Login_JWT.png |
| CT02 | Consultar dados do usuário autenticado | Positivo | Token JWT válido | GET /auth/me | Token JWT no cabeçalho Authorization | HTTP 200 e dados do usuário | Aprovado: HTTP 200 e dados do usuário retornados | Postman: Consultar usuário autenticado |
| CT03 | Criar pedido com dados válidos | Positivo | Cliente, unidade e produtos cadastrados; token válido | POST /pedidos/ | Cliente, unidade, canal e itens válidos | HTTP 201 e pedido criado com valor total calculado | Aprovado: HTTP 201 e pedido criado com sucesso | Postman: Criar pedido / Evidencia_03_Criacao_Pedido.png |
| CT04 | Processar pagamento aprovado | Positivo | Pedido pendente e estoque disponível | POST /pedidos/{pedido_id}/pagamento | aprovado: true | HTTP 200, pagamento APROVADO e pedido PAGO | Aprovado: HTTP 200, pagamento APROVADO e pedido PAGO | Postman: Processar pagamento aprovado / Evidencia_04_Pagamento_Aprovado.png |
| CT05 | Criar pedido para processamento de pagamento recusado | Positivo | Cliente, unidade e produtos cadastrados; token válido | POST /pedidos/ | Dados válidos para criação do pedido | HTTP 201 e pedido com status PENDENTE | Aprovado: HTTP 201 e pedido criado com status PENDENTE | Postman: Criar pedido |
| CT06 | Processar pagamento recusado | Positivo | Pedido pendente | POST /pedidos/{pedido_id}/pagamento | aprovado: false | HTTP 200, pagamento RECUSADO e pedido PAGAMENTO_RECUSADO | Aprovado: HTTP 200, pagamento RECUSADO e pedido PAGAMENTO_RECUSADO | Postman: Processar pagamento recusado / Evidencia_05_Pagamento_Recusado.png |
| CT07 | Consultar lista de pedidos com autenticação | Positivo | Usuário autenticado com token válido | GET /pedidos/ | Token JWT no cabeçalho Authorization | HTTP 200 e lista de pedidos permitidos ao usuário | Aprovado: HTTP 200 e lista de pedidos retornada | Postman: Listar pedidos |
| CT08 | Consultar pedidos sem token de autenticação | Negativo | Nenhuma autenticação fornecida | GET /pedidos/ | Requisição sem token JWT | HTTP 401 e acesso negado | Aprovado: HTTP 401 e mensagem de erro padronizada | Postman: Consultar pedidos sem autenticação / Evidencia_06_Acesso_Sem_Autenticacao.png |
| CT09 | Tentar processar novamente um pagamento já realizado | Negativo | Pedido com pagamento já processado | POST /pedidos/{pedido_id}/pagamento | ID de pedido já processado e aprovado | HTTP 409 e processamento duplicado impedido | Aprovado: HTTP 409 e mensagem informando que o pedido não está pendente | Postman: Processar pagamento duplicado |
| CT10 | Criar pedido com quantidade inválida | Negativo | Token válido e produto cadastrado | POST /pedidos/ | Quantidade igual a zero ou inválida | HTTP 422 e erro de validação | Aprovado: HTTP 422 e erro de validação | Postman: Criar pedido - Quantidade inválida |
| CT11 | Criar pedido com produto inexistente | Negativo | Token válido | POST /pedidos/ | ID de produto inexistente | HTTP 404 e mensagem de produto não encontrado | Aprovado: HTTP 404 e mensagem de erro correspondente | Postman: Criar pedido - Produto inexistente |
| CT12 | Criar pedido com cliente inexistente | Negativo | Token válido e unidade cadastrada | POST /pedidos/ | ID de cliente inexistente | HTTP 404 e mensagem de cliente não encontrado | Aprovado: HTTP 404 e mensagem de erro correspondente | Postman: Criar pedido - Cliente inexistente |
| CT13 | Criar pedido com unidade inexistente | Negativo | Token válido e cliente cadastrado | POST /pedidos/ | ID de unidade inexistente | HTTP 404 e mensagem de unidade não encontrada | Aprovado: HTTP 404 e mensagem de erro correspondente | Postman: Criar pedido - Unidade inexistente |
| CT14 | Login do operador com credenciais válidas | Positivo | Operador cadastrado no banco | POST /auth/login | E-mail e senha válidos do operador | HTTP 200 e token JWT | Aprovado: HTTP 200 e token JWT retornado | Postman: Login operador |
| CT15 | Operador tentar processar pagamento de pedido de outra unidade | Negativo | Operador autenticado e pedido pertencente a outra unidade | POST /pedidos/{pedido_id}/pagamento | Token do operador e ID de pedido de outra unidade | HTTP 403 e operação impedida | Aprovado: HTTP 403 e mensagem de acesso não permitido | Postman: Pagamento de outra unidade / Evidencia_07_Controle_de_Permissao_403.png |
| CT16 | Criar pedido sem informar o cliente | Negativo | Token válido e demais dados da requisição preenchidos | POST /pedidos/ | Requisição sem o campo cliente_id | HTTP 422 e indicação de campo obrigatório | Aprovado: HTTP 422 e detalhe indicando Field required em cliente_id | Postman: Criar pedido - Campo obrigatório ausente / Evidencia_08 |
| CT17 | Administrador consultar pedidos filtrando pelo canal APP | Positivo | Administrador autenticado e pedidos de diferentes canais cadastrados | GET /pedidos/?canal_pedido=APP | Parâmetro canal_pedido=APP | HTTP 200 e somente pedidos do canal APP | Aprovado: consulta executada no Swagger e retornou somente pedidos do canal APP | Swagger: filtro por canal / Evidencia_09_filtro_por_canal.png |
| CT18 | Operador consultar pedidos filtrando pelo canal APP | Positivo | Operador autenticado e pedidos APP cadastrados em sua unidade | GET /pedidos/?canal_pedido=APP | Token do operador e parâmetro canal_pedido=APP | HTTP 200 e somente pedidos APP da unidade do operador | Aprovado: consulta executada no Swagger e retornou somente pedidos APP da unidade 1 | Swagger: consulta filtrada por canal e unidade |
| CT19 | Verificar isolamento por unidade durante a consulta filtrada | Negativo | Operador vinculado à unidade 1 e pedido APP cadastrado na unidade 2 | GET /pedidos/?canal_pedido=APP | Token do operador da unidade 1 e parâmetro canal_pedido=APP | Não retornar pedidos de outras unidades | Aprovado: pedido 13 da unidade 2 não apareceu na consulta do operador vinculado à unidade 1 | Swagger: verificação do isolamento por unidade |
| CT20 | Processar pagamento aprovado com estoque disponível | Positivo | Pedido pendente e estoque inicial de 20 unidades | POST /pedidos/{pedido_id}/pagamento | aprovado: true; pedido com 1 unidade do produto | HTTP 200, pedido PAGO e estoque reduzido em 1 unidade | Aprovado: HTTP 200 e estoque reduzido de 20 para 19 unidades | Postman: Processar pagamento aprovado |
| CT21 | Processar pagamento aprovado com estoque insuficiente | Negativo | Pedido pendente com quantidade solicitada superior ao estoque disponível | POST /pedidos/{pedido_id}/pagamento | aprovado: true; estoque do produto igual a zero | HTTP 409, pedido permanece PENDENTE e estoque não é alterado | Aprovado: HTTP 409, pedido permaneceu PENDENTE e estoque permaneceu em zero | Postman: Processar pagamento - Estoque insuficiente |