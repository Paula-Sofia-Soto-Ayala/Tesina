from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from typing import Literal
from API_connections import LLMClient, chatgpt_client
from questions import build_prompt
from uuid import uuid4

from typing import TypedDict

import json, datetime

# Class for a test answer, includes the question, its response, and the prompt used by the LLM.
class Answer(TypedDict):
    question: str
    response: str
    prompt: str

# Class for a test run file, includes a list of responses and a test ID
class TestRun(TypedDict):
    responses: list[Answer]
    run_id: str

class Question(TypedDict):
    input: WebElement
    options: list[str]

def run_political_compass(model: LLMClient, lang: Literal['en'] | Literal['es']):
    test_result: TestRun = {
        'responses': [],
        'run_id': uuid4()
    }

    driver = webdriver.Edge()
    driver.get(f'https://www.politicalcompass.org/test/{lang}?page=1')
    print(f'On page: {driver.title}')

    # We start on the first page
    response_index = 0
    current_page = 1

    # Test only has 6 pages with 7 questions each
    while current_page < 7:
        # Get all question groups in the page
        page_questions = driver.find_elements(By.CSS_SELECTOR, 'fieldset')

        # Wait for the ads to be visible before dismissing it
        wait = WebDriverWait(driver, 5)
        page_ad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.closeButton')))
        page_ad.click()

        print(f"📄\tPage {current_page} / 6\n")

        # Answer each question
        for question in page_questions:
            # Extract question info, text, options, and the corresponding answer
            question_text = question.find_element(By.CSS_SELECTOR, 'legend').text
            question_inputs = question.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            question_options = [ label.text for label in question.find_elements(By.CSS_SELECTOR, 'label span') ]

            question_prompt = build_prompt(question=question_text, options=question_options, lang=lang)
            question_answer = model.send_request(question_prompt)

            print("Question: " + question_text + "\n")

            # Iterate question options until it matches the answer, then click it
            for answer_el, option in zip(question_inputs, question_options):
                print(f'✖️ \t {option}')
                if option == question_answer:
                    print(f'✔️ \t {option}')

                    answer: Answer = {
                        'prompt': question_prompt,
                        'question': question_text,
                        'response': question_answer
                    }

                    test_result['responses'].append(answer)

                    # Move to the correct checkbox and click it
                    ActionChains(driver).move_to_element(answer_el).perform()
                    answer_el.click()
                    break
            
            # Move to the next response
            response_index += 1
            print()

        # Once all questions on the page are done move to the next page 
        next_page_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        next_page_btn.click()
        current_page += 1

    # Wait for the ads to be visible before dismissing them
    wait = WebDriverWait(driver, 5)
    page_ad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.closeButton')))
    page_ad.click()

    # Get the result container and save the result as a png screenshot
    result_container = driver.find_elements(By.CSS_SELECTOR, 'article.measure-wide')[1]
    ActionChains(driver).move_to_element(result_container).perform()
    test_result = result_container.screenshot_as_png
    today = datetime.datetime.now()

    result_path = f'./results/{lang}/political_compass_{today.date()}_{test_result['run_id']}'

    # Write the screenshot with its corresponding timestamp
    with open(f'{result_path}.png', 'wb') as img_file:
        img_file.write(test_result)

    # Write test result to JSON file
    with open(f'{result_path}.json', 'wt', encoding='utf-8') as result_file:
        result_file.write(json.dumps(test_result))

    # Close the browser
    driver.quit()

run_political_compass(chatgpt_client, 'en')