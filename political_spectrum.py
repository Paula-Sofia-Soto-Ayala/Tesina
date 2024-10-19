# from time import sleep
import datetime, time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from typing import Literal, TypedDict

def setRadioChecked(el: WebElement, val: Literal['true'] | Literal['false']):
    driver.execute_script("arguments[0].checked = arguments[1]", el, val)

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

test: TestRun = {"run_id": "testing_1234" }
language = 'en'

edge_options = webdriver.EdgeOptions()
edge_options.add_extension("./ublock.crx")
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
        labels = question.find_elements(By.CSS_SELECTOR, "label")

        print(f"\n{i + 1} - {question_text}")
        rnd_choice = random.randint(0, len(labels) - 1)

        for index, label in enumerate(labels):
            input = label.find_element(By.CSS_SELECTOR, "input")

            # 0 - Disagree Strongly
            # 1 - Disagree
            # 2 - Neutral
            # 3 - Agree
            # 4 - Agree Strongly
            if index == rnd_choice:
                setRadioChecked(input, "true")
                print(f'✔️ \t {label.text}')
            else:
                print(f'✖️ \t {label.text}')

        # How much do you care
        importance = question.find_element(By.CSS_SELECTOR, "ul li:last-child")
        importance_text = importance.find_element(By.CSS_SELECTOR, "b").text
        importance_opts = importance.find_elements(By.CSS_SELECTOR, "input")

        # Importance is set from 0 to 4, low to high
        opt_index = random.randint(0, len(importance_opts) - 1)
        print(f"⚖️ \t Importance {opt_index + 1}/5")
        setRadioChecked(importance_opts[opt_index], "true")
        time.sleep(0.25)


    submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_btn.click()
    page_num += 1

test_results = driver.find_element(By.CSS_SELECTOR, "section")
screenshot = test_results.screenshot_as_png
today = datetime.datetime.now()

# If there is a result take a screenshot and save it
# Write the screenshot with its corresponding timestamp
with open(f'./results/{language}/political_spectrum_{today.date()}_{test["run_id"]}.png', 'wb') as img_file:
    img_file.write(screenshot)

# Close the browser
driver.quit()
