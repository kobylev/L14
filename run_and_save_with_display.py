import os
import json
import csv
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Tuple
from agent_english_spanish import english_spanish_translator
from agent_spanish_hebrew import spanish_hebrew_translator
from agent_hebrew_english import hebrew_english_translator
from agent_sentences_creator import sentences_creator
from agent_evaluation import evaluate_translation_quality
import matplotlib
import matplotlib.pyplot as plt


def run_pipeline_save_and_display(api_key: str, num_sentences: int = 100):
    """
    Run complete pipeline, display results, AND save to files.

    Displays:
    - Console output with all metrics
    - Interactive plot window

    Saves to Insights folder:
    - evaluation_metrics.json: Statistical results
    - evaluation_plot.png: Visualization
    - translation_results.json: All translation pairs
    - translation_results.csv: All translation pairs in CSV format
    """

    # Create Insights directory if it doesn't exist
    insights_dir = Path("Insights")
    insights_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("TRANSLATION PIPELINE WITH EVALUATION")
    print("=" * 70)
    print(f"Pipeline: English → Spanish → Hebrew → English")
    print(f"Total Sentences: {num_sentences}")
    print(f"Output Directory: {insights_dir.absolute()}\n")

    translation_results = []
    sentence_count = 0

    # Translation pipeline
    for original_sentence in sentences_creator(api_key, count=num_sentences):
        sentence_count += 1
        print(f"[{sentence_count}/{num_sentences}] Processing...")

        try:
            spanish_output = english_spanish_translator(original_sentence, api_key)
            hebrew_output = spanish_hebrew_translator(spanish_output, api_key)
            final_english_output = hebrew_english_translator(hebrew_output, api_key)

            translation_results.append((original_sentence, final_english_output))
            print(f"Original: {original_sentence} | Final: {final_english_output}")
        except Exception as e:
            print(f"ERROR on sentence {sentence_count}: {str(e)}")
            continue

    print(f"\n" + "=" * 70)
    print(f"Translation Pipeline Complete: {sentence_count} sentences")
    print("=" * 70)
    print()

    # Run evaluation
    print("Starting Evaluation Agent...\n")
    evaluation_metrics = evaluate_translation_quality(translation_results)

    # IMPORTANT: Save the plot BEFORE showing it
    print("\nSaving results to Insights folder...")

    # Define file paths in Insights directory
    plot_file = insights_dir / 'evaluation_plot.png'
    metrics_file = insights_dir / 'evaluation_metrics.json'
    json_file = insights_dir / 'translation_results.json'
    csv_file = insights_dir / 'translation_results.csv'

    # Get the figure from evaluation metrics and save
    fig = evaluation_metrics['figure']
    fig.savefig(plot_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Plot saved: {plot_file}")

    # Now display the plot
    print("\n=== Displaying plot... ===")
    plt.show()

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

    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics_to_save, f, indent=2, ensure_ascii=False)
    print(f"✓ Metrics saved: {metrics_file}")

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

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results_to_save, f, indent=2, ensure_ascii=False)
    print(f"✓ Translation results saved: {json_file}")

    # Save CSV with cosine distances
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'Original English', 'Final Re-translated English', 'Cosine Distance'])
        for idx, (orig, final) in enumerate(translation_results):
            cosine_dist = float(evaluation_metrics['distances'][idx])
            writer.writerow([idx + 1, orig, final, f"{cosine_dist:.6f}"])
    print(f"✓ CSV with distances saved: {csv_file}")

    print("\n" + "=" * 70)
    print(f"FILES CREATED IN: {insights_dir.absolute()}")
    print("=" * 70)
    print("1. evaluation_metrics.json    - Statistical metrics")
    print("2. evaluation_plot.png        - Visualization (high-res)")
    print("3. translation_results.json   - All sentence pairs with distances")
    print("4. translation_results.csv    - All sentence pairs (CSV format)")
    print("=" * 70)

    return translation_results, evaluation_metrics


def main():
    """Main entry point"""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set ANTHROPIC_API_KEY or create a .env file")
        return

    try:
        num_input = input("Enter number of sentences to generate (default 100): ").strip()
        num_sentences = int(num_input) if num_input else 100
        if num_sentences <= 0:
            print("Number must be positive. Using default: 100")
            num_sentences = 100
    except ValueError:
        print("Invalid input. Using default: 100")
        num_sentences = 100

    print(f"\nStarting pipeline with {num_sentences} sentences...\n")

    results, metrics = run_pipeline_save_and_display(api_key, num_sentences)

    print(f"\n✓ COMPLETE! All results displayed and saved.")


if __name__ == "__main__":
    main()
