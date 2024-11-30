from bert_score import score
import os

# Ensure BERTScore package is installed
# pip install bert-score

def load_text(file_path):
    """
    Loads text from the provided file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The loaded text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_bertscore_self_similarity(original_text, generated_summary):
    """
    Calculates BERTScore self-similarity between the original text and the generated summary.

    Args:
        original_text (str): The original transcription text.
        generated_summary (str): The summary text generated by the model.

    Returns:
        tuple: Precision, Recall, and F1 scores as averages.
    """
    P, R, F1 = score([generated_summary], [original_text], lang="en", verbose=True)
    return P.mean().item(), R.mean().item(), F1.mean().item()

def calculate_compression_ratio(original_text, generated_summary):
    """
    Calculates the compression ratio between the original text and the generated summary.

    Args:
        original_text (str): The original transcription text.
        generated_summary (str): The summary text generated by the model.

    Returns:
        float: The compression ratio.
    """
    original_length = len(original_text.split())
    summary_length = len(generated_summary.split())
    if summary_length == 0:
        return 0  # Avoid division by zero
    return original_length / summary_length

def main():
    # Paths to the directories
    base_dir = 'data/summarized_texts_v2'
    transcriptions_dir = 'data/transcripts'
    eval_reports_dir = 'data/eval_reports'

    # Ensure the eval_reports directory exists
    os.makedirs(eval_reports_dir, exist_ok=True)

    # Initialize report aggregation
    report_path = os.path.join(eval_reports_dir, "bertscore_report.txt")
    total_files = 0
    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0
    total_compression_ratio = 0.0

    with open(report_path, 'w', encoding='utf-8') as report:
        report.write("=== BERTScore Self-Similarity Report ===\n\n")

        # Iterate over generated summary files in the base directory
        for file_name in os.listdir(base_dir):
            if not (file_name.startswith("transcription_") and file_name.endswith("_summarized.txt")):
                continue

            # Construct file paths
            generated_summary_file = os.path.join(base_dir, file_name)
            original_text_file = os.path.join(transcriptions_dir, file_name.replace("_summarized.txt", ".txt"))

            # Check if the original transcription exists
            if not os.path.exists(original_text_file):
                print(f"Original transcription not found for: {file_name}")
                continue

            # Load texts
            generated_summary = load_text(generated_summary_file)
            original_text = load_text(original_text_file)

            # Calculate BERTScore self-similarity
            precision, recall, f1 = calculate_bertscore_self_similarity(original_text, generated_summary)

            # Calculate compression ratio
            compression_ratio = calculate_compression_ratio(original_text, generated_summary)

            # Update totals
            total_files += 1
            total_precision += precision
            total_recall += recall
            total_f1 += f1
            total_compression_ratio += compression_ratio

            # Write individual results to the report
            report.write(f"File: {file_name}\n")
            report.write(f"Precision: {precision:.4f}\n")
            report.write(f"Recall: {recall:.4f}\n")
            report.write(f"F1 Score: {f1:.4f}\n")
            report.write(f"Compression Ratio: {compression_ratio:.4f}\n")
            report.write("--------------------------------------------------\n")

        # Calculate averages
        if total_files > 0:
            avg_precision = total_precision / total_files
            avg_recall = total_recall / total_files
            avg_f1 = total_f1 / total_files
            avg_compression_ratio = total_compression_ratio / total_files
        else:
            avg_precision = avg_recall = avg_f1 = avg_compression_ratio = 0.0

        # Write summary statistics
        report.write("\nSummary Statistics:\n")
        report.write(f"Total files processed: {total_files}\n")
        report.write(f"Average Precision: {avg_precision:.4f}\n")
        report.write(f"Average Recall: {avg_recall:.4f}\n")
        report.write(f"Average F1 Score: {avg_f1:.4f}\n")
        report.write(f"Average Compression Ratio: {avg_compression_ratio:.4f}\n")

    print(f"BERTScore report generated: {report_path}")

if __name__ == "__main__":
    main()