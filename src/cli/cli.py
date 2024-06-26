import argparse
from src.core.ai_module import AIModule

def main():
    parser = argparse.ArgumentParser(description="AioSion Command-Line Interface")
    parser.add_argument("action", choices=["generate", "tokenize", "pos", "ner", "sentiment", "summarize"],
                        help="Action to perform")
    parser.add_argument("text", help="Input text for the chosen action")
    parser.add_argument("--model", choices=["openai", "anthropic", "google", "huggingface"],
                        help="AI model to use for generation (default: as per config)")
    parser.add_argument("--ratio", type=float, default=0.2,
                        help="Summarization ratio (default: 0.2)")

    args = parser.parse_args()

    ai_module = AIModule()

    if args.action == "generate":
        result = ai_module.generate_response(args.text, model=args.model)
        print("Generated response:", result)
    elif args.action == "tokenize":
        tokens = ai_module.tokenize(args.text)
        print("Tokens:", tokens)
    elif args.action == "pos":
        pos_tags = ai_module.pos_tag(args.text)
        print("Part-of-speech tags:", pos_tags)
    elif args.action == "ner":
        entities = ai_module.named_entities(args.text)
        print("Named entities:", entities)
    elif args.action == "sentiment":
        sentiment = ai_module.sentiment_analysis(args.text)
        print("Sentiment analysis:", sentiment)
    elif args.action == "summarize":
        summary = ai_module.summarize(args.text, ratio=args.ratio)
        print("Summary:", summary)

if __name__ == "__main__":
    main()