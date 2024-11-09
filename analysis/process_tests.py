import os
import pandas as pd
from load_data import process_test_files

models = ['ChatGPT', 'Claude', 'Gemini']
tests = ['Political Compass Test', 'Political Coordinates Test', 'Political Spectrum Quiz']
langs = ['en', 'es']

base_dir = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"

def process_all_data():
    all_data = []

    # Recorre todos los modelos, tests e idiomas
    for model in models:
        for test in tests:
            for lang in langs:
                test_folder = f'{base_dir}/{model}/{test}/{lang}/results/'
                test_data = process_test_files(test_folder, model, test, lang)
                all_data.extend(test_data)

    # Crear el DataFrame con todos los datos
    df = pd.DataFrame(all_data)
    return df

if __name__ == "__main__":
    df = process_all_data()
    df.to_csv('resultados_completos.csv', index=False)
    print("Datos procesados y guardados en 'resultados_completos.csv'.")
