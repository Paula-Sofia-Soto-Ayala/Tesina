import os
import json
from typing import TypedDict

# Class for an LLM response attempt for a particular question
class Attempt(TypedDict):
    failure_reason: str | None
    response_number: int
    is_failure: bool
    response: str
    attempts: int

# Class for a test answer, includes the question, its response, and the prompt used by the LLM.
class Answer(TypedDict):
    importance_attempts: list[Attempt] | None
    importance: str | None
    attemps: list[Attempt]
    question: str
    response: str
    prompt: str

# Class for a test run file, includes a list of responses and a test ID
class TestRun(TypedDict):
    responses: list[Answer]
    run_id: str
    model: str
    test: str
    lang: str

def load_test_data(file_path: str) -> TestRun:
    # Carga los datos JSON de un archivo con codificación UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def parse_response_data(data: TestRun, model: str, test: str, lang: str):
    #Procesa los datos del JSON y los convierte en formato adecuado para el DataFrame.
    rows = []
    
    for index, answer in enumerate(data['responses']):
        for attempt in answer['attemps']:
            row = {
                'Id': index,
                'Modelo': model,
                'Test': test,
                'Idioma': lang,
                'Pregunta': answer['question'],
                'Respuesta': attempt['response'],
                'Es fallo': attempt['is_failure'],
                'Intentos': attempt['response_number'],
                'Importancia': answer.get('importance', None),
                'Intentos Importancia': len(answer.get('importance_attempts') or [])
            }
            rows.append(row)
    return rows

