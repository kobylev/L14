import os
from dotenv import load_dotenv
from orchestrator import run_translation_pipeline


def test_pipeline():
    """Test script to run the translation pipeline with a small number of sentences"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY or create a .env file")
        return

    # Test with 3 sentences
    print("Running test with 3 sentences...\n")
    run_translation_pipeline(api_key, num_sentences=3)


if __name__ == "__main__":
    test_pipeline()
