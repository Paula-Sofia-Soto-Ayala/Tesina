from API_connections import chatgpt_client, claude_client, gemini_client, LLMClient
from questions import ModelOptions, TestOptions, LangOptions
from political_coordinates import run_political_coords
from political_spectrum import run_political_spectrum
from political_compass import run_political_compass

def select_llm() -> tuple[str, ModelOptions]:
    models = {
        "1": "ChatGPT",
        "2": "Claude",
        "3": "Gemini"
    }

    print("1. ChatGPT")
    print("2. Claude")
    print("3. Gemini")
    choice = "0"

    while choice not in models.keys():
        choice = input("Input a number from 1 to 3: ")

    return [choice, models[choice]]

def select_test() -> TestOptions:
    test_options = {
        "1": "Political Compass",
        "2": "Political Coordinates",
        "3": "Political Spectrum"
    }
    for test in test_options:
        print(f"{test}. {test_options[test]}")

    choice = "0"
    while choice not in test_options.keys():
        choice = input("Select one of the shown tests: ")

    return test_options[choice]

def select_language() -> LangOptions:
    lang = "NA"

    while lang not in ["es", "en"]:
        lang = input("Select either 'en' or 'es': ")

    return lang

def run_test(model_name: str, model: LLMClient, test: TestOptions, lang: LangOptions):
    print(f"You have selected the test: {test} in {lang.upper()}")
    print(f"Using model: {model_name}")

    try:
        # Ejecucion del test segun su nombre
        if test == 'Political Compass':
            run_political_compass(model, lang, model_name)
        if test == 'Political Coordinates':
            run_political_coords(model, lang, model_name)
        if test == 'Political Spectrum':
            run_political_spectrum(model, lang, model_name)
    except Exception as e:
        print(f"An error happened while running the {test} test")
        print(str(e))
        exit(1)

    print("All questions have been sent and answers have been recorded.")

def main():
    print("Select an LLM to test")
    [model_choice, model_name] = select_llm()

    print(f"You selected model: {model_name}\n")
    
    print("Select a test to run")
    selected_test = select_test()

    print(f"Yout selected test: {selected_test}\n")
    
    print("Showing language menu...")
    test_lang = select_language()

    print(f"You selected: {test_lang}\n")

    llm_clients: dict[str, LLMClient] = {
        "1": chatgpt_client,
        "2": claude_client,
        "3": gemini_client
    }
 
    run_test(
        model=llm_clients[model_choice],
        test=selected_test,
        model_name=model_name,
        lang=test_lang
    )

if __name__ == "__main__":
    main()
