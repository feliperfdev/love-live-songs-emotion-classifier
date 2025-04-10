# API - Classificador de emoção em título das músicas de Love Live

Modelo e API desenvolvidos para fins de estudos acadêmicos e profissionais.

Modelo de classificação de sentimentos utilizando Logistic Regression e NLTK para títulos de músicas dos grupos da franquia "[Love Live!](https://pt.wikipedia.org/wiki/Love_Live!)" (Muses, Aquors, Nijigaku e Liella).

## Desenvolvimento

O algoritmo desenvolvido está disponível [**neste repositório**](https://github.com/feliperfdev/AI-ML-Studies/tree/main/day_05).

Tecnologias e modelos utilizados:

- Python 3.12
- NLTK para tokenização e análise de sentimentos
- Algoritmo de Regressão Logística ([Logistic Regression - Sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html))
- FastAPI e Uvicorn para desenvolvimento da API
- Pickle para exportação e importação do modelo treinado
- NumPy para manipulação algébrica
- Pandas para manipulação de datasets
- Docker para conteinerização

## Como utilizar

```sh
docker build -t fastapi-app .
```

```sh
docker run -d --name {container-name} -p 80:80 fastapi-app
```

## Acessando

1. [GET] Documentação

```sh
http://localhost/docs
```

---

2. [POST] Classificação de título da música

```sh
http://localhost/song?song="song name"
```

Resposta

```json
{
  "sentiment": "EXCITING | NORMAL"
}
```

---
