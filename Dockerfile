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
    && poetry install --no-root --without dev

# Estágio final
FROM python:3.12-slim

WORKDIR /app

# Copia as dependências instaladas
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia a aplicação
COPY ./app ./app

# Porta da aplicação
EXPOSE 8000

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]