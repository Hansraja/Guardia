import os
import datetime
import random
from openai import OpenAI
from config import API_KEY

class GuardiaAssistant:
    def __init__(self):
        self.system = []
        self.user = []
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )

    def chat(self, query):
        self.user.append(query)
        try:
            completion = self.client.chat.completions.create(
                model="liquid/lfm-40b:free",
                messages=[
                    {"role": "system", "content": msg} for msg in self.system
                ] + [
                    {"role": "user", "content": msg} for msg in self.user
                ]
            )
            response = completion.choices[0].message.content
            self.system.append(response)
            return response
        except Exception as e:
            return str('An error occurred: ')