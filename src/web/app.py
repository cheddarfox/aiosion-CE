from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.core.ai_module import AIModule

app = FastAPI()
ai_module = AIModule()

class GenerateRequest(BaseModel):
    prompt: str
    model: str = None

class GenerateResponse(BaseModel):
    response: str

class TextRequest(BaseModel):
    text: str

class TokenizeResponse(BaseModel):
    tokens: List[str]

class POSTagResponse(BaseModel):
    tags: List[Dict[str, str]]

class NERResponse(BaseModel):
    entities: List[Dict[str, str]]

class SentimentResponse(BaseModel):
    sentiment: Dict[str, float]

class SummarizeRequest(BaseModel):
    text: str
    ratio: float = 0.2

class SummarizeResponse(BaseModel):
    summary: str

@app.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    try:
        response = ai_module.generate_response(request.prompt, request.model)
        return GenerateResponse(response=response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the response")

@app.post("/tokenize", response_model=TokenizeResponse)
async def tokenize_text(request: TextRequest):
    try:
        tokens = ai_module.tokenize(request.text)
        return TokenizeResponse(tokens=tokens)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while tokenizing the text")

@app.post("/pos-tag", response_model=POSTagResponse)
async def pos_tag_text(request: TextRequest):
    try:
        tags = ai_module.pos_tag(request.text)
        return POSTagResponse(tags=[{"word": word, "tag": tag} for word, tag in tags])
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while performing POS tagging")

@app.post("/ner", response_model=NERResponse)
async def named_entity_recognition(request: TextRequest):
    try:
        entities = ai_module.named_entities(request.text)
        return NERResponse(entities=[{"entity": entity, "label": label} for entity, label in entities])
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while performing named entity recognition")

@app.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: TextRequest):
    try:
        sentiment = ai_module.sentiment_analysis(request.text)
        return SentimentResponse(sentiment=sentiment)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while analyzing sentiment")

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    try:
        summary = ai_module.summarize(request.text, request.ratio)
        return SummarizeResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while summarizing the text")

@app.get("/health")
async def health_check():
    return {"status": "ok"}