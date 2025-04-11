# Estágio de construção
FROM python:3.12-slim as builder

WORKDIR /app

# Instala o Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==$POETRY_VERSION"

# Copia os arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala dependências do projeto
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Estágio final
FROM python:3.12-slim

WORKDIR ./love_live_songs_sentiment_classfier

RUN pip install fastapi[standard]

# Copia as dependências instaladas
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia a aplicação
COPY ./love_live_songs_sentiment_classfier ./app

# Porta da aplicação
EXPOSE 8000

# Comando de execução
# CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
CMD ["fastapi", "run", "app/main.py", "--port", "80"]