FROM python:3.12-slim as builder

WORKDIR /app

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

FROM python:3.12-slim

WORKDIR ./love_live_songs_sentiment_classfier

RUN pip install fastapi[standard]

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./love_live_songs_sentiment_classfier ./app

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
CMD ["fastapi", "run", "app/main.py", "--port", "80"]