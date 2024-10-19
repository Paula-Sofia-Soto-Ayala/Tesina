import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from typing import TypedDict

import json, datetime

def getRespuesta(val: str) -> str:
    opciones = {
        "0": "Strongly disagree",
        "1": "Disagree",
        "2": "Neutral",
        "3": "Agree",
        "4": "Strongly agree"
    }

    return opciones.get(val) or "Invalid Option"

def setInputValue(el: WebElement, val: str):
    driver.execute_script("arguments[0].value = arguments[1]", el, val)

# Class for a test answer, includes the question, its response, and the prompt used by the LLM.
class Answer(TypedDict):
    question: str
    response: str
    prompt: str

# Class for a test run file, includes a list of responses and a test ID
class TestRun(TypedDict):
    responses: list[Answer]
    run_id: str

es_url = 'https://www.idrlabs.com/es/coordenadas-politicas/prueba.php'
en_url = 'https://www.idrlabs.com/political-coordinates/test.php'
test: TestRun = {}
language = 'en'
test_url = es_url if language == 'es' else en_url

# Load the JSON file
with open('responses.json', 'r', encoding='utf-8') as file:
    test = json.load(file)

edge_options = webdriver.EdgeOptions()
edge_options.add_extension("./ublock.crx")
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
        with open(f'./results/{language}/political_coords_{today.date()}_{test["run_id"]}.png', 'wb') as img_file:
            img_file.write(result.screenshot_as_png)

        break

    # Otherwise get the question's text and input element
    question_text = driver.find_element(By.CSS_SELECTOR, 'p.question').text
    question_input = driver.find_element(By.CSS_SELECTOR, 'input[name="answer"]')
    next_button = driver.find_element(By.CSS_SELECTOR, 'span.qnav.next')

    question_answer = str(random.randint(0, 4))

    print(f"\n{curr_question}. Question: {question_text}")
    print(f"Respuesta: {getRespuesta(question_answer)}")

    # Set its value to the LLM answer
    # TODO: Change input value to test response
    setInputValue(question_input, question_answer)

    # Click the input and move to the next question
    next_button.click()
    curr_question += 1
    sleep(0.5)

# Close the browser
driver.quit()
