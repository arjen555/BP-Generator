from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI 

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_bp(text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
Maak een begeleidingsplan met:

- sectie1
- sectie2
- sectie3

Geef ALLEEN JSON terug:

{{
  "sectie1": "...",
  "sectie2": "...",
  "sectie3": "..."
}}

INPUT:
{text}
"""
            }
        ]
    )

    result_text = response.choices[0].message.content

    try:
        parsed = json.loads(result_text)
    except Exception:
        parsed = {
            "sectie1": result_text,
            "sectie2": "",
            "sectie3": ""
        }

    return parsed


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    result = generate_bp(data.get("text", ""))
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
