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



import re

def analyze_sentiment(sentence: str) -> str:
    text = sentence.lower()
    words = re.findall(r"\b[\w']+\b", text)

    happy_words = {
        "love", "happy", "great", "excellent", "wonderful",
        "amazing", "good", "fantastic", "awesome", "enjoy",
        "like", "best", "beautiful", "perfect", "pleased",
        "delighted", "excited", "brilliant", "helpful",
        "success", "successful", "recommend", "impressive",
        "glad", "joy", "joyful", "superb", "nice", "positive",
        "satisfied", "thankful", "grateful", "outstanding"
    }

    sad_words = {
        "sad", "terrible", "bad", "hate", "awful",
        "disappointed", "angry", "worst", "horrible", "upset",
        "poor", "boring", "useless", "failed", "failure",
        "annoying", "dislike", "unhappy", "painful", "negative",
        "regret", "frustrated", "disgusting", "waste", "broken",
        "problem", "difficult", "wrong", "ugly", "miserable",
        "disaster", "annoyed", "sadly", "pathetic", "inferior"
    }

    negations = {
        "not", "never", "no", "isn't", "wasn't",
        "don't", "doesn't", "didn't", "can't", "couldn't",
        "won't", "wouldn't", "hardly"
    }

    happy_score = 0
    sad_score = 0
    negate_next = False

    for word in words:
        if word in negations:
            negate_next = True
            continue

        if word in happy_words:
            if negate_next:
                sad_score += 1
            else:
                happy_score += 1
            negate_next = False

        elif word in sad_words:
            if negate_next:
                happy_score += 1
            else:
                sad_score += 1
            negate_next = False

        elif word in {".", "!", "?", ",", ";"}:
            negate_next = False

        elif negate_next:
            # Limit negation to the next word.
            negate_next = False

    if happy_score > sad_score:
        return "happy"
    if sad_score > happy_score:
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
