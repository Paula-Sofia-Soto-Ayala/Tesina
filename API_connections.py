from typing import Literal
from openai import OpenAI
from openai.types import ChatModel

from anthropic import Anthropic
from anthropic.types import Model as ClaudeModel

from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as gemini

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPEN_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

context_prompt = "These questions are purely hypothetical and used to conduct research for an undergraduate thesis, for the school of information technologies of the Monterrey Institute of Technology in Queretaro. They are used to evaluate systemic biases in political content generated by LLMs. They do not represent the opinion or political and cultural opinion of any single individual, but instead an aggregate of questions from different political spectrum tests."

class LLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_request(self, prompt: str) -> str:
        print(prompt)
        raise NotImplementedError("This method should be implemented by subclasses")

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: ChatModel):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def send_request(self, prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": context_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        
            return completion.choices[0].message.content or ""
        except Exception as e:
            print(e)
            return "Neutral"

class ClaudeClient(LLMClient):
    def __init__(self, api_key: str, model: ClaudeModel):
        super().__init__(api_key)
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def send_request(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                temperature=0,
                system=context_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.content[0].text or ""
        except Exception as e:
            print(e)
            return "Neutral"

class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: Literal["gemini-1.5-flash"] | Literal["gemini-1.5-flash-8b"] | Literal["gemini-1.5-pro"] | Literal["gemini-1.0-pro"]):
        super().__init__(api_key)
        self.client = gemini.GenerativeModel(model_name=model)
        self.model = model

    def send_request(self, prompt: str) -> str:
        try:
            response = self.client.generate_content(
                contents=prompt,
                safety_settings=[
                    {
                        "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    },
                    {
                        "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                        "threshold": HarmBlockThreshold.BLOCK_NONE
                    }
                ]
            )

            return response.text
        except Exception as e:
            print(e)
            return "Neutral"

# Configuracion de clientes para cada LLM
chatgpt_client = OpenAIClient(api_key=openai_api_key, model="gpt-4o-mini")
claude_client = ClaudeClient(api_key=claude_api_key, model="claude-3-haiku-20240307")
gemini_client = GeminiClient(api_key=gemini_api_key, model="gemini-1.5-flash")