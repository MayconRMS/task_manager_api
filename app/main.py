from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.routers import auth, tasks
from app.core.logging_config import logger
from app.core.exceptions import validation_exception_handler, database_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="Tasks API",
    description="API para gerenciamento de tarefas com autenticação JWT",
    version="1.0.0",
)

# Configuração CORS (ajuste origins conforme frontend)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # api front 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Rota raiz apenas para teste
@app.get("/", summary="Raiz", tags=["health"])
def root():
    return {"status": "ok", "service": "tasks-api"}

# Criar tabelas automaticamente em dev (Alembic é recomendado para produção)
@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as exc:
        import logging
        logging.getLogger("uvicorn.error").warning("Falha ao criar tabelas: %s", exc)

# Middleware de logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Tratadores de exceções
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
