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
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url

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
            messages=[
                {"role": "user", "content": prompt}
            ]
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
        message = self.client.completions.create(
            model="claude-3-haiku-20240307",
            max_tokens_to_sample=150,
            prompt=prompt
        )

        return message.completion

class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: Literal["gemini-1.5-flash"] | Literal["gemini-1.5-flash-8b"] | Literal["gemini-1.5-pro"] | Literal["gemini-1.0-pro"]):
        super().__init__(api_key)
        self.client = gemini.GenerativeModel(model_name=model)
        self.model = model

    def send_request(self, prompt: str) -> str:
        response = self.client.generate_content(contents=prompt)
        return response.text

# Configuración de clientes para cada LLM
chatgpt_client = OpenAIClient(api_key=openai_api_key, model="gpt-3.5-turbo")
claude_client = ClaudeClient(api_key=claude_api_key, model="claude-3-haiku-20240307")
gemini_client = GeminiClient(api_key=gemini_api_key, model="gemini-1.5-flash")