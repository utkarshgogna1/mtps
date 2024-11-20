from rouge import Rouge
import os

# Install necessary package if not already installed
# pip install rouge

def load_reference_summary(file_path):
    """
    Loads the reference summary from the provided file.

    Args:
        file_path (str): Path to the reference summary file.

    Returns:
        str: The reference summary text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def evaluate_summary(generated_summary, reference_summary):
    """
    Evaluates the performance of the generated summary using ROUGE metrics.

    Args:
        generated_summary (str): The summary text generated by the model.
        reference_summary (str): The reference summary for comparison.

    Returns:
        dict: Dictionary containing ROUGE-N (unigram, bigram) and ROUGE-L scores.
    """
    # Initialize the Rouge object
    rouge = Rouge()

    # Evaluate the generated summary against the reference summary
    scores = rouge.get_scores(generated_summary, reference_summary, avg=True)

    return scores


def main():
    # Paths to the generated and reference summaries
    generated_summary_file = 'data/summarized_texts_v2/transcription_test_AimeeMullins_1249s_summarized.txt'
    reference_summary_file = 'data/summarized_texts_v2/reference_summary_AimeeMullins_1249s.txt'

    # Load the generated and reference summaries
    if not os.path.exists(generated_summary_file) or not os.path.exists(reference_summary_file):
        print("Generated or reference summary file not found.")
        return

    with open(generated_summary_file, 'r', encoding='utf-8') as file:
        generated_summary = file.read()

    reference_summary = load_reference_summary(reference_summary_file)

    # Evaluate the generated summary using ROUGE scores
    rouge_scores = evaluate_summary(generated_summary, reference_summary)

    # Print the ROUGE scores
    print("\nROUGE Scores:")
    for key, value in rouge_scores.items():
        print(f"{key}: Precision: {value['p']:.4f}, Recall: {value['r']:.4f}, F1-Score: {value['f']:.4f}")


if __name__ == "__main__":
    main()
