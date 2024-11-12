import os, json
from questions import TestData, TestRun

def load_test_data(file_path: str) -> TestRun:
    # Carga los datos JSON de un archivo con codificación UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

test_folder = './Gemini/Political Spectrum Quiz/es/results'
result_path = './tests/political_spectrum_data.json'

result_json = open(file=result_path, mode='+r', encoding='utf-8')
result_list: list[TestData] = json.load(result_json)
correct_questions = result_list[1]['questions']

for file_name in os.listdir(test_folder):
    if file_name.endswith('.json'):
        test_path = os.path.join(test_folder, file_name)
        copy_path = os.path.join(test_folder, "copy_" + file_name)
        test = load_test_data(test_path)
        
        print(f'{test['test']} - {test['lang']}')
        print(f'{test['model']} - {test['run_id']}')

        for index, response in enumerate(test['responses']):
            response['question'] = correct_questions[index]
            copy = open(copy_path, 'w', encoding='utf-8') 
            json.dump(test, copy, indent=4, ensure_ascii=False)