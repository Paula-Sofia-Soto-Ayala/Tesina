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
    
    # Process each file if found
    for file_path in file_paths:
        path_parts = file_path.split(os.sep)
        
        try:
            model = path_parts[-4]
            test_type = path_parts[-3]
            lang = path_parts[-2]

            # Read JSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Extract responses
            for response_entry in json_data.get("responses", []):
                question = response_entry.get("question", "")
                prompt = response_entry.get("prompt", "")

                # Extract attempts for each response entry
                for attempt in response_entry.get("attemps", []):
                    data.append({
                        "run_id": json_data.get("run_id", ""),
                        "test_type": test_type,
                        "model": model,
                        "lang": lang,
                        "question": question,
                        "prompt": prompt,
                        "response_number": attempt.get("response_number"),
                        "attempts": attempt.get("attempts"),
                        "response": attempt.get("response", ""),
                        "is_failure": attempt.get("is_failure", False)
                    })
        
        except (json.JSONDecodeError, IndexError) as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # Convert to DataFrame and return
    df = pd.DataFrame(data)
    print("DataFrame loaded:", df.head())
    return df

# Example usage
root_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"
df = load_data(root_folder)