def process_test_files(test_folder: str, model: str, test_name: str, lang: str):
    #Recorre los archivos JSON dentro de una carpeta de test y extrae la información.

    if test_name == "Political Spectrum Quiz" and lang == "es":
        tests: list[TestRun] = []
        for file_name in os.listdir(test_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(test_folder, file_name)
                test = load_test_data(file_path)
                tests.append(test)

        return process_spectrum_test_es(tests, model, test_name, lang)

    data_rows = []
    for file_name in os.listdir(test_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(test_folder, file_name)
            test = load_test_data(file_path)
            data_rows.extend(parse_response_data(test, model, test_name, lang))

    return data_rows

def process_spectrum_test_es(tests: list[TestRun], model: str, name: str, lang: str):
    unique_questions: dict[int, str] = {}

    for id, answer in enumerate(tests[0]['responses']):
        unique_questions[id] = answer['question']

    for test in tests:
        for id, response in enumerate(test['responses']):
            response['question'] = unique_questions[id]

    results = []

    for test in tests:
        results.extend(parse_response_data(test, model, name, lang))

    return results

'''
def parse_response_data(data, model, test, lang):
    """Procesa los datos del JSON y los convierte en formato adecuado para el DataFrame."""
    rows = []
    
    for item in data['responses']:
        # Dependiendo del test, procesamos de una manera distinta
        if test == "Political Compass Test":
            for attempt in item['attemps']:
                row = {
                    'Modelo': model,
                    'Test': test,
                    'Idioma': lang,
                    'Pregunta': item['question'],
                    'Respuesta': attempt['response'],
                    'Intentos': attempt['response_number'],
                    'Es fallo': attempt['is_failure'],
                    'Importancia': None  # No aplica para este test
                }
                rows.append(row)

        elif test == "Political Coordinates Test":
            for attempt in item['attemps']:
                row = {
                    'Modelo': model,
                    'Test': test,
                    'Idioma': lang,
                    'Pregunta': item['question'],
                    'Respuesta': attempt['response'],
                    'Intentos': attempt['response_number'],
                    'Es fallo': attempt['is_failure'],
                    'Importancia': None  # No aplica para este test
                }
                rows.append(row)

        elif test == "Political Spectrum Quiz":
            for attempt, importance_attempt in zip(item['attemps'], item['importance_attempts']):
                row = {
                    'Modelo': model,
                    'Test': test,
                    'Idioma': lang,
                    'Pregunta': item['question'],
                    'Respuesta': attempt['response'],
                    'Intentos': attempt['response_number'],
                    'Es fallo': attempt['is_failure'],
                    'Importancia': importance_attempt['response']  # Aquí usamos la importancia
                }
                rows.append(row)
    
    return rows

def process_test_files(test_folder, model, test_name, lang):
    """Recorre los archivos JSON dentro de una carpeta de test y extrae la información."""
    data_rows = []
    for file_name in os.listdir(test_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(test_folder, file_name)
            data = load_json_data(file_path)
            data_rows.extend(parse_response_data(data, model, test_name, lang))
    return data_rows
'''

""" # Define la carpeta donde se encuentran los archivos JSON
test_folder = 'path_to_data/ChatGPT/Political Compass Test/en/results/'

# Define los parámetros
model = 'ChatGPT'
test_name = 'Political Compass Test'
lang = 'en'

# Procesa los archivos JSON en esa carpeta
processed_data = process_test_files(test_folder, model, test_name, lang)

# Si quieres ver los datos procesados
print(processed_data)
  """
 
""" import json
import os
import pandas as pd

# Define the directory paths (edit as needed)
base_dir = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"

# Load JSON files and parse based on test type
def load_responses(test_folder):
    data = []
    for filename in os.listdir(test_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(test_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                record = json.load(file)
                
                test_type = record["test"]
                model = record["model"]
                lang = record["lang"]
                run_id = record["run_id"]

                for response_data in record["responses"]:
                    question = response_data["question"]
                    prompt = response_data["prompt"]
                    final_response = response_data["response"]
                    
                    # Distinguish processing based on test type
                    if test_type == "Political Spectrum Quiz":
                        # Spectrum Quiz includes 'importance' data
                        importance = response_data.get("importance", None)
                        importance_attempts = response_data.get("importance_attempts", [])
                    else:
                        # Compass and Coordinates Tests do not have 'importance'
                        importance = None
                        importance_attempts = []

                    # Extract attempts data for responses
                    attempts = []
                    for attempt in response_data["attemps"]:
                        attempts.append({
                            "response_number": attempt["response_number"],
                            "attempts": attempt["attempts"],
                            "response": attempt["response"],
                            "is_failure": attempt["is_failure"]
                        })

                    # Append processed data to main list
                    data.append({
                        "run_id": run_id,
                        "test": test_type,
                        "model": model,
                        "lang": lang,
                        "question": question,
                        "prompt": prompt,
                        "final_response": final_response,
                        "importance": importance,
                        "importance_attempts": importance_attempts,
                        "attempts": attempts
                    })
    return data

# Usage example for loading specific test folders
compass_data = load_responses(os.path.join(base_dir, "Political Compass Test"))
coordinates_data = load_responses(os.path.join(base_dir, "Political Coordinates Test"))
spectrum_data = load_responses(os.path.join(base_dir, "Political Spectrum Quiz"))

# Convert to DataFrames for analysis
compass_df = pd.DataFrame(compass_data)
coordinates_df = pd.DataFrame(coordinates_data)
spectrum_df = pd.DataFrame(spectrum_data)

# Print sample of data loaded
print("Compass Test Data Sample:")
print(compass_df.head())
print("\nCoordinates Test Data Sample:")
print(coordinates_df.head())
print("\nSpectrum Test Data Sample:")
print(spectrum_df.head())
 """
 
""" import json
import os
import pandas as pd

# Define los directorios base y de salida
base_dir = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina"
output_dir = "C:/Users/sofo-/OneDrive/Documentos/Tesina/Tesina/processed_data"

# Crea el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Función para cargar respuestas desde un directorio de pruebas
def load_responses(test_folder):
    data = []
    for filename in os.listdir(test_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(test_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                record = json.load(file)
                
                # Extraer información principal
                test_type = record.get("test", "Unknown")
                model = record.get("model", "Unknown")
                lang = record.get("lang", "Unknown")
                run_id = record.get("run_id", "Unknown")

                # Procesar cada respuesta en el archivo
                for response_data in record.get("responses", []):
                    question = response_data.get("question", "Unknown")
                    prompt = response_data.get("prompt", "Unknown")
                    final_response = response_data.get("response", "Unknown")

                    # Datos específicos para el Political Spectrum Quiz
                    if test_type == "Political Spectrum Quiz":
                        importance = response_data.get("importance", None)
                        importance_attempts = response_data.get("importance_attempts", [])
                    else:
                        importance = None
                        importance_attempts = []

                    # Procesar cada intento
                    attempts = []
                    for attempt in response_data.get("attemps", []):
                        attempts.append({
                            "response_number": attempt.get("response_number"),
                            "attempts": attempt.get("attempts"),
                            "response": attempt.get("response"),
                            "is_failure": attempt.get("is_failure")
                        })

                    # Añadir los datos procesados a la lista principal
                    data.append({
                        "run_id": run_id,
                        "test": test_type,
                        "model": model,
                        "lang": lang,
                        "question": question,
                        "prompt": prompt,
                        "final_response": final_response,
                        "importance": importance,
                        "importance_attempts": importance_attempts,
                        "attempts": attempts
                    })
    return data

# Cargar datos desde las carpetas de cada modelo y tipo de prueba
all_data = []
models = ["ChatGPT", "Claude", "Gemini"]
tests = ["Political Compass Test", "Political Coordinates Test", "Political Spectrum Quiz"]

for model in models:
    for test in tests:
        test_folder = os.path.join(base_dir, model, test, "en/results")
        if os.path.exists(test_folder):
            print(f"Cargando datos desde {test_folder}")
            data = load_responses(test_folder)
            all_data.extend(data)

# Convertir los datos cargados en un DataFrame
df = pd.DataFrame(all_data)

# Imprimir las columnas y una muestra de datos para verificar
print("Columnas del DataFrame:", df.columns)
print("Muestra de datos cargados:")
print(df.head())

# Verificar si 'model' y 'test' están presentes en el DataFrame
if 'model' not in df.columns or 'test' not in df.columns:
    print("Error: Las columnas 'model' o 'test' no están presentes en el DataFrame.")
else:
    # Guardar el DataFrame completo en un archivo CSV en el directorio de salida
    df.to_csv(os.path.join(output_dir, "all_models_data.csv"), index=False, encoding='utf-8')

    # Guardar archivos CSV separados por modelo y tipo de prueba
    for model in df['model'].unique():
        for test in df['test'].unique():
            # Filtrar el DataFrame para el modelo y el tipo de prueba actual
            filtered_df = df[(df['model'] == model) & (df['test'] == test)]
            
            # Definir el nombre del archivo basado en el modelo y tipo de prueba
            filename = f"{model}_{test.replace(' ', '_')}.csv"
            
            # Guardar el archivo CSV
            filtered_df.to_csv(os.path.join(output_dir, filename), index=False, encoding='utf-8')

    # Mensajes de éxito
    print("Datos procesados y guardados correctamente.")
    print("Ubicación de los archivos CSV:", output_dir) """

""" # Llama a la función y carga los datos
data = load_responses_by_model(base_dir)

# Convierte los datos a un DataFrame para su análisis
df = pd.DataFrame(data)

# Muestra una muestra de los datos cargados
print("Data Sample:")
print(df.head()) """
