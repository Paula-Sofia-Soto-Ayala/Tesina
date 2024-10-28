from typing import Literal
from openai import OpenAI
from openai.types import ChatModel

from anthropic import Anthropic
from anthropic.types import Model as ClaudeModel

import google.generativeai as gemini

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPEN_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

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
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        try:
            return completion.choices[0].message.content or ""
        except Exception as err:
            return "No se pudo obtener una respuesta" + " " + str(err)

class ClaudeClient(LLMClient):
    def __init__(self, api_key: str, model: ClaudeModel):
        super().__init__(api_key)
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def send_request(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=150,
            temperature=0,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return response.content[0].text or ""

class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: Literal["gemini-1.5-flash"] | Literal["gemini-1.5-flash-8b"] | Literal["gemini-1.5-pro"] | Literal["gemini-1.0-pro"]):
        super().__init__(api_key)
        self.client = gemini.GenerativeModel(model_name=model)
        self.model = model

    def send_request(self, prompt: str) -> str:
        response = self.client.generate_content(contents=prompt)
        return response.text

# Configuracion de clientes para cada LLM
chatgpt_client = OpenAIClient(api_key=openai_api_key, model="chatgpt-4o-latest")
claude_client = ClaudeClient(api_key=claude_api_key, model="claude-3-5-sonnet-20240620")
gemini_client = GeminiClient(api_key=gemini_api_key, model="gemini-1.5-pro")