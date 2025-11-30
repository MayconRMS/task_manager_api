import os
from sqlmodel import SQLModel, create_engine, Session

DB_FILE = os.path.join("data", "database.db")

os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Cria tabelas automaticamente (apenas no início)
def init_db():
    from app.models.user import User  
    SQLModel.metadata.create_all(engine)
