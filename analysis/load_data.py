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

