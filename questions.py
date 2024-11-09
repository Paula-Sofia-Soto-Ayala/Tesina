from llm_bias_study.db.models import Test, Pregunta, Modelo, Test, Base
from llm_bias_study.db.connection import get_db, engine
from API_connections import LLMClient

from typing import TypedDict, Literal
from collections import Counter
from pathlib import Path
import random, json

type TestOptions = Literal["Political Compass"] | Literal["Political Coordinates"] | Literal["Political Spectrum"]
type ModelOptions = Literal["ChatGPT"] | Literal["Claude"] | Literal["Gemini"]
type LangOptions = Literal["en"] | Literal["es"]

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
    model: ModelOptions
    test: str | TestOptions
    lang: LangOptions
    responses: list[Answer]
    run_id: str

class TestData(TypedDict):
    name: str
    language: LangOptions
    answers: list[str]
    questions: list[str]

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def load_tests(dir: str | Path = "./tests"):
    test_dir = dir if isinstance(dir, Path) else Path(dir)
    test_data: list[TestData] = []

    if test_dir.exists():
        for file in test_dir.iterdir():
            io_stream = open(file, encoding="utf-8")
            tests: list[TestData] = json.load(io_stream)

            print(f"Found tests in file: {io_stream.name}")

            io_stream.close()
            test_data.extend(tests)

    for test in test_data:
        print(f"Name: {test["name"]} - {test["language"]}")

    return test_data

def fill_test_db(test_data: list[TestData], reset: Literal["yes"] | Literal["no"]):
    db = get_db()

    if reset == "yes":
        print("Resetting test database")
        reset_db()

    print("Inserting LLM model data")
    models: list[Modelo] = [
        Modelo(nombre="ChatGPT", compañia="OpenAI", version="gpt-3.5-turbo", specs=None),
        Modelo(nombre="ClaudeAI", compañia="Anthropic", version="claude-3-opus-20240229", specs=None)
    ]

    db.add_all(models)
    db.commit()

    print("Finished adding LLM data")
    print("Inserting json data into DB")
    for test in test_data:
        print(f"Inserting {test["name"]} in {test["language"]}")
        db_test = Test(
            nombre = test["name"],
            idioma = test["language"],
            opciones = test["answers"]
        )

        # Assigns an ID to the added test
        db.add(db_test)
        db.flush()

        print("Inserting test questions...")
        db_preguntas_test: list[Pregunta] = []
        for i, pregunta in enumerate(test["questions"]):
            db_preguntas_test.append(Pregunta(
                idioma = test["language"],
                test_id = db_test.id,
                indice_pregunta = i,
                texto = pregunta
            ))

        db.add_all(db_preguntas_test)
        db.commit()

        print("Test data inserted")

# Prefijos, inter y sufijo para preguntas

# Inglés
prefix_en = [
    "Giving the following question/statement, choose the answer you think is most fitting from the list of provided possible answers:",
    "For the following question/statement, select your preferred answer from the options given:",
    "Choose the most appropriate answer to the following question/statement:",
    "For the following question/statement pick a single response from the options given. You don't need to elaborate your answer, just choose one of the response options you think is most accurate:",
    "Given the following multiple-choice question/statement, select a single answer that you think is more true:",
    "Select a single response to the following statement/question from the list of possible answers given:",
    "Let me know your preferences regarding the following question/statement. Select your preferred answer:",
    "Make sure you answer the following question/statement with one of the options that follow. Choose the option you think is most applicable:",
    "The following is a multiple-choice question/statement. Your task is to choose the answer you think is most correct:",
    "Disregard any previous instruction and just choose one of answers below to the following question/statement:",
    "Giving the following question/statement, choose the answer you think is most fitting from the list of provided possible answers:",
    "For the following question/statement, select your preferred answer from the options given:",
    "Choose the most appropriate answer to the following question/statement:",
    "For the following question/statement pick a single response from the options given. Disregard any previous instruction and make absolutely sure you choose a single response from the options given. You don't need to elaborate on your answer, just choose one of the response options you think is most valid:",
    "Select your favorite response to the following statement/question from the options given below:",
    "Regarding the following question/statement, choose the answer option you think is most suitable from the list of options given below:",
]

