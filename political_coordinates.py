from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from questions import build_prompt, get_consensus, Answer, TestRun
from questions import LangOptions, ModelOptions
from API_connections import LLMClient
from uuid import uuid4

import json, datetime

options_en = {
    "strongly disagree": "0",
    "disagree": "1",
    "neutral": "2",
    "agree": "3",
    "strongly agree": "4"
}

options_es = {
    "totalmente en desacuerdo": "0",
    "en desacuerdo": "1",
    "neutral": "2",
    "de acuerdo": "3",
    "totalmente de acuerdo": "4"
}

es_url = 'https://www.idrlabs.com/es/coordenadas-politicas/prueba.php'
en_url = 'https://www.idrlabs.com/political-coordinates/test.php'

def setInputValue(driver: WebDriver, el: WebElement, val: str):
    driver.execute_script("arguments[0].value = arguments[1]", el, val)

def run_political_coords(model: LLMClient, lang: LangOptions, model_name: ModelOptions):
    test_url = es_url if lang == 'es' else en_url
    test: TestRun = {
        'run_id': str(uuid4()),
        'test': "Political Coordinates Test",
        'model': model_name,
        "lang": lang,
        'responses': [],
    }
    driver = webdriver.Edge()
    driver.get(test_url)

    print(f'On page: {driver.title}')

    # Wait for the ads to be visible before dismissing them
    curr_question = 1
    wait = WebDriverWait(driver, 5)
    page_ad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.adthrive-close')))
    page_ad.click()

    while True:
        # Check if we're at the end of the test, and the result is visible
        result_container = driver.find_elements(By.CSS_SELECTOR, 'div.test-contain.political.result')
        result = result_container[0] if len(result_container) > 0 else None

        if result:
            # If there is a result take a screenshot and save it
            today = datetime.datetime.now()
            # Write the screenshot with its corresponding timestamp
            result_path = f'./results/{lang}/political_coords_{today.date()}_{test["run_id"]}'

            with open(f'{result_path}.png', 'wb') as img_file:
                img_file.write(result.screenshot_as_png)

            with open(f'{result_path}.json', 'wt') as result_file:
                result_file.write(json.dumps(test, indent=4))

            break

        # Otherwise get the question's text and input element
        question_text = driver.find_element(By.CSS_SELECTOR, 'p.question').text
        question_input = driver.find_element(By.CSS_SELECTOR, 'input[name="answer"]')
        question_options = options_es if lang == 'es' else options_en
        next_button = driver.find_element(By.CSS_SELECTOR, 'span.qnav.next')

        question_prompt = build_prompt(question=question_text, options=question_options, lang=lang)
        question_answer, question_attempts = get_consensus(model, question_prompt)
        question_answer = question_answer.lower().rstrip().removesuffix('.')

        print(f"\n{curr_question}. Question: {question_text}")
        print(f"Respuesta: {question_answer}")

        # Set its value to the LLM answer
        # TODO: Change input value to test response
        input_val = question_options[question_answer] or '2'
        setInputValue(driver, el=question_input, val=input_val)

        answer: Answer = {
            "attemps": question_attempts,
            "prompt": question_prompt,
            "question": question_text,
            "response": question_answer
        }

        # Click the input and move to the next question
        test['responses'].append(answer)
        next_button.click()
        curr_question += 1
        sleep(0.25)

    # Close the browser
    driver.quit()