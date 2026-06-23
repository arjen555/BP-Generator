from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# API key uit Render
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        text = data.get("text", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Je bent een zeer ervaren ambulant onderwijskundig begeleider in cluster 1 (visuele beperking).

Je taak is om informatie uit onderzoeken (zoals VFO, psychologisch onderzoek en maatschappelijk werk) te vertalen naar een professioneel en direct bruikbaar begeleidingsplan.

------------------------------
ALGEMENE RICHTLIJNEN
------------------------------
- Schrijf vloeiend en professioneel
- Formuleer praktisch en direct toepasbaar
- Vermijd vage of algemene taal
- Gebruik geen namen (anoniem blijven)
- Schrijf iets uitgebreider zodat copy-paste direct mogelijk is

------------------------------
INHOUD
------------------------------

1. Vertaal visuele functies naar onderwijsimpact  
(bijv. visus → overzicht, digibordgebruik, lezen)

2. Benoem:
- wat goed gaat (bevorderende factoren)
- wat aandacht nodig heeft (belemmerende factoren)

3. Verwerk impliciet kritische succesfactoren:
- zelfstandigheid
- zelfinzicht
- participatie
- sociale interactie
- toekomstgericht functioneren

4. Maak altijd de vertaalslag:
onderzoek → gedrag → klas → ondersteuning

------------------------------
SECTIE 1 — Huidige situatie
------------------------------
- Beschrijf visuele functies begrijpelijk
- Leg uit wat dit betekent op school
- Benoem sterke kanten
- Benoem aandachtspunten
- Neem sociaal en praktisch functioneren mee

------------------------------
SECTIE 2 — Doelen en acties
------------------------------
- Genereer meerdere doelen (automatisch aantal)
- SMART niveau 2 formuleren
- Concreet gedrag beschrijven
- Koppelen aan situaties

Per doel:

Doel:
...

Acties:
- ...
- ...

------------------------------
SECTIE 3 — Hulpmiddelen en adviezen
------------------------------
- Benoem hulpmiddelen concreet
- Koppel aan situaties (klas, gym, sociaal)
- Maak adviezen direct uitvoerbaar
- Gebruik formuleringen zoals:
  "heeft baat bij..."
  "gebruik..."
  "bij voorkeur..."

------------------------------
OUTPUT
------------------------------

Geef ALLEEN JSON terug:

{{
  "sectie1": "...",
  "sectie2": "...",
  "sectie3": "..."
}}

------------------------------
INPUT
------------------------------
{text}
"""
                }
            ]
        )

        result_text = response.choices[0].message.content

        try:
            parsed = json.loads(result_text)
        except:
            parsed = {
                "sectie1": result_text,
                "sectie2": "",
                "sectie3": ""
            }

        return jsonify(parsed)

    except Exception as e:
        # Fouten zichtbaar maken in je tool
        return jsonify({
            "sectie1": "❌ Fout in backend",
            "sectie2": str(e),
            "sectie3": ""
        }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
