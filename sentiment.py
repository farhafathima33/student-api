from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(sentence: str) -> str:
    scores = analyzer.polarity_scores(sentence)
    compound = scores["compound"]

    if compound > 0:
        return "happy"
    elif compound < 0:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
