from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
from typing import List
from xquik_import import parse_xquik_export

# Load the model, tokenizer, and label encoder
model = tf.keras.models.load_model('tweet_sentiment_lstm_model.h5')
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)

# Initialize FastAPI app
app = FastAPI()

# Define input data model
class TweetInput(BaseModel):
    tweet: str


class BatchTweetInput(BaseModel):
    tweets: List[str]


class XquikExportInput(BaseModel):
    export: str
    filename: str = "tweets.json"


# Function to clean the text
def clean_text(text):
    text = re.sub(r"http\S+|@\S+|#\S+|[^A-Za-z\s]", "", text)
    text = text.lower().strip()
    return text


def predict_tweet_sentiment(tweet: str):
    cleaned_text = clean_text(tweet)
    if not cleaned_text:
        raise ValueError("Tweet text must contain words.")

    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=50, padding='post', truncating='post')

    prediction = model.predict(padded_sequence)
    predicted_class = np.argmax(prediction, axis=1)[0]
    sentiment_label = label_encoder.inverse_transform([predicted_class])[0]

    return sentiment_label


# Define prediction endpoint
@app.post("/predict/")
def predict_sentiment(input_data: TweetInput):
    try:
        sentiment_label = predict_tweet_sentiment(input_data.tweet)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"predicted_sentiment": sentiment_label}


@app.post("/predict/batch/")
def predict_batch_sentiment(input_data: BatchTweetInput):
    if not input_data.tweets:
        raise HTTPException(status_code=400, detail="At least one tweet is required.")

    predictions = []
    for index, tweet in enumerate(input_data.tweets):
        try:
            sentiment_label = predict_tweet_sentiment(tweet)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=f"Tweet {index + 1}: {exc}") from exc
        predictions.append({"tweet": tweet, "predicted_sentiment": sentiment_label})

    return {"predictions": predictions}


@app.post("/predict/xquik-export/")
def predict_xquik_export(input_data: XquikExportInput):
    try:
        tweets = parse_xquik_export(input_data.export, input_data.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not tweets:
        raise HTTPException(status_code=400, detail="Xquik export did not contain tweet text.")

    return predict_batch_sentiment(BatchTweetInput(tweets=tweets))
