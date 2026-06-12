from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bp(text):

    prompt = f"""
Maak een begeleidingsplan met:
- sectie1
- sectie2
- sectie3

Geef output als JSON:
{{
  "sectie1": "...",
  "sectie2": "...",
  "sectie3": "..."
}}

INPUT:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.choices[0].message.content

    try:
