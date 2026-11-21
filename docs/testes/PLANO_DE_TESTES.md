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
Os testes foram realizados utilizando o Postman, por meio de requisições HTTP aos endpoints da API. Foram executados testes positivos, para verificar o funcionamento esperado das funcionalidades, e testes negativos, para validar o tratamento de erros, dados inválidos e acessos não autorizados. Também foram utilizadas verificações automatizadas para conferir os códigos HTTP e o conteúdo das respostas.

### 4. Cenários de testes

| ID | Cenário | Tipo | Endpoint | Resultado esperado | Resultado obtido |
|---|---|---|---|---|---|
| CT01 | Login do administrador com credenciais válidas | Positivo | POST /auth/login | Retornar HTTP 200 e um token JWT | Aprovado: HTTP 200 e token JWT retornado |
| CT02 | Consultar dados do usuário autenticado | Positivo | GET /auth/me | Retornar HTTP 200 e os dados do usuário autenticado | Aprovado: HTTP 200 e dados do usuário retornados |
| CT03 | Criar pedido com dados válidos | Positivo | POST /pedidos/ | Retornar HTTP 201 e os dados do pedido criado, com valor total calculado | Aprovado: HTTP 201 e pedido criado com sucesso |
| CT04 | Processar pagamento aprovado | Positivo | POST /pedidos/{pedido_id}/pagamento | Retornar HTTP 200, registrar pagamento como APROVADO e atualizar pedido para PAGO | Aprovado: HTTP 200, pagamento APROVADO e pedido PAGO |
| CT05 | Criar pedido para processamento de pagamento recusado | Positivo | POST /pedidos/ | Retornar HTTP 201 e criar o pedido com status PENDENTE | Aprovado: HTTP 201 e pedido criado com status PENDENTE |
| CT06 | Processar pagamento recusado | Positivo | POST /pedidos/{pedido_id}/pagamento | Retornar HTTP 200, registrar pagamento como RECUSADO e atualizar pedido para PAGAMENTO_RECUSADO | Aprovado: HTTP 200, pagamento RECUSADO e pedido PAGAMENTO_RECUSADO |
| CT07 | Consultar lista de pedidos com autenticação | Positivo | GET /pedidos/ | Retornar HTTP 200 e a lista de pedidos permitidos ao usuário | Aprovado: HTTP 200 e lista de pedidos retornada |
| CT08 | Consultar pedidos sem token de autenticação | Negativo | GET /pedidos/ | Retornar HTTP 401 e impedir o acesso aos pedidos | Aprovado: HTTP 401 e mensagem de erro padronizada |
| CT09 | Tentar processar novamente um pagamento já realizado | Negativo | POST /pedidos/{pedido_id}/pagamento | Retornar HTTP 409 e impedir o processamento duplicado | Aprovado: HTTP 409 e mensagem informando que o pedido não está pendente |
| CT10 | Criar pedido com quantidade inválida | Negativo | POST /pedidos/ | Retornar HTTP 422 e informar que os dados enviados são inválidos | Aprovado: HTTP 422 e erro de validação |
| CT11 | Criar pedido com produto inexistente | Negativo | POST /pedidos/ | Retornar HTTP 404 e informar que o produto não foi encontrado | Aprovado: HTTP 404 e mensagem de erro correspondente |
| CT12 | Criar pedido com cliente inexistente | Negativo | POST /pedidos/ | Retornar HTTP 404 e informar que o cliente não foi encontrado | Aprovado: HTTP 404 e mensagem de erro correspondente |
| CT13 | Criar pedido com unidade inexistente | Negativo | POST /pedidos/ | Retornar HTTP 404 e informar que a unidade não foi encontrada | Aprovado: HTTP 404 e mensagem de erro correspondente |
| CT14 | Login do operador com credenciais válidas | Positivo | POST /auth/login | Retornar HTTP 200 e um token JWT | Aprovado: HTTP 200 e token JWT retornado |
| CT15 | Operador tentar processar pagamento de pedido de outra unidade | Negativo | POST /pedidos/{pedido_id}/pagamento | Retornar HTTP 403 e impedir a operação | Aprovado: HTTP 403 e mensagem de acesso não permitido |
| CT16 | Criar pedido sem informar o cliente | Negativo | POST /pedidos/ | Retornar HTTP 422 e informar que o campo cliente_id é obrigatório | Aprovado: HTTP 422 e detalhe indicando Field required em cliente_id |
| CT17 | Administrador consultar pedidos filtrando pelo canal APP | Positivo | GET /pedidos/?canal_pedido=APP | Retornar HTTP 200 e somente pedidos cujo canal_pedido seja APP | Aprovado: consulta executada no Swagger e retornou somente pedidos do canal APP |
| CT18 | Operador consultar pedidos filtrando pelo canal APP | Positivo | GET /pedidos/?canal_pedido=APP | Retornar HTTP 200 e somente pedidos do canal APP pertencentes à unidade do operador | Aprovado: consulta executada no Swagger e retornou somente pedidos APP da unidade 1 |
| CT19 | Verificar isolamento por unidade durante a consulta filtrada | Negativo | GET /pedidos/?canal_pedido=APP | Não retornar pedidos de outras unidades, mesmo que correspondam ao canal informado | Aprovado: pedido 13 da unidade 2 não apareceu na consulta do operador vinculado à unidade 1 |