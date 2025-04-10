from fastapi import FastAPI  
import pandas as pd

import pickle

app = FastAPI()


@app.get("/") 
async def main_route():     
  
  return {"message": "API Tested OK"}

@app.post("/song") 
async def classifySongSentiment(song: str):
  from sklearn.feature_extraction.text import TfidfVectorizer

  with open('love_live_songs_sentiment_classfier\LL_songs_sentiment_classfier.pkl', 'rb') as f:
      model = pickle.load(f)

  df = pd.DataFrame({'title': [song]})

  data = pd.read_csv('love_live_songs_sentiment_classfier\love_live_songs.csv')

  vectorizer = TfidfVectorizer(stop_words='english', max_features=1)
  vectorizer.fit_transform(data['title'])

  sentiment = vectorizer.transform(df['title'])

  pred = model.predict(sentiment.reshape(1, -1))

  return {"sentiment": 'EXCT' if pred[0] == 1 else 'NRM'}