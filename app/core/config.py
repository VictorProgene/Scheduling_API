from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    # Isso diz ao Pydantic para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()