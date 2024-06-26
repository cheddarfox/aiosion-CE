import os
from typing import Dict, Any, List
import logging
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import google.generativeai as palm
from transformers import pipeline
import yaml
import spacy
from spacy.language import Language
from spacy.tokens import Doc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIModule:
    def __init__(self, config_path: str = 'config/config.yml'):
        self.config = self._load_config(config_path)
        self.models = self._initialize_models()
        self.nlp = self._initialize_spacy()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    def _initialize_models(self) -> Dict[str, Any]:
        models = {}
        try:
            # OpenAI
            openai.api_key = os.getenv(self.config['ai_models']['openai']['api_key'].strip('${}'))
            models['openai'] = openai
            
            # Anthropic
            anthropic_api_key = os.getenv(self.config['ai_models']['anthropic']['api_key'].strip('${}'))
            models['anthropic'] = Anthropic(api_key=anthropic_api_key)
            
            # Google PaLM
            palm.configure(api_key=os.getenv(self.config['ai_models']['google']['api_key'].strip('${}')))
            models['google'] = palm
            
            # HuggingFace
            models['huggingface'] = pipeline('text-generation', model=self.config['ai_models']['huggingface']['default'])
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise
        return models

    def _initialize_spacy(self) -> Language:
        try:
            return spacy.load(self.config['nlp']['model'])
        except Exception as e:
            logger.error(f"Error loading spaCy model: {str(e)}")
            raise

    def generate_response(self, prompt: str, model: str = None) -> str:
        if model is None:
            model = self.config['model_selection']['primary']
        
        try:
            if model == 'openai':
                response = self.models['openai'].Completion.create(
                    engine=self.config['ai_models']['openai']['default'],
                    prompt=prompt,
                    max_tokens=150
                )
                return response.choices[0].text.strip()
            
            elif model == 'anthropic':
                response = self.models['anthropic'].completions.create(
                    model=self.config['ai_models']['anthropic']['default'],
                    prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
                    max_tokens_to_sample=150
                )
                return response.completion.strip()
            
            elif model == 'google':
                response = self.models['google'].generate_text(
                    model=self.config['ai_models']['google']['default'],
                    prompt=prompt,
                    max_output_tokens=150
                )
                return response.result
            
            elif model == 'huggingface':
                response = self.models['huggingface'](prompt, max_length=150)
                return response[0]['generated_text']
            
            else:
                raise ValueError(f"Unsupported model: {model}")
        
        except ValueError as e:
            logger.error(f"Error generating response with {model}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error generating response with {model}: {str(e)}")
            return self._fallback(prompt, model)

    def _fallback(self, prompt: str, failed_model: str) -> str:
        fallback_order = self.config['model_selection']['fallback_order']
        for model in fallback_order:
            if model != failed_model:
                try:
                    return self.generate_response(prompt, model)
                except Exception as e:
                    logger.warning(f"Fallback to {model} failed: {str(e)}")
                    continue
        logger.error("All fallback options exhausted")
        return "I apologize, but I'm unable to generate a response at the moment."

    def tokenize(self, text: str) -> List[str]:
        try:
            doc = self.nlp(text)
            return [token.text for token in doc]
        except Exception as e:
            logger.error(f"Error in tokenization: {str(e)}")
            return []

    def pos_tag(self, text: str) -> List[tuple]:
        try:
            doc = self.nlp(text)
            return [(token.text, token.pos_) for token in doc]
        except Exception as e:
            logger.error(f"Error in POS tagging: {str(e)}")
            return []

    def named_entities(self, text: str) -> List[tuple]:
        try:
            doc = self.nlp(text)
            return [(ent.text, ent.label_) for ent in doc.ents]
        except Exception as e:
            logger.error(f"Error in named entity recognition: {str(e)}")
            return []

    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        try:
            doc = self.nlp(text)
            return {
                'polarity': doc.sentiment,
                'subjectivity': sum(token.is_stop for token in doc) / len(doc)
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return {'polarity': 0.0, 'subjectivity': 0.0}

    def summarize(self, text: str, ratio: float = 0.2) -> str:
        try:
            doc = self.nlp(text)
            sentences = list(doc.sents)
            num_sentences = max(1, round(len(sentences) * ratio))
            return ' '.join(str(sent) for sent in sentences[:num_sentences])
        except Exception as e:
            logger.error(f"Error in text summarization: {str(e)}")
            return ""

# Usage example:
# ai = AIModule()
# response = ai.generate_response("Hello, how are you?")
# print(response)
# tokens = ai.tokenize("This is a test sentence.")
# print(tokens)
# pos_tags = ai.pos_tag("The quick brown fox jumps over the lazy dog.")
# print(pos_tags)
# entities = ai.named_entities("Apple Inc. was founded by Steve Jobs in Cupertino, California.")
# print(entities)
# sentiment = ai.sentiment_analysis("I love this product! It's amazing!")
# print(sentiment)
# summary = ai.summarize("This is a long text that needs to be summarized. It contains multiple sentences with various information. We want to extract the key points.")
# print(summary)