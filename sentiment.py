from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()

    happy_words = [
        "love", "happy", "great", "excellent", "wonderful",
        "amazing", "good", "fantastic", "awesome", "enjoy"
    ]

    sad_words = [
        "sad", "terrible", "bad", "hate", "awful",
        "disappointed", "angry", "worst", "horrible", "upset"
    ]

    happy_score = sum(word in text for word in happy_words)
    sad_score = sum(word in text for word in sad_words)

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
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
