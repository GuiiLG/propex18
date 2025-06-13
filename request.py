import openai
from dotenv import load_dotenv
import os

load_dotenv("/home/luigi/VSCODE/PROPEX/key.env")

openai.api_key = os.getenv("OPENAI_API_KEY")

answer = str(input("Pergunte algo:"))

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content" : "Seu nome é constructionBOT"},
        {"role": "user", "content": f"{answer} "}
    ]
)

print(response.choices[0].message.content)