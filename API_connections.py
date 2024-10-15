from typing import Literal
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPEN_API_KEY')

type OpenAIModel = Literal["gpt-4o-mini"] | Literal["gpt-3.5-turbo"]

class LLMClient:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url

    def send_request(self, prompt: str):
        raise NotImplementedError("This method should be implemented by subclasses")

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: OpenAIModel ):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def send_request(self, prompt: str):
        result = self.client.chat
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            return completion.choices[0].message
        except Exception as err:
            return "No se pudo obtener una respuesta" + " " + str(err)

class ClaudeClient(LLMClient):
    def send_request(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 150
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        return response.json()

class LlamaClient(LLMClient):
    def send_request(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 150
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        return response.json()

# Configuración de clientes para cada LLM
chatgpt_client = OpenAIClient(api_key=openai_api_key, model="gpt-3.5-turbo")
claude_client = ClaudeClient(api_key='YOUR_CLAUDE_API_KEY', base_url='https://api.anthropic.com/v1/complete')
llama_client = LlamaClient(api_key='YOUR_LLAMA_API_KEY', base_url='https://api.llama.ai/v1/complete')

