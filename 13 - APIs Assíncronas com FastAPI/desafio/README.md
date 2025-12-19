======== Desafio: API Bancária Assíncrona com FastAPI ======== 

Este projeto consiste em uma API RESTful assíncrona desenvolvida com FastAPI para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Ele utiliza autenticação via JWT e segue boas práticas de desenvolvimento de APIs modernas.

🔹 Funcionalidades

- Cadastro de contas: Criação de contas bancárias com saldo inicial.

- Cadastro de transações: Registro de depósitos e saques vinculados a contas.

- Exibição de extrato: Consulta de todas as transações de uma conta específica.

- Validação de saldo: Impede saques que excedam o saldo disponível.

- Autenticação JWT: Apenas usuários autenticados podem acessar endpoints protegidos.

- Documentação automática: API documentada via OpenAPI (Swagger).

🔹 Tecnologias Utilizadas

Python 3.11

- FastAPI (Framework web assíncrono)

- Databases + SQLAlchemy (Banco de dados e ORM)

- SQLite (banco de dados para desenvolvimento)

- Pydantic (Validação e schemas)

- Uvicorn (Servidor ASGI)

- JWT (Autenticação de usuário)