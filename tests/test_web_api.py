import pytest
from fastapi.testclient import TestClient
from src.web.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_response():
    response = client.post("/generate", json={"prompt": "Hello, how are you?", "model": "openai"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_tokenize():
    response = client.post("/tokenize", json={"text": "This is a test."})
    assert response.status_code == 200
    assert "tokens" in response.json()
    assert response.json()["tokens"] == ["This", "is", "a", "test", "."]

def test_pos_tag():
    response = client.post("/pos-tag", json={"text": "This is a test."})
    assert response.status_code == 200
    assert "tags" in response.json()
    assert len(response.json()["tags"]) == 5  # 4 words + 1 punctuation

def test_named_entity_recognition():
    response = client.post("/ner", json={"text": "Apple Inc. is located in Cupertino."})
    assert response.status_code == 200
    assert "entities" in response.json()
    entities = response.json()["entities"]
    assert any(entity["entity"] == "Apple Inc." for entity in entities)
    assert any(entity["entity"] == "Cupertino" for entity in entities)

def test_sentiment_analysis():
    response = client.post("/sentiment", json={"text": "I love this product!"})
    assert response.status_code == 200
    assert "sentiment" in response.json()
    sentiment = response.json()["sentiment"]
    assert "polarity" in sentiment
    assert "subjectivity" in sentiment

def test_summarize():
    long_text = "This is a long text. It contains multiple sentences. We want to summarize it."
    response = client.post("/summarize", json={"text": long_text, "ratio": 0.5})
    assert response.status_code == 200
    assert "summary" in response.json()
    assert len(response.json()["summary"]) < len(long_text)

def test_generate_response_invalid_model():
    response = client.post("/generate", json={"prompt": "Hello", "model": "invalid_model"})
    assert response.status_code == 400
    assert "detail" in response.json()

# Add more edge cases and error handling tests as needed