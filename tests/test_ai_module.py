import unittest
from unittest.mock import patch, MagicMock
from src.core.ai_module import AIModule

class TestAIModule(unittest.TestCase):

    @patch('src.core.ai_module.spacy.load')
    @patch('src.core.ai_module.openai')
    @patch('src.core.ai_module.Anthropic')
    @patch('src.core.ai_module.palm')
    @patch('src.core.ai_module.pipeline')
    def setUp(self, mock_pipeline, mock_palm, mock_anthropic, mock_openai, mock_spacy_load):
        self.mock_nlp = MagicMock()
        mock_spacy_load.return_value = self.mock_nlp
        self.mock_openai = mock_openai
        self.mock_anthropic = mock_anthropic
        self.mock_palm = mock_palm
        self.mock_pipeline = mock_pipeline
        self.ai_module = AIModule()

    def test_tokenize(self):
        self.mock_nlp.return_value = [MagicMock(text=word) for word in ["This", "is", "a", "test"]]
        result = self.ai_module.tokenize("This is a test")
        self.assertEqual(result, ["This", "is", "a", "test"])

    def test_pos_tag(self):
        mock_tokens = [MagicMock(text=word, pos_=pos) for word, pos in [("This", "DET"), ("is", "AUX"), ("a", "DET"), ("test", "NOUN")]]
        self.mock_nlp.return_value = mock_tokens
        result = self.ai_module.pos_tag("This is a test")
        self.assertEqual(result, [("This", "DET"), ("is", "AUX"), ("a", "DET"), ("test", "NOUN")])

    def test_named_entities(self):
        mock_doc = MagicMock()
        mock_doc.ents = [MagicMock(text="John Doe", label_="PERSON"), MagicMock(text="New York", label_="GPE")]
        self.mock_nlp.return_value = mock_doc
        result = self.ai_module.named_entities("John Doe lives in New York")
        self.assertEqual(result, [("John Doe", "PERSON"), ("New York", "GPE")])

    def test_sentiment_analysis(self):
        mock_doc = MagicMock(sentiment=0.8)
        mock_doc.__len__.return_value = 5
        mock_tokens = [MagicMock(is_stop=i % 2 == 0) for i in range(5)]
        mock_doc.__iter__.return_value = mock_tokens
        self.mock_nlp.return_value = mock_doc
        result = self.ai_module.sentiment_analysis("This is a positive sentence")
        self.assertEqual(result, {'polarity': 0.8, 'subjectivity': 0.6})

    def test_summarize(self):
        mock_doc = MagicMock()
        mock_sentences = [MagicMock(__str__=lambda self: sent) for sent in ["First sentence.", "Second sentence.", "Third sentence."]]
        mock_doc.sents = mock_sentences
        self.mock_nlp.return_value = mock_doc
        result = self.ai_module.summarize("First sentence. Second sentence. Third sentence.", ratio=0.67)
        self.assertEqual(result, "First sentence. Second sentence.")

    def test_generate_response_openai(self):
        self.mock_openai.Completion.create.return_value = MagicMock(choices=[MagicMock(text="OpenAI response")])
        result = self.ai_module.generate_response("Test prompt", model="openai")
        self.assertEqual(result, "OpenAI response")

    def test_generate_response_anthropic(self):
        self.mock_anthropic.return_value.completions.create.return_value = MagicMock(completion="Anthropic response")
        result = self.ai_module.generate_response("Test prompt", model="anthropic")
        self.assertEqual(result, "Anthropic response")

    def test_generate_response_google(self):
        self.mock_palm.generate_text.return_value = MagicMock(result="Google PaLM response")
        result = self.ai_module.generate_response("Test prompt", model="google")
        self.assertEqual(result, "Google PaLM response")

    def test_generate_response_huggingface(self):
        self.mock_pipeline.return_value.return_value = [{'generated_text': "HuggingFace response"}]
        result = self.ai_module.generate_response("Test prompt", model="huggingface")
        self.assertEqual(result, "HuggingFace response")

    def test_generate_response_unsupported_model(self):
        with self.assertRaises(ValueError):
            self.ai_module.generate_response("Test prompt", model="unsupported_model")

    @patch('src.core.ai_module.AIModule.generate_response')
    def test_fallback_mechanism(self, mock_generate_response):
        mock_generate_response.side_effect = [Exception("First failure"), Exception("Second failure"), "Fallback success"]
        result = self.ai_module._fallback("Test prompt", "failed_model")
        self.assertEqual(result, "Fallback success")

    @patch('src.core.ai_module.AIModule.generate_response')
    def test_fallback_mechanism_all_fail(self, mock_generate_response):
        mock_generate_response.side_effect = Exception("All models failed")
        result = self.ai_module._fallback("Test prompt", "failed_model")
        self.assertEqual(result, "I apologize, but I'm unable to generate a response at the moment.")

if __name__ == '__main__':
    unittest.main()