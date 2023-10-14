from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings
    """
    model_config = SettingsConfigDict(
        env_file='../../.env-dev',
        extra='allow'
    )
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
