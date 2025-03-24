from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database settings
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    # redis settings
    CACHE_HOST: str
    CACHE_PORT: str
    ACCESS_TOKEN_EXPIRE: int
    # jwt settings
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings


settings = get_settings()
