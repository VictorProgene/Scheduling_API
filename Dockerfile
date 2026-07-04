# 1. Imagem base oficial do Python em versão leve (slim)
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /workspace

# 3. Instala dependências do sistema necessárias para compilar pacotes (como psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código da aplicação e arquivos de migração
COPY app/ ./app
COPY alembic/ ./alembic
COPY alembic.ini .

# 6. Expõe a porta interna da aplicação
EXPOSE 8000

# 7. Executa as migrações pendentes do Alembic e inicia o servidor Uvicorn
CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"