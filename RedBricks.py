from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re

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

# Function to clean the text
def clean_text(text):
    text = re.sub(r"http\S+|@\S+|#\S+|[^A-Za-z\s]", "", text)
    text = text.lower().strip()
    return text

# Define prediction endpoint
@app.post("/predict/")
def predict_sentiment(input_data: TweetInput):
    cleaned_text = clean_text(input_data.tweet)
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=50, padding='post', truncating='post')
    
    prediction = model.predict(padded_sequence)
    predicted_class = np.argmax(prediction, axis=1)[0]
    sentiment_label = label_encoder.inverse_transform([predicted_class])[0]
    
    return {"predicted_sentiment": sentiment_label}
