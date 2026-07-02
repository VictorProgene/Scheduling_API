from sqlmodel import create_engine, Session
from app.core.config import settings

# Agora ele lê dinamicamente o que está no seu .env (porta 5432)
engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session