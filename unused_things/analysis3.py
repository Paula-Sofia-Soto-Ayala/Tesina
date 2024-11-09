import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os

# Create a reusable function for saving plots
def save_plot(data, plot_func, title, x, y, save_path, plot_hue=None):
    plt.figure(figsize=(12, 8))
    plot = plot_func(data=data, x=x, y=y, hue=plot_hue)
    plot.set_title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()  # Close plot to free memory
    print(f"Saved plot to {save_path}")

# Load JSON files from a nested directory structure
def load_data(root_folder):
    data = []
    file_paths = glob(f"{root_folder}/*/*/*/results/*.json")
    for file_path in file_paths:
        path_parts = file_path.split(os.sep)
        model = path_parts[-4]
        test_type = path_parts[-3]
        lang = path_parts[-2]
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for response_entry in json_data.get("responses", []):
            for attempt in response_entry.get("attemps", []):
                data.append({
                    "run_id": json_data.get("run_id", ""),
                    "test_type": test_type,
                    "model": model,
                    "lang": lang,
                    "question": response_entry.get("question", ""),
                    "response": attempt.get("response", ""),
                    "attempt_number": attempt.get("response_number"),
                    "is_failure": attempt.get("is_failure")
                })
    df = pd.DataFrame(data)
    print(df.head())
    return df

# Analyze response distribution by model and language
def analyze_response_distribution(df, output_folder):
    response_dist = df.groupby(['model', 'test_type', 'lang', 'response']).size().reset_index(name='count')
    for (model, test_type, lang), group_data in response_dist.groupby(['model', 'test_type', 'lang']):
        subfolder = os.path.join(output_folder, model, test_type, lang, "response_distribution")
        os.makedirs(subfolder, exist_ok=True)
        
        # Save data and plot
        group_data.to_csv(os.path.join(subfolder, "response_distribution.csv"), index=False)
        save_plot(
            group_data, sns.barplot, f"Response Distribution for {model} - {test_type} ({lang})",
            x="response", y="count", save_path=os.path.join(subfolder, "response_distribution.png")
        )

# Analyze test comparisons across different models and languages
def analyze_test_comparison(df, output_folder):
    test_comparison = df.groupby(['test_type', 'response']).size().reset_index(name='count')
    test_comparison['percentage'] = test_comparison.groupby('test_type')['count'].apply(lambda x: 100 * x / x.sum())
    
    for test_type, group_data in test_comparison.groupby('test_type'):
        subfolder = os.path.join(output_folder, test_type, "test_comparison")
        os.makedirs(subfolder, exist_ok=True)
        
        # Save data and plot
        group_data.to_csv(os.path.join(subfolder, "test_comparison.csv"), index=False)
        save_plot(
            group_data, sns.barplot, f"Test Comparison - {test_type}",
            x="response", y="percentage", save_path=os.path.join(subfolder, "test_comparison.png")
        )

# Analyze discrepancies between languages for each model and test
def analyze_language_discrepancies(df, output_folder):
    if 'lang' in df.columns and 'response' in df.columns:
        language_diff = df.pivot_table(index=['model', 'test_type', 'question'], columns='lang', values='response', aggfunc=lambda x: x.iloc[0]).reset_index()
        for (model, test_type), group_data in language_diff.groupby(['model', 'test_type']):
            subfolder = os.path.join(output_folder, model, test_type, "language_discrepancies")
            os.makedirs(subfolder, exist_ok=True)
            
            if 'en' in group_data.columns and 'es' in group_data.columns:
                discrepancies = group_data[group_data['en'] != group_data['es']]
                discrepancies.to_csv(os.path.join(subfolder, "language_discrepancies.csv"), index=False)
                print(f"Saved language discrepancies for {model} - {test_type} to {subfolder}")

# Analyze failure rates for each model, test, and language
def analyze_failure_rate(df, output_folder):
    if 'is_failure' in df.columns:
        failure_rate = df[df['is_failure']].groupby(['model', 'test_type', 'lang']).size().reset_index(name='failure_count')
        for (model, test_type, lang), group_data in failure_rate.groupby(['model', 'test_type', 'lang']):
            subfolder = os.path.join(output_folder, model, test_type, lang, "failure_rate")
            os.makedirs(subfolder, exist_ok=True)
            
            # Save data and plot
            group_data.to_csv(os.path.join(subfolder, "failure_rate.csv"), index=False)
            save_plot(
                group_data, sns.barplot, f"Failure Rate for {model} - {test_type} ({lang})",
                x="model", y="failure_count", save_path=os.path.join(subfolder, "failure_rate.png")
            )

# Example usage
root_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"
output_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina/outcomes"

df = load_data(root_folder)
""" if not df.empty:
    analyze_response_distribution(df, output_folder)
    analyze_test_comparison(df, output_folder)
    analyze_language_discrepancies(df, output_folder)
    analyze_failure_rate(df, output_folder)
else:
    print("No data found. Please check the folder structure and JSON file contents.") """
