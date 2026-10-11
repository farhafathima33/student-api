
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

# Three-class sentiment model
classifier = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(sentence: str) -> str:
    result = classifier(sentence, truncation=True)[0]
    label = result["label"].lower()

    if label == "positive":
        return "happy"
    elif label == "negative":
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
async def batch_sentiment(request: SentimentRequest):
    results = [
        {
            "sentence": sentence,
            "sentiment": analyze_sentiment(sentence)
        }
        for sentence in request.sentences
    ]
    return {"results": results}
