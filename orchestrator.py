import os
from dotenv import load_dotenv
from agent_english_spanish import english_spanish_translator
from agent_spanish_hebrew import spanish_hebrew_translator
from agent_hebrew_english import hebrew_english_translator
from agent_sentences_creator import sentences_creator


def run_translation_pipeline(api_key: str, num_sentences: int = 100):
    """
    Orchestrator: Manages the complete translation pipeline.

    This function coordinates:
    1. Sentence generation via sentences_creator
    2. Pipeline execution through all three translation agents for each sentence
    3. Synchronized output of original and final translated results

    The pipeline processes sentences as they are generated, enabling quasi-parallel execution:
    English -> Spanish (Agent 2) -> Hebrew (Agent 3) -> English (Agent 4)

    Args:
        api_key: Claude API key for all agent operations
        num_sentences: Number of sentences to generate and process (default: 100)
    """
    print("=== Multi-Agent Translation Pipeline ===")
    print("Pipeline: English -> Spanish -> Hebrew -> English")
    print(f"Generating and processing {num_sentences} sentences...\n")

    sentence_count = 0

    # Process sentences as they are generated (synchronized pipeline)
    for original_sentence in sentences_creator(api_key, count=num_sentences):
        sentence_count += 1

        # Execute the translation chain for this sentence
        # Agent 2: English -> Spanish
        spanish_output = english_spanish_translator(original_sentence, api_key)

        # Agent 3: Spanish -> Hebrew
        hebrew_output = spanish_hebrew_translator(spanish_output, api_key)

        # Agent 4: Hebrew -> English
        final_english_output = hebrew_english_translator(hebrew_output, api_key)

        # Output the synchronized result
        print(f"Original: {original_sentence} | Final Translated: {final_english_output}")

    print(f"\n=== Pipeline Complete: Processed {sentence_count} sentences ===")


def main():
    """Main entry point - runs the multi-agent translation pipeline"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY or create a .env file")
        return

    # Get number of sentences from user (default: 100)
    try:
        num_input = input("Enter number of sentences to generate (default 100): ").strip()
        num_sentences = int(num_input) if num_input else 100
        if num_sentences <= 0:
            print("Number must be positive. Using default: 100")
            num_sentences = 100
    except ValueError:
        print("Invalid input. Using default: 100")
        num_sentences = 100

    # Run the complete orchestrator pipeline
    run_translation_pipeline(api_key, num_sentences)


if __name__ == "__main__":
    main()
