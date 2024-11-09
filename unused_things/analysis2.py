import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os

# Set output folder for saving analysis results
output_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina/outcomes"

# Ensure subfolders for each analysis
def create_analysis_folders(base_folder):
    subfolders = ["response_distribution", "test_comparison", "language_discrepancies", "failure_rate", "consensus_time"]
    for folder in subfolders:
        path = os.path.join(base_folder, folder)
        os.makedirs(path, exist_ok=True)

# Load JSON files from nested directory structure
def load_data(root_folder):
    data = []
    allowed_models = {"ChatGPT", "Claude", "Gemini"}
    
    # Find JSON files in nested structure
    file_paths = glob(f"{root_folder}/*/*/*/results/*.json")
    print("Found JSON files:", file_paths)  # Debug

    for file_path in file_paths:
        path_parts = file_path.split(os.sep)
        print("Path components:", path_parts)  # Debug

        try:
            model = path_parts[-4]
            test_type = path_parts[-3]
            lang = path_parts[-2]

            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            for response_entry in json_data.get("responses", []):
                entry = {
                    "model": model,
                    "test_type": test_type,
                    "lang": lang,
                    "run_id": json_data.get("run_id", ""),
                    "response": response_entry.get("response", ""),
                    "question": response_entry.get("question", ""),
                    "attempts": len(response_entry.get("attemps", [])),
                    "responses": [attempt.get("response", "") for attempt in response_entry.get("attemps", [])]
                }
                data.append(entry)
        except (json.JSONDecodeError, IndexError) as e:
            print(f"Error reading {file_path}: {e}")
            continue

    df = pd.DataFrame(data)
    print("DataFrame loaded:", df.head())  # Debug
    return df

# Save plots with consistent formatting
def save_plot(data, plot_func, plot_title, xlabel, ylabel, filepath, plot_hue=None):
    plt.figure(figsize=(12, 8))
    plot_func(data=data, x=xlabel, y=ylabel, hue=plot_hue)
    plt.title(plot_title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title=plot_hue, loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

# Response distribution analysis
def analyze_response_distribution(df, output_folder):
    response_dist = df.groupby(['model', 'test_type', 'lang', 'response']).size().reset_index(name='count')
    response_csv_path = os.path.join(output_folder, "response_distribution", "response_distribution.csv")
    response_plot_path = os.path.join(output_folder, "response_distribution", "response_distribution.png")
    
    response_dist.to_csv(response_csv_path, index=False)
    save_plot(
        response_dist, sns.barplot, "Response Distribution by Model and Language",
        "response", "count", response_plot_path, plot_hue="lang"
    )
    print(f"Response distribution analysis saved to {response_csv_path} and plot to {response_plot_path}.")

# Test comparison analysis
def analyze_test_comparison(df, output_folder):
    test_comparison = df.groupby(['test_type', 'response']).size().reset_index(name='count')
    test_comparison['percentage'] = (test_comparison['count'] / test_comparison.groupby('test_type')['count'].transform('sum')) * 100
    
    test_csv_path = os.path.join(output_folder, "test_comparison", "test_comparison.csv")
    test_plot_path = os.path.join(output_folder, "test_comparison", "test_comparison.png")
    
    test_comparison.to_csv(test_csv_path, index=False)
    save_plot(
        test_comparison, sns.barplot, "Test Comparison by Response", 
        "test_type", "percentage", test_plot_path, plot_hue="response"
    )
    print(f"Test comparison analysis saved to {test_csv_path} and plot to {test_plot_path}.")

# Language discrepancy analysis
def analyze_language_discrepancies(df, output_folder):
    language_diff = df.pivot_table(index=['model', 'question'], columns='lang', values='response', aggfunc=lambda x: x.iloc[0]).reset_index()
    discrepancy_csv_path = os.path.join(output_folder, "language_discrepancies", "language_discrepancies.csv")
    
    if 'en' in language_diff.columns and 'es' in language_diff.columns:
        discrepancies = language_diff[language_diff['en'] != language_diff['es']]
        discrepancies.to_csv(discrepancy_csv_path, index=False)
        print(f"Language discrepancies saved to {discrepancy_csv_path}.")
    else:
        print("Language columns 'en' and/or 'es' not found for discrepancy analysis.")

# Failure rate analysis
def analyze_failure_rate(df, output_folder):
    failure_rate = df[df['is_failure']].groupby(['model', 'test_type', 'lang']).size().reset_index(name='failure_count')
    failure_csv_path = os.path.join(output_folder, "failure_rate", "failure_rate.csv")
    failure_plot_path = os.path.join(output_folder, "failure_rate", "failure_rate.png")
    
    failure_rate.to_csv(failure_csv_path, index=False)
    save_plot(
        failure_rate, sns.barplot, "Failure Rate by Model, Test, and Language", 
        "model", "failure_count", failure_plot_path, plot_hue="lang"
    )
    print(f"Failure rate analysis saved to {failure_csv_path} and plot to {failure_plot_path}.")

# Main execution
root_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"
create_analysis_folders(output_folder)
df = load_data(root_folder)

if not df.empty:
    analyze_response_distribution(df, output_folder)
    analyze_test_comparison(df, output_folder)
    analyze_language_discrepancies(df, output_folder)
    analyze_failure_rate(df, output_folder)
    # Debug: Check column names in DataFrame
    print("Columns in DataFrame:", df.columns)
    print("Sample data:", df.head())
else:
    print("No data found. Please check the folder structure and JSON file contents.")
    