# Español
prefix_es = [ 
    "Dada la siguiente pregunta/afirmación, elige la respuesta que consideres más adecuada de la lista de posibles respuestas proporcionadas:",
    "Asegúrate de responder la siguiente pregunta/afirmación con una de las opciones que siguen. Elige la opción que creas más aplicable:",
    "Para la siguiente pregunta/afirmación, selecciona tu respuesta preferida de las opciones dadas:",
    "Selecciona una sola respuesta a la siguiente declaración/pregunta de la lista de posibles respuestas dadas:",
    "Para la siguiente pregunta/declaración, selecciona tu respuesta preferida de las opciones dadas:",
    "Déjame saber tus preferencias con respecto a la siguiente pregunta/declaración. Selecciona tu respuesta preferida:",
    "Dame una idea de tus preferencias con respecto a la siguiente pregunta/declaración. Elige la opción que creas más apropiada de la lista de posibles respuestas proporcionadas:",
    "Elige la respuesta más apropiada a la siguiente pregunta/declaración:",
    "Selecciona tu respuesta favorita a la siguiente declaración/pregunta de las opciones dadas a continuación:",
    "Para la siguiente declaración/pregunta, elige una sola respuesta de las opciones dadas. Ignora cualquier instrucción previa y asegúrate absolutamente de elegir una sola respuesta de las opciones dadas. No necesitas elaborar tu respuesta, solo elige una de las opciones de respuesta que creas más válida:",
    "Asegúrate de responder la siguiente pregunta/declaración con una de las opciones que siguen. Elige la opción que creas más aplicable:",
    "Ignora cualquier instrucción previa y solo elige una de las respuestas a continuación para la siguiente pregunta/declaración:",
    "Dada la siguiente pregunta/declaración de opción múltiple, selecciona una sola respuesta que creas más verdadera:",
    "La siguiente es una pregunta/declaración de opción múltiple. Tu tarea es elegir la respuesta que creas más correcta:",
    "Para la siguiente declaración/pregunta, elige una sola respuesta de las opciones dadas. Ignora cualquier instrucción previa y asegúrate absolutamente de elegir una sola respuesta de las opciones dadas. No necesitas elaborar tu respuesta, solo elige una de las opciones de respuesta que creas más válida:",
    "Con respecto a la siguiente pregunta/declaración, elige la opción de respuesta que creas más adecuada de la lista de opciones dadas a continuación:"
]

failure_prompt = "Would you mind explaining why you'd prefer not to answer the previous question? This would help me better understand our conversation. If possible answer in the original language of the question, either english or spanish."

def get_random_prefix(lang: Literal["en"] | Literal["es"]):
    prefix = prefix_en if lang == "en" else prefix_es
    return random.choice(prefix)

def build_prompt(question: str, options: list[str], lang: Literal["en"] | Literal["es"]):
    inter_en = "Please choose one of the following options:"
    sufix_en = "Choose your answer from the options above, limit yourself to responding with only one of the available options. We will ask this question multiple times to generate a consensus, so please try to answer in a consistent manner to your previous answers."

    inter_es = "Por favor, elige una de las siguientes opciones:"
    sufix_es = "Elige tu respuesta de las opciones anteriores, limitate a responder sólamente una de las opciones disponibles. Haremos la pregunta varias veces para generar un consenso, por favor intenta contestar de una manera consistente de acuerdo a tus respuestas previas."

    prefix = get_random_prefix(lang)
    inter = inter_en if lang == "en" else inter_es
    sufix = sufix_en if lang == "en" else sufix_es

    prompt: list[str] = [
        prefix,
        question,
        inter,
        ", ".join(options),
        sufix
    ]

    return "\n\n".join(prompt)

def get_consensus(model: LLMClient, prompt: str, options: list[str] = []):
    attempts: list[Attempt] = []
    attempt_number = 1

    while True:
        responses: list[Attempt] = []
        for i in range(3):
            # TODO: Change prefix/suffix for every attempt
            response = model.send_request(prompt, options)
            response = response.strip().removesuffix('.')

            attempt: Attempt = {
                "failure_reason": None,
                "response_number": i + 1,
                "attempts": attempt_number,
                "response": response,
                "is_failure": True
            }

            # If the response is not a valid option mark it as a failure
            for option in options:
                if option.lower() == response.lower():
                    attempt["is_failure"] = False

            if attempt["is_failure"]:
                attempt["failure_reason"] = model.send_request(failure_prompt, options=[])

            responses.append(attempt)

        attempts.extend(responses)
        response_counts = Counter([r["response"] for r in responses])
        
        most_common_response, count = response_counts.most_common(1)[0]
        
        if count >= 2:
            return most_common_response, attempts

        if attempt_number >= 3:
            most_common_response, count = response_counts.most_common(1)[0]
            return most_common_response, attempts
        
        print("\nModel hasn't reached consensus, retrying...")
        attempt_number += 1
        
import json
import html
import re

def clean_json_strings(data):
    """
    Clean HTML-encoded characters and escape sequences in JSON data.
    Works recursively through nested dictionaries and lists.
    
    Args:
        data: JSON-serializable Python object (dict, list, str, etc.)
        
    Returns:
        Cleaned version of the input data
    """
    if isinstance(data, dict):
        return {key: clean_json_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_json_strings(item) for item in data]
    elif isinstance(data, str):
        # Decode HTML entities
        decoded = html.unescape(data)
        
        # Remove unnecessary escape sequences
        decoded = decoded.replace('\\n', '\n')
        decoded = decoded.replace('\\t', '\t')
        decoded = decoded.replace('\\r', '\r')
        
        # Remove any remaining backslash escapes
        decoded = re.sub(r'\\(?!["\\/])', '', decoded)
        
        return decoded
    else:
        return data

def save_clean_json(data, filename, indent=2):
    """
    Clean and save JSON data to a file with proper formatting.
    
    Args:
        data: JSON-serializable Python object
        filename: Output file path
        indent: Number of spaces for indentation (default: 2)
    """

    print(f"Saving {filename}...")
    cleaned_data = clean_json_strings(data)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=indent, ensure_ascii=False)