import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os

# Create folder to store results
output_folder = "results"
os.makedirs(output_folder, exist_ok=True)

# Load JSON files from a nested directory structure
def load_data(root_folder):
    data = []
    allowed_models = {"ChatGPT", "Claude", "Gemini"}
    
    # Simplified pattern to find JSON files
    file_paths = glob(f"{root_folder}/*/*/*/results/*.json")
    
    # Debug: Print all JSON file paths found
    print("Found JSON files:", file_paths)

    # Process each file if found
    for file_path in file_paths:
        path_parts = file_path.split(os.sep)
        
        # Debug: Print path components to ensure structure is parsed correctly
        print("Path components:", path_parts)

        try:
            model = path_parts[-4]
            test_type = path_parts[-3]
            lang = path_parts[-2]

            # Read JSON data and check contents
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

    # Convert to DataFrame and debug the result
    df = pd.DataFrame(data)
    print("DataFrame loaded:", df.head())
    return df

# Consensus time analysis
def analyze_consensus_time(df):
    # Ensure 'test' column exists, rename if necessary
    if 'test' not in df.columns and 'test_type' in df.columns:
        df.rename(columns={'test_type': 'test'}, inplace=True)
    
    # Ensure 'lang' column exists, rename if necessary
    if 'lang' not in df.columns:
        raise KeyError("'lang' column not found in the DataFrame.")
    
    # Print the columns to debug
    print("DataFrame columns after renaming (if applicable):", df.columns)

    # Group by the relevant columns and calculate the number of unique responses
    group_df = df.groupby(['model', 'test', 'lang', 'question']).agg(
        response_count=('response', 'nunique')  # Count the number of unique responses
    ).reset_index()

    # Display the grouped data for verification
    print(group_df.head())

    plt.figure(figsize=(12, 8))
    sns.barplot(x='test', y='response_count', hue='model', data=group_df)
    plt.title('Response Count by Test and Model')
    plt.xlabel('Test')
    plt.ylabel('Unique Response Count')
    plt.legend(title='Model', loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Further analysis, if needed
    # For example, comparing consensus times across different languages or tests
    language_group_df = group_df.groupby(['lang', 'test'])['response_count'].mean().reset_index()
    print(language_group_df)
    
# Process data and convert to DataFrame
def process_data(data):
    rows = []
    for entry in data:
        for response in entry["responses"]:
            for attempt in response["attemps"]:
                rows.append({
                    "run_id": entry["run_id"],
                    "test": entry["test"],
                    "model": entry["model"],
                    "language": entry["lang"],
                    "question": response["question"],
                    "response": attempt["response"],
                    "attempt_number": attempt["response_number"],
                    "is_failure": attempt["is_failure"]
                })
    df = pd.DataFrame(rows)
    return df

# Response distribution analysis
def analyze_response_distribution(df, output_folder):
    # Agrupamos los datos y aseguramos que el resultado sea un DataFrame
    response_dist = (
        df.groupby(['model', 'test', 'lang', 'response'])
        .size().reset_index(name='count')  # Resetear índice para convertir en DataFrame
    )
    
    # Realizamos el gráfico de barras con Seaborn
    plt.figure(figsize=(12, 8))
    sns.barplot(data=response_dist, x="response", y="count", hue="lang")
    plt.title("Response Distribution by Model and Language")

    # Guardamos los resultados en archivos
    plt.savefig(f"{output_folder}/response_distribution.png")
    response_dist.to_csv(f"{output_folder}/response_distribution.csv", index=False)
    plt.close()

# Test comparison analysis
def analyze_test_comparison(df,  output_folder):
    # Asegúrate de que las columnas necesarias existen en el DataFrame
    if 'test' not in df.columns:
        raise ValueError("La columna 'test' no está presente en el DataFrame.")
    if 'response' not in df.columns:
        raise ValueError("La columna 'response' no está presente en el DataFrame.")
    
    # Calcula las comparaciones del test, asegurándonos de que los valores estén presentes
    test_comparison = df.groupby(['test', 'response']).size().reset_index(name='count')

    # Calcula el porcentaje para cada respuesta dentro de cada test
    total_responses_per_test = test_comparison.groupby('test')['count'].transform('sum')
    test_comparison['percentage'] = (test_comparison['count'] / total_responses_per_test) * 100
    
    # Verifica si 'test' está presente antes de continuar
    print(test_comparison.columns)  # Verifica que 'test' y otras columnas estén presentes

    # Realiza el gráfico de barras con Seaborn
    try:
        sns.barplot(data=test_comparison, x="test", y="percentage", hue="response")
        plt.title("Comparación de Test por Respuesta")
        plt.show()
    except ValueError as e:
        print(f"Error al intentar graficar: {e}")
        
# Language discrepancy analysis
def analyze_language_discrepancies(df):
    """ language_diff = df.pivot_table(
        index=['model', 'question'], columns='lang', values='response', aggfunc=lambda x: x.iloc[0]
    ).reset_index()
    discrepancies = language_diff[language_diff['en'] != language_diff['es']]
    discrepancies.to_csv(f"{output_folder}/language_discrepancies.csv", index=False)
    print("Language discrepancies saved in language_discrepancies.csv") """
    # Pivot table para obtener las respuestas por idioma ('en' y 'es')
    language_diff = df.pivot_table(
        index=['model', 'question'], columns='lang', values='response', aggfunc=lambda x: x.iloc[0]
    ).reset_index()

    # Imprime las columnas para depuración
    print("Columnas del DataFrame pivotado:", language_diff.columns)

    # Verifica que las columnas 'en' y 'es' estén presentes
    if 'en' not in language_diff.columns or 'es' not in language_diff.columns:
        raise ValueError("Las columnas 'en' y/o 'es' no están presentes en el DataFrame pivotado.")
    
    # Filtra las discrepancias entre los idiomas 'en' y 'es'
    discrepancies = language_diff[language_diff['en'] != language_diff['es']]

    # Si no hay discrepancias, mostrar un mensaje informativo
    if discrepancies.empty:
        print("No se encontraron discrepancias entre los idiomas.")
    else:
        # Guarda el resultado en un archivo CSV
        discrepancies.to_csv(f"{output_folder}/language_discrepancies.csv", index=False)
        print("Language discrepancies saved in language_discrepancies.csv")

# Failure rate analysis
def analyze_failure_rate(df):
    failure_rate = df[df['is_failure']].groupby(['model', 'test', 'lang']).size().reset_index(name='failure_count')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=failure_rate, x="model", y="failure_count", hue="language")
    plt.title("Failure Rate by Model, Test, and Language")
    plt.savefig(f"{output_folder}/failure_rate.png")
    failure_rate.to_csv(f"{output_folder}/failure_rate.csv", index=False)
    plt.close()

# Run analyses and save results

# Example usage
root_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"
df = load_data(root_folder)
print("head", df.head())

""" # Ensure DataFrame isn't empty before analysis
if not df.empty:
    analyze_consensus_time(df)
else:
    print("No data found. Please check the folder structure and JSON file contents.")


output_folder = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina/outcomes"

analyze_consensus_time(df)
analyze_response_distribution(df, output_folder)
analyze_test_comparison(df, output_folder)
analyze_language_discrepancies(df)
analyze_failure_rate(df) """