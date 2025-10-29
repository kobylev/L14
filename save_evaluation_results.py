import os
import json
from dotenv import load_dotenv
from typing import List, Tuple
from agent_english_spanish import english_spanish_translator
from agent_spanish_hebrew import spanish_hebrew_translator
from agent_hebrew_english import hebrew_english_translator
from agent_sentences_creator import sentences_creator
from agent_evaluation import evaluate_translation_quality
import matplotlib.pyplot as plt


def run_and_save_evaluation(api_key: str, num_sentences: int = 100):
    """
    Run complete pipeline and save evaluation results to files.

    Saves:
    - evaluation_metrics.json: Statistical results
    - evaluation_plot.png: Visualization
    - translation_results.json: All translation pairs
    """

    print("=" * 70)
    print("TRANSLATION PIPELINE WITH SAVED EVALUATION")
    print("=" * 70)

    translation_results = []
    sentence_count = 0

    # Translation pipeline
    for original_sentence in sentences_creator(api_key, count=num_sentences):
        sentence_count += 1
        print(f"[{sentence_count}/{num_sentences}] Processing...")

        spanish_output = english_spanish_translator(original_sentence, api_key)
        hebrew_output = spanish_hebrew_translator(spanish_output, api_key)
        final_english_output = hebrew_english_translator(hebrew_output, api_key)

        translation_results.append((original_sentence, final_english_output))
        print(f"Original: {original_sentence} | Final: {final_english_output}")

    print(f"\n✓ Translation complete: {sentence_count} sentences\n")

    # Run evaluation and get metrics
    print("Running evaluation...\n")

    # Temporarily disable plot display to save it instead
    plt.ioff()

    evaluation_metrics = evaluate_translation_quality(translation_results)

    # Save the plot
    plt.savefig('evaluation_plot.png', dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved: evaluation_plot.png")

    # Close the plot (don't display)
    plt.close()

    # Save metrics to JSON
    metrics_to_save = {
        'total_sentences': len(translation_results),
        'mean_cosine_distance': float(evaluation_metrics['mean']),
        'variance': float(evaluation_metrics['variance']),
        'standard_deviation': float(evaluation_metrics['std']),
        'min_distance': float(evaluation_metrics['min']),
        'max_distance': float(evaluation_metrics['max']),
        'interpretation': {
            'note': 'Lower cosine distance = Higher semantic similarity',
            'perfect_match': 0.0,
            'completely_different': 1.0
        }
    }

    with open('evaluation_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics_to_save, f, indent=2, ensure_ascii=False)

    print(f"✓ Metrics saved: evaluation_metrics.json")

    # Save translation results to JSON
    results_to_save = {
        'total_sentences': len(translation_results),
        'pipeline': 'English → Spanish → Hebrew → English',
        'results': [
            {
                'index': i + 1,
                'original': orig,
                'final_translated': final,
                'cosine_distance': float(evaluation_metrics['distances'][i])
            }
            for i, (orig, final) in enumerate(translation_results)
        ]
    }

    with open('translation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_to_save, f, indent=2, ensure_ascii=False)

    print(f"✓ Translation results saved: translation_results.json")

    print("\n" + "=" * 70)
    print("FILES CREATED:")
    print("=" * 70)
    print("1. evaluation_metrics.json    - Statistical metrics")
    print("2. evaluation_plot.png        - Visualization (high-res)")
    print("3. translation_results.json   - All sentence pairs with distances")
    print("=" * 70)

    return translation_results, evaluation_metrics


def main():
    """Main entry point"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found")
        return

    try:
        num_input = input("Enter number of sentences (default 100): ").strip()
        num_sentences = int(num_input) if num_input else 100
        if num_sentences <= 0:
            num_sentences = 100
    except ValueError:
        num_sentences = 100

    results, metrics = run_and_save_evaluation(api_key, num_sentences)

    print(f"\n✓ Complete! Check the files in: {os.getcwd()}")


if __name__ == "__main__":
    main()
