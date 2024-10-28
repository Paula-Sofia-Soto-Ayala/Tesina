# from time import sleep
import datetime, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.webdriver import WebDriver

from questions import build_prompt, get_consensus, Answer, TestRun
from questions import ModelOptions, LangOptions
from API_connections import LLMClient
from typing import Literal
from uuid import uuid4

def setRadioChecked(driver: WebDriver, el: WebElement, val: Literal['true'] | Literal['false']):
    driver.execute_script("arguments[0].checked = arguments[1]", el, val)

def setInputValue(driver: WebDriver, el: WebElement, val: str):
    driver.execute_script("arguments[0].value = arguments[1]", el, val)

def remove_page_ads(driver: WebDriver):
    time.sleep(1)
    ad_btns = driver.find_elements(By.CSS_SELECTOR, 'div.grippy-host')
    for ad in ad_btns:
        ad.click()

    time.sleep(1)

options_en = {
    "Disagree strongly": "0",
    "Disagree": "1",
    "Neutral": "2",
    "Agree": "3",
    "Agree strongly": "4"
}

options_es = {
    "Totalmente en desacuerdo": "0",
    "En desacuerdo": "1",
    "Neutral": "2",
    "De acuerdo": "3",
    "Totalmente de acuerdo": "4"
}

translate = {
    "Totalmente en desacuerdo": "Disagree strongly",
    "En desacuerdo": "Disagree",
    "Neutral": "Neutral",
    "De acuerdo": "Agree",
    "Totalmente de acuerdo": "Agree strongly"
}

importance_values = ["0", "1", "2", "3", "4"]

def run_political_spectrum(model: LLMClient, lang: LangOptions, model_name: ModelOptions):
    test: TestRun = {
        "run_id": str(uuid4()),
        "model": model_name,
        "test": "Political Spectrum Quiz",
        "lang": lang,
        "responses": [],
    }

    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://www.gotoquiz.com/politics/political-spectrum-quiz.html")

    print(f'On page: {driver.title}')
    page_num = 1

    while page_num < 3:
        print(f"\n📄 \t Completing page {page_num} / 2")
        question_list = driver.find_elements(By.CSS_SELECTOR, "ol.questions > li")

        for i, question in enumerate(question_list):
            # Move to the correct checkbox and click it
            ActionChains(driver).move_to_element(question).perform()

            # Skip the last question, it's optional
            if question.get_attribute("class") == "opt":
                continue

            question_text = question.find_element(By.CSS_SELECTOR, "strong").text
            spanish_prompt = "Please translate the following question to spanish, try to keep it as accurate as possible and avoid changing the meaning"
            question_text = question_text if lang == "en" else model.send_request(
                prompt=spanish_prompt + "\n" + question_text
            )

            question_opts = options_es if lang == 'es' else options_en
            labels = question.find_elements(By.CSS_SELECTOR, "label")

            print(f"\n{i + 1} - {question_text}")

            question_prompt = build_prompt(
                options=list(question_opts.keys()),
                question=question_text,
                lang=lang
            )

            question_answer, question_attempts = get_consensus(model, question_prompt)
            question_answer = question_answer.rstrip().removesuffix('.')
            final_answer = question_answer if lang == "en" else translate[question_answer]
            print(f"Answer: {question_answer}")

            for label in labels:
                input = label.find_element(By.CSS_SELECTOR, "input")

                # 0 - Disagree Strongly
                # 1 - Disagree
                # 2 - Neutral
                # 3 - Agree
                # 4 - Agree Strongly
                if label.text == final_answer:
                    setRadioChecked(driver, el=input, val="true")
                    print(f'✔️ \t {label.text}')
                else:
                    print(f'✖️ \t {label.text}')

            # How much do you care
            importance = question.find_element(By.CSS_SELECTOR, "ul li:last-child")
            importance_text = importance.find_element(By.CSS_SELECTOR, "b").text
            importance_opts = importance.find_elements(By.CSS_SELECTOR, "input")

            # Importance is set from 0 to 4, low to high
            importance_prompt = build_prompt(
                options=importance_values,
                question=importance_text,
                lang=lang
            )

            importance_answer, importance_attempts = get_consensus(model, importance_prompt)
            importance_index = int(importance_answer)

            answer: Answer = {
                "importance_attempts": importance_attempts,
                "importance": importance_answer,
                "attemps": question_attempts,
                "response": question_answer,
                "question": question_text,
                "prompt": question_prompt
            }

            test['responses'].append(answer)

            print(f"⚖️ \t Importance {importance_answer}/4")
            setRadioChecked(driver, el=importance_opts[importance_index], val="true")
            time.sleep(0.25)


        submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        remove_page_ads(driver)
        submit_btn.click()
        page_num += 1

    remove_page_ads(driver)
    test_results = driver.find_element(By.CSS_SELECTOR, "section")
    today = datetime.datetime.now()

    # If there is a result take a screenshot and save it
    result_path = f'./results/{lang}/political_spectrum_{today.date()}_{test["run_id"]}'

    # Write the screenshot with its corresponding timestamp
    with open(f'{result_path}.png', 'wb') as img_file:
        img_file.write(test_results.screenshot_as_png)

    with open(f'{result_path}.json', 'wt') as result_file:
        result_file.write(json.dumps(test, indent=4))

    # Close the browser
    driver.quit()