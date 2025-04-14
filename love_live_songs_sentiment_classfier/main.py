from fastapi import FastAPI  
import pandas as pd
import numpy as np
import re
from math import log
from collections import defaultdict

description = """
**LLClf API** was built for reasons of study in *Python* and *Machine Learning*.
"""

tags_metadata = [
    {
        "name": "Trained Songs",
        "description": "Returns all songs used on the algorithm training",
    },
    {
        "name": "Classifier",
        "description": "Predict the song sentiment by it parsed name",
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title='Love Live! Songs sentiment classifier API',
    description=description,
    version='1.0.1',
    summary='Predict a LL franchise song sentiment by parsing it name!',
    contact={
        "name": "Felipe Ribeiro",
        "url": "http://github.com/feliperfdev",
        "email": "feliper.dev@gmail.com",
    },
    )

data = pd.read_csv('./app/love_live_songs.csv')

def durations_mean(track_durations: list[str]) -> str:
    total_seconds = 0
    for duration in track_durations:
        if np.nan_to_num(duration) != 0.0:
            minutes, seconds = map(int, str(np.nan_to_num(duration)).split(':'))
            total_seconds += minutes * 60 + seconds

    mean_seconds = total_seconds / len(track_durations)
    mean_aproach = round(mean_seconds)

    minutes = mean_aproach // 60
    seconds = mean_aproach % 60

    return f"{minutes}:{seconds:02d}"

data['bpm'].fillna(data['bpm'].mean(), inplace=True)
data['duration'].fillna(durations_mean(data['duration']), inplace=True)

model = pd.read_pickle('./app/LL_songs_sentiment_classfier.pkl')

ENGLISH_STOP_WORDS = {
     "a","about","above","across","after","afterwards","again","against","all","almost","alone","along","already","also","although","always","am","among","amongst","amoungst","amount","an","and","another","any","anyhow","anyone","anything","anyway","anywhere","are","around","as","at","back","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","below","beside","besides","between","beyond","bill","both","bottom","but","by","call","can","cannot","cant","co","con","could","couldnt","cry","de","describe","detail","do","done","down","due","during","each","eg","eight","either","eleven","else","elsewhere","empty","enough","etc","even","ever","every","everyone","everything","everywhere","except","few","fifteen","fifty","fill","find","fire","first","five","for","former","formerly","forty","found","four","from","front","full","further","get","give","go","had","has","hasnt","have","he","hence","her","here","hereafter","hereby","herein","hereupon","hers","herself","him","himself","his","how","however","hundred","i","ie","if","in","inc","indeed","interest","into","is","it","its","itself","keep","last","latter","latterly","least","less","ltd","made","many","may","me","meanwhile","might","mill","mine","more","moreover","most","mostly","move","much","must","my","myself","name","namely","neither","never","nevertheless","next","nine","no","nobody","none","noone","nor","not","nothing","now","nowhere","of","off","often","on","once","one","only","onto","or","other","others","otherwise","our","ours","ourselves","out","over","own","part","per","perhaps","please","put","rather","re","same","see","seem","seemed","seeming","seems","serious","several","she","should","show","side","since","sincere","six","sixty","so","some","somehow","someone","something","sometime","sometimes","somewhere","still","such","system","take","ten","than","that","the","their","them","themselves","then","thence","there","thereafter","thereby","therefore","therein","thereupon","these","they","thick","thin","third","this","those","though","three","through","throughout","thru","thus","to","together","too","top","toward","towards","twelve","twenty","two","un","under","until","up","upon","us","very","via","was","we","well","were","what","whatever","when","whence","whenever","where","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","whose","why","will","with","within","without","would","yet","you","your","yours","yourself","yourselves",
}

def preprocess_title(title: str) -> list:
    title = title.lower()
    tokens = re.findall(r'(?u)\b\w{2,}\b', title)
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]

all_tokens = []

for title in data['title']:
    all_tokens.extend(preprocess_title(title))

token_counts = defaultdict(int)

for token in all_tokens:
    token_counts[token] += 1

selected_word = max(token_counts, key=token_counts.get, default=None)

total_docs = len(data)
doc_freq = sum(1 for title in data['title'] if selected_word in preprocess_title(title))
idf_value = log((total_docs + 1) / (doc_freq + 1)) + 1 if selected_word else 0

@app.get("/") 
async def main_route():     
  
  return {"message": "API Tested OK"}

@app.get("/trained", tags=['Trained Songs']) 
async def trainedSongs():     

  songs = []

  for song in data.values:
     s = {}
     s['title'] = song[0]
     s['album'] = song[1]
     s['attribution'] = song[2]
     s['members'] = song[3]
     s['release_date'] = song[4]
     s['bpm'] = song[5]
     s['duration'] = song[6]
     songs.append(s)

  return {"songs": songs}

@app.post("/song", tags=['Classifier'])
async def classifySongSentiment(song: str):
    tokens = preprocess_title(song)
    total_words = len(tokens)
    
    tf = tokens.count(selected_word) / total_words if total_words > 0 else 0
    tfidf = tf * idf_value
    
    pred = model.predict([[tfidf]])
    
    return {"sentiment": 'EXCITING' if pred[0] == 1 else 'NORMAL'}