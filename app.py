from flask import Flask, request
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bp(text):

    prompt = f"""
Je bent een expert in cluster 1 onderwijs (visuele beperking).

Verwerk onderstaande input tot een begeleidingsplan.

Geef output in JSON:
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
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    result = generate_bp(data["text"])
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
