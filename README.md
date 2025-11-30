# Task Manager API

## 📌 Visão Geral

API para gerenciamento de tarefas com autenticação JWT, construída em FastAPI, SQLModel e banco de dados SQL. Permite CRUD completo de tarefas, cada usuário acessa apenas as suas.

------------------------------------------------------------------------

## 🚀 Tecnologias

- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn
- JWT (python-jose)
- Alembic
- SQLite (ou PostgreSQL/MySQL)
- Docker / Docker Compose (opcional)

------------------------------------------------------------------------

## ✔️​​ Requisitos

- Python 3.10+
- pip
- Virtualenv (opcional, mas recomendado)
- Banco de dados SQLite, PostgreSQL ou MySQL

## 📁 Estrutura do projeto

- app/main.py — inicia a aplicação, inclui os routers, configura CORS e inicializa o DB (opcional).

- app/database.py — engine + sessão (SessionLocal) + função create_db_and_tables() se usar SQLModel.

- app/core/config.py — configurações (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL).

- app/core/security.py — hash_password, verify_password, create_access_token, decode_token.

- app/models/ — modelos SQLModel (User, Task).

- app/schemas/ — Pydantic/SQLModel schemas de entrada e saída.

- app/routers/auth.py — endpoints: register, login, me.

- app/routers/tasks.py — CRUD de tasks, todos protegidos por autenticação.

- app/services/ — regras de negócio, chamadas pelos routers (boa prática tipo “service layer”).

- alembic/ — configurado apontando para SQLModel.metadata no env.py.

------------------------------------------------------------------------

## 🔧 Como rodar o projeto

### 1️⃣ Criar e ativar o ambiente virtual

##### Windows
``` bash
python -m venv venv
venv\Scripts\activate
```

##### Linux/Mac
``` bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar dependências

``` bash
python -m pip install --upgrade pip
```

``` bash
pip install fastapi "uvicorn[standard]" sqlmodel alembic passlib argon2_cffi pyjwt python-dotenv pydantic-settings
```

#### Descrição das dependências

- **FastAPI** — Framework principal da API — rápido, tipado e moderno.
- **Uvicorn** — Servidor ASGI para rodar a aplicação FastAPI no modo desenvolvimento.
- **SQLModel** — ORM/ODM baseado em SQLAlchemy + Pydantic. Facilita trabalhar com modelos e tabelas.
- **SQLAlchemy** — Base usada pelo SQLModel para gerenciar consultas, conexões e transações no banco.
- **Alembic** — Gerenciador de migrações do banco de dados.
- **Passlib** — Hash e verificação segura de senhas.
- **argon2-cffi** — Backend utilizado pelo Passlib para realizar hashing de senhas com Argon2.
- **PyJWT** — Usado para gerar e validar tokens JWT na autenticação.
- **python-dotenv** — Permite carregar variáveis sensíveis (como SECRET_KEY) a partir do arquivo .env.
- **pydantic-settings** — Gerencia configurações do projeto usando variáveis de ambiente, substituindo o antigo BaseSettings do Pydantic.

### 3️⃣ Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto com:
``` bash
SECRET_KEY=uma_chave_secreta_aqui
DATABASE_URL=sqlite:///./database.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### 4️⃣ Criar o banco de dados
Automaticamente via script:
``` bash
python app/init_db.py
```

Ou via migrations Alembic:
``` bash
# Gerar migration após alterar modelos
alembic revision --autogenerate -m "Mensagem da migration"

# Aplicar migrations no banco
alembic upgrade head

```

### 5️⃣ Rodar o servidor

``` bash
venv\Scripts\activate
uvicorn app.main:app --reload
```

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### 6️⃣ Encerrar o ambiente virtual
``` bash
deactivate
```

### 7️⃣ (Opcional) Docker
``` bash
docker-compose up --build
```

------------------------------------------------------------------------

## 🔑 Autenticação

A API usa **JWT Bearer Token**.

### Criar usuário

POST: `/auth/register`

Exemplo: 
``` json
{
  "name": "Maycon",
  "email": "maycon@example.com",
  "password": "123456"
}
``` 

### Login

POST: `/auth/login`\
Exemplo: 

``` json
{
  "email": "maycon@example.com",
  "password": "123456"
}

```
Resposta: 

``` json
{
  "access_token": "seu_token",
  "token_type": "bearer",
}

```

### Usuário autenticado

GET: `/auth/me`\
Requer Header:

    Authorization: Bearer SEU_TOKEN

------------------------------------------------------------------------

## 🗂️ Rotas de Tarefas

Todas **EXIGEM autenticação**.

##### POST /tasks/ — Criar tarefa
Exemplo payload:

``` json
{
  "title": "Comprar leite",
  "description": "Ir ao mercado comprar leite",
  "status": "pendente"
}
``` 


##### GET /tasks/ — Listar tarefas
Suporta filtros opcionais:

``` json
/tasks/?status=pendente&page=1&size=10
``` 

##### GET /tasks/{id} — Detalhar tarefa

##### PUT /tasks/{id} — Atualizar tarefa
Exemplo payload:

``` json
{
  "title": "Comprar leite e pão",
  "status": "concluido"
}
``` 

Atualiza completed_at automaticamente se status for concluido.

##### DELETE /tasks/{id} — Remover tarefa

------------------------------------------------------------------------

## 🧪 Acessar a documentação

-   Swagger: `http://localhost:8000/docs`
-   Redoc: `http://localhost:8000/redoc`

------------------------------------------------------------------------

## 📊 Paginação e filtros (opcional)

- Query params para GET /tasks/:

- - page — Página (padrão 1)
- - size — Itens por página (padrão 10)
- - status — Filtrar por status (pendente, em_andamento, concluido)

------------------------------------------------------------------------
## ⚠️ Tratamento de erros

- Erros de validação: 422 Unprocessable Entity
- Usuário não autenticado: 401 Unauthorized
- Tarefa não encontrada: 404 Not Found
- Erros de banco: 500 Internal Server Error

------------------------------------------------------------------------
## 📝 Autor

Projeto desenvolvido por **Maycon Ricardo Monteiro**.