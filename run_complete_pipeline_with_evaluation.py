import os
from dotenv import load_dotenv
from typing import List, Tuple
from agent_english_spanish import english_spanish_translator
from agent_spanish_hebrew import spanish_hebrew_translator
from agent_hebrew_english import hebrew_english_translator
from agent_sentences_creator import sentences_creator
from agent_evaluation import evaluate_translation_quality


def run_full_pipeline_with_evaluation(api_key: str, num_sentences: int = 100) -> List[Tuple[str, str]]:
    """
    Complete pipeline: Generate sentences, translate through chain, and evaluate quality.

    Args:
        api_key: Claude API key
        num_sentences: Number of sentences to process (default: 100)

    Returns:
        List of tuples containing (original_sentence, final_translated_sentence)
    """
    print("=" * 70)
    print("MULTI-AGENT TRANSLATION PIPELINE WITH EVALUATION")
    print("=" * 70)
    print(f"Pipeline: English → Spanish → Hebrew → English")
    print(f"Total Sentences: {num_sentences}\n")

    translation_results = []
    sentence_count = 0

    # Process sentences through translation pipeline
    for original_sentence in sentences_creator(api_key, count=num_sentences):
        sentence_count += 1
        print(f"[{sentence_count}/{num_sentences}] Processing: {original_sentence[:60]}...")

        # Execute the translation chain
        spanish_output = english_spanish_translator(original_sentence, api_key)
        hebrew_output = spanish_hebrew_translator(spanish_output, api_key)
        final_english_output = hebrew_english_translator(hebrew_output, api_key)

        # Store results
        translation_results.append((original_sentence, final_english_output))

        # Display result
        print(f"    Original: {original_sentence}")
        print(f"    Final:    {final_english_output}\n")

    print("=" * 70)
    print(f"Translation Pipeline Complete: {sentence_count} sentences processed")
    print("=" * 70)
    print()

    # Run evaluation
    print("\nStarting Evaluation Agent...\n")
    evaluation_metrics = evaluate_translation_quality(translation_results)

    return translation_results


def main():
    """Main entry point"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY or create a .env file")
        return

    # Get number of sentences
    try:
        num_input = input("Enter number of sentences to generate (default 100): ").strip()
        num_sentences = int(num_input) if num_input else 100
        if num_sentences <= 0:
            print("Number must be positive. Using default: 100")
            num_sentences = 100
    except ValueError:
        print("Invalid input. Using default: 100")
        num_sentences = 100

    # Run complete pipeline
    results = run_full_pipeline_with_evaluation(api_key, num_sentences)

    print(f"\n✓ Complete! Processed and evaluated {len(results)} sentences.")


if __name__ == "__main__":
    main()
