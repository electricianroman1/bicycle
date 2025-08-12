from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://mongo:27017"
    MONGO_DB: str = "dnd"
    API_PREFIX: str = "/api/v1"

    JWT_SECRET: str = "replace_with_strong_secret"  # переопределять через env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # время жизни токена в минутах

    class Config:
        env_file = ".env"

settings = Settings()