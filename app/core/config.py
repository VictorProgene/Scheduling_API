from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    secret_key_core: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Adicione isso logo abaixo da definição de 'settings'
print("DEBUG: Atributos carregados:", settings.model_dump().keys())