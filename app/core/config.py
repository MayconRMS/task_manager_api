from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()  # lê o .env

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")

    # Paginação
    DEFAULT_PAGE: int = Field(1, env="DEFAULT_PAGE")
    DEFAULT_SIZE: int = Field(10, env="DEFAULT_SIZE")

    # Database
    DATABASE_URL: str = Field("sqlite:///./app.db", env="DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()
