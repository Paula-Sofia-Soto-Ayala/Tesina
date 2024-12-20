from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from questions import build_prompt, get_consensus, Answer, TestRun, save_clean_json
from questions import LangOptions, ModelOptions
from API_connections import LLMClient
from uuid import uuid4

import datetime, os

def click_element(driver: WebDriver, el: WebElement):
    driver.execute_script("arguments[0].click()", el)

def run_political_compass(model: LLMClient, lang: LangOptions, model_name: ModelOptions):
    test_result: TestRun = {
        'run_id': str(uuid4()),
        'test': "Political Compass Test",
        'model': model_name,
        'lang': lang,
        'responses': [],
    }

    driver = webdriver.Edge()
    driver.get(f'https://www.politicalcompass.org/test/{lang}?page=1')
    print(f'On page: {driver.title}')

    # We start on the first page
    question_index = 1
    current_page = 1

    # Test only has 6 pages with 7 questions each
    while current_page < 7:
        # Get all question groups in the page
        page_questions = driver.find_elements(By.CSS_SELECTOR, 'fieldset')

        # Wait for the ads to be visible before dismissing it
        try:
            wait = WebDriverWait(driver, 10)
            page_ad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.closeButton')))
            click_element(driver, page_ad)
            # page_ad.click()
        except:
            print("No ads were found")

        print(f"📄\tPage {current_page} / 6\n")

        # Answer each question
        for question in page_questions:
            # Extract question info, text, options, and the corresponding answer
            question_text = question.find_element(By.CSS_SELECTOR, 'legend').text
            question_inputs = question.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            question_options = [ label.text for label in question.find_elements(By.CSS_SELECTOR, 'label span') ]

            question_prompt = build_prompt(question=question_text, options=question_options, lang=lang)
            question_answer, question_attempts = get_consensus(model, question_prompt, question_options)
            question_answer = question_answer.strip().removesuffix('.')

            print(f"{question_index}. Question: " + question_text + "\n")
            print(f"Answer: {question_answer}")

            # Iterate question options until it matches the answer, then click it
            for answer_el, option in zip(question_inputs, question_options):
                if option == question_answer:
                    print(f'✔️ \t {option}')

                    answer: Answer = {
                        'attemps': question_attempts,
                        'response': question_answer,
                        'prompt': question_prompt,
                        'question': question_text,
                        'importance_attempts': None,
                        'importance': None,
                    }

                    test_result['responses'].append(answer)

                    # Move to the correct checkbox and click it
                    ActionChains(driver).move_to_element(answer_el).perform()
                    click_element(driver, answer_el)
                    # answer_el.click()
                else:
                    print(f'✖️ \t {option}')
            
            # Move to the next response
            question_index += 1
            print()

        # Once all questions on the page are done move to the next page 
        next_page_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        click_element(driver, next_page_btn)
        # next_page_btn.click()
        current_page += 1

    # Create the path to save the results, including model, test, and language
    today = datetime.datetime.now()
    result_path = f'./{model_name}/{test_result["test"]}/{lang}/results/political_compass_{today.date()}_{test_result["run_id"]}'
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    # Write test result to JSON file
    save_clean_json(test_result, f'{result_path}.json')

    # Wait for the ads to be visible before dismissing them
    wait = WebDriverWait(driver, 5)
    page_ad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.closeButton')))
    click_element(driver, page_ad)
    # page_ad.click()

    # Get the result container and save the result as a png screenshot
    result_container = driver.find_elements(By.CSS_SELECTOR, 'article.measure-wide')[1]

    if result_container is None:
        print("No test result found, check all answers were filled")
        exit(0)

    ActionChains(driver).move_to_element(result_container).perform()
    test_photo = result_container.screenshot_as_png
    
    # Write the screenshot with its corresponding timestamp
    with open(f'{result_path}.png', 'wb') as img_file:
        img_file.write(test_photo)

    # Close the browser
    driver.quit()
