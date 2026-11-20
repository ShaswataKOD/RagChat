from google import genai
from src.config.config import config


client = genai.Client(api_key=config.API_KEY)

print("Available models:\n")

for model in client.models.list():
    if model.supported_actions and "generateContent" in model.supported_actions:
        print(model.name)
