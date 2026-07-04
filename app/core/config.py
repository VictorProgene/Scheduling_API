"""
config.py - Gerenciamento de Configurações e Variáveis de Ambiente

Este arquivo define a estrutura de configurações globais do aplicativo utilizando Pydantic Settings.
Sua função é:
1. Ler e carregar dinamicamente as variáveis de ambiente declaradas no arquivo `.env`.
2. Validar que as configurações fundamentais (como URL do banco e chaves de segurança) existam.
3. Disponibilizar a instância global 'settings' para o resto da aplicação.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    secret_key_core: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Adicione isso logo abaixo da definição de 'settings'
print("DEBUG: Atributos carregados:", settings.model_dump().keys())