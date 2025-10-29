import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from scipy.spatial.distance import cosine


def evaluate_translation_quality(translation_results: List[Tuple[str, str]]):
    """
    Evaluation Agent: Analyzes translation quality by comparing original and re-translated sentences.

    This function performs three main tasks:
    1. Vectorization: Converts sentences to embeddings using sentence-transformers
    2. Distance Measurement: Calculates cosine distance and statistics
    3. Visualization: Plots the error distribution across all sentences

    Args:
        translation_results: List of tuples containing (original_sentence, final_translated_sentence)

    Prints:
        - Average cosine distance
        - Variance of cosine distances

    Displays:
        - Scatter plot showing error (cosine distance) for each sentence
    """

    print("=== Evaluation Agent: Translation Quality Analysis ===\n")

    # Step 1: Vectorization (Embeddings)
    print("Step 1: Loading embedding model and generating sentence vectors...")

    # Load pre-trained sentence transformer model
    # 'all-MiniLM-L6-v2' is a high-quality, efficient model for semantic similarity
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Extract original and re-translated sentences
    original_sentences = [result[0] for result in translation_results]
    retranslated_sentences = [result[1] for result in translation_results]

    # Generate embeddings for all sentences
    print(f"Encoding {len(original_sentences)} original sentences...")
    original_embeddings = model.encode(original_sentences, convert_to_numpy=True)

    print(f"Encoding {len(retranslated_sentences)} re-translated sentences...")
    retranslated_embeddings = model.encode(retranslated_sentences, convert_to_numpy=True)

    print("✓ Embeddings generated successfully\n")

    # Step 2: Distance Measurement and Statistics
    print("Step 2: Calculating cosine distances...")

    cosine_distances = []

    for i in range(len(original_embeddings)):
        # Calculate cosine distance between original and re-translated embeddings
        distance = cosine(original_embeddings[i], retranslated_embeddings[i])
        cosine_distances.append(distance)

    # Convert to numpy array for statistical calculations
    cosine_distances = np.array(cosine_distances)

    # Calculate statistics
    mean_distance = np.mean(cosine_distances)
    variance_distance = np.var(cosine_distances)
    std_distance = np.std(cosine_distances)
    min_distance = np.min(cosine_distances)
    max_distance = np.max(cosine_distances)

    print("✓ Distance calculations complete\n")

    # Print statistics
    print("=" * 60)
    print("TRANSLATION QUALITY METRICS")
    print("=" * 60)
    print(f"Total Sentences Evaluated: {len(cosine_distances)}")
    print(f"\nCosine Distance Statistics:")
    print(f"  Average (Mean):          {mean_distance:.6f}")
    print(f"  Variance:                {variance_distance:.6f}")
    print(f"  Standard Deviation:      {std_distance:.6f}")
    print(f"  Minimum Distance:        {min_distance:.6f}")
    print(f"  Maximum Distance:        {max_distance:.6f}")
    print("\nInterpretation:")
    print("  • Lower cosine distance = Higher semantic similarity")
    print("  • Distance of 0 = Identical meaning")
    print("  • Distance of 1 = Completely different meaning")
    print("=" * 60)
    print()

    # Step 3: Visualization
    print("Step 3: Generating visualization...\n")

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Subplot 1: Scatter plot with line
    sentence_indices = np.arange(1, len(cosine_distances) + 1)

    ax1.scatter(sentence_indices, cosine_distances, alpha=0.6, c='blue', s=50, label='Cosine Distance')
    ax1.plot(sentence_indices, cosine_distances, alpha=0.3, c='blue', linewidth=1)
    ax1.axhline(y=mean_distance, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_distance:.4f}')
    ax1.fill_between(sentence_indices,
                      mean_distance - std_distance,
                      mean_distance + std_distance,
                      alpha=0.2, color='red', label=f'±1 Std Dev')

    ax1.set_xlabel('Sentence Index', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cosine Distance (Error)', fontsize=12, fontweight='bold')
    ax1.set_title('Translation Quality: Cosine Distance per Sentence\n(English → Spanish → Hebrew → English)',
                  fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(0, len(cosine_distances) + 1)

    # Subplot 2: Histogram of distances
    ax2.hist(cosine_distances, bins=30, color='green', alpha=0.7, edgecolor='black')
    ax2.axvline(x=mean_distance, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_distance:.4f}')
    ax2.set_xlabel('Cosine Distance', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Distribution of Cosine Distances', fontsize=14, fontweight='bold', pad=20)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

    plt.tight_layout()

    print("✓ Visualization complete")
    print("\n=== Displaying plot... ===")
    plt.show()

    return {
        'mean': mean_distance,
        'variance': variance_distance,
        'std': std_distance,
        'min': min_distance,
        'max': max_distance,
        'distances': cosine_distances
    }


# Example usage and testing
if __name__ == "__main__":
    # Sample test data
    test_results = [
        ("The psychohistorians gathered to discuss the future of civilization.",
         "Psychohistorians met to discuss civilization's future."),
        ("Seldon's plan would save humanity from a dark age.",
         "Seldon's strategy would protect humanity from darkness."),
        ("The Foundation was established on Terminus at the galaxy's edge.",
         "The Foundation was set up on Terminus at galaxy's border.")
    ]

    print("Running evaluation with sample data...\n")
    results = evaluate_translation_quality(test_results)
