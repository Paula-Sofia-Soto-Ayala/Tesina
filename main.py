from sqlalchemy.orm import Session
from API_connections import chatgpt_client, claude_client, llama_client
from llm_bias_study.db.connection import get_db
from llm_bias_study.db.models import Modelo, Pregunta, Respuesta
from questions import build_prompt
from collections import Counter
import json, sys, os, uuid
        
def load_tests():
    try:
        with open('tests/political_compass_data.json', 'r', encoding='utf-8') as file:
            political_compass_test = json.load(file)
        with open('tests/political_coordinates_data.json', 'r', encoding='utf-8') as file:
            political_coordinates_test = json.load(file)
        with open('tests/political_spectrum_data.json', 'r', encoding='utf-8') as file:
            political_spectrum_quiz = json.load(file)
        return [political_compass_test, political_coordinates_test, political_spectrum_quiz]
    except Exception as e:
        print(f"Error al cargar los tests: {e}")
        sys.exit()
        
def main_menu():
    print("Seleccione un modelo de lenguaje:")
    print("1. ChatGPT")
    print("2. Claude")
    print("3. LLaMA")
    choice = input("Ingrese el número de su elección: ")
    return choice

def test_menu(tests):
    print("Seleccione un test de orientación política:")
    for i, test in enumerate(tests):
        print(f"{i + 1}. {test[0]['name']}")
    choice = int(input("Ingrese el número de su elección: ")) - 1
    return tests[choice]

def language_menu(test):
    print(f"Seleccione el idioma para el {test[0]['name']}:")
    languages = list(set([t['language'] for t in test]))
    for i, lang in enumerate(languages):
        print(f"{i + 1}. {lang.capitalize()}")
    choice = int(input("Ingrese el número de su elección: ")) - 1
    selected_language = languages[choice]
    return [t for t in test if t['language'] == selected_language][0]

""" def save_response_to_db(session: Session, respuesta_raw: str, respuesta: str, pregunta_id: int, modelo_id: int) -> None:
    nueva_respuesta = Respuesta(
        respuesta_raw=respuesta_raw,
        respuesta=respuesta,
        pregunta_id=pregunta_id,
        modelo_id=modelo_id
    )
    session.add(nueva_respuesta)
    session.commit() """
    
def save_response(model_name: str, test_name: str, language: str, run_id: str, question: str, prompt: str, response: str, attempts: list):
    directory = f"./{model_name}/{test_name}/{language}/answers"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "responses.json")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    run_entry = next((item for item in data if 'run_id' in item and item["run_id"] == run_id), None)
    if not run_entry:
        run_entry = {"run_id": run_id, "responses": []}
        data.append(run_entry)

    response_content = response.content if hasattr(response, 'content') else str(response)

    run_entry["responses"].append({
        "question": question,
        "prompt": prompt,
        "response": response_content,
        "attempts": attempts
    })

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

        
""" def save_response(model_name: str, test_name: str, language: str, run_id: str, question: str, prompt: str, response: str):
    directory = f"./{model_name}/{test_name}/{language}/answers"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "responses.json")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []
        
    run_entry = next((item for item in data if 'run_id' in item and item["run_id"] == run_id), None)
    if not run_entry:
        run_entry = {"run_id": run_id, "responses": []}
        data.append(run_entry)


    # Extraer el contenido de la respuesta
    response_content = response.content if hasattr(response, 'content') else str(response)

    run_entry["responses"].append({
        "question": question,
        "prompt": prompt,
        "response": response_content
    })

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)   """ 
        
def get_consensus_response(model, prompt):
    attempts = []
    attempt_number = 1
    while True:
        responses = []
        for i in range(3):
            response = model.send_request(prompt).content
            responses.append({"attempt": attempt_number, "response_number": i + 1, "response": response})
        attempts.extend(responses)
        
        response_counts = Counter([r["response"] for r in responses])
        most_common_response, count = response_counts.most_common(1)[0]
        if count >= 2:
            return most_common_response, attempts
        print("No consensus reached, repeating the questions...")
        attempt_number += 1

        
""" def get_consensus_response(model, prompt):
    while True:
        responses = [model.send_request(prompt).content for _ in range(3)]
        response_counts = Counter(responses)
        most_common_response, count = response_counts.most_common(1)[0]
        if count >= 2:
            return most_common_response
        print("No consensus reached, repeating the questions...") """
        
def run_test(model_name: str, model, selected_test_language: dict):
    run_id = str(uuid.uuid4())
    print(f"Has seleccionado el test: {selected_test_language['name']} en {selected_test_language['language']}")
    
    for question in selected_test_language['questions']:
        prompt = build_prompt(question, selected_test_language['answers'], selected_test_language['language'])
        print(f"Enviando prompt: {prompt}")
        response, attempts = get_consensus_response(model, prompt)
        print(f"Respuesta: {response}")
        save_response(model_name, selected_test_language['name'], selected_test_language['language'], run_id, question, prompt, response, attempts)

    print("Todas las preguntas han sido enviadas y las respuestas guardadas.")


""" def run_test(model_name: str, model, selected_test_language: dict):
    run_id = str(uuid.uuid4())
    print(f"Has seleccionado el test: {selected_test_language['name']} en {selected_test_language['language']}")
    
    for question in selected_test_language['questions']:
        prompt = build_prompt(question, selected_test_language['answers'], selected_test_language['language'])
        print(f"Enviando prompt: {prompt}")
        response = get_consensus_response(model, prompt)
        print(f"Respuesta: {response}")
        save_response(model_name, selected_test_language['name'], selected_test_language['language'], run_id, question, prompt, response)

    print("Todas las preguntas han sido enviadas y las respuestas guardadas.")  """   

def main():
    print("Cargando tests...")
    tests = load_tests()
    print("Tests cargados.")
    
    print("Mostrando menú de modelos...")
    model_choice = main_menu()
    print(f"Modelo seleccionado: {model_choice}")
    
    print("Mostrando menú de tests...")
    selected_test = test_menu(tests)
    print(f"Test seleccionado: {selected_test[0]['name']}")
    
    print("Mostrando menú de idiomas...")
    selected_test_language = language_menu(selected_test)
    print(f"Idioma seleccionado: {selected_test_language['language']}")
    
    if model_choice == '1':
        model = chatgpt_client
        model_name = "ChatGPT"
    elif model_choice == '2':
        model = claude_client
        model_name = "Claude"
    elif model_choice == '3':
        model = llama_client
        model_name = "Llama"
    else:
        print("Opción no válida")
        sys.exit()
        
    run_test(model_name, model, selected_test_language)
    
    """ db = get_db()
    modelo = db.query(Modelo).filter(Modelo.nombre == model_name).first()
    if not modelo:
        print(f"Modelo {model_name} no encontrado en la base de datos.")
        sys.exit()

    print(f"Has seleccionado el test: {selected_test_language['name']} en {selected_test_language['language']}")
    for question in selected_test_language['questions']:
        prompt = build_prompt(question, selected_test_language['answers'], selected_test_language['language'])
        print(f"Enviando prompt: {prompt}")
        response = model.send_request(prompt)
        print(f"Respuesta: {response}")

        pregunta = db.query(Pregunta).filter(Pregunta.texto == question, Pregunta.idioma == selected_test_language['language']).first()
        if pregunta:
            save_response_to_db(db, response, response, pregunta.id, modelo.id)

    print("Todas las preguntas han sido enviadas y las respuestas guardadas.") """

if __name__ == "__main__":
    main()

