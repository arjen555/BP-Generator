from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# API key uit Render environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bp(text):

    prompt = f"""
Je bent een expert in cluster 1 onderwijs (visuele beperking).

Verwerk onderstaande informatie tot een begeleidingsplan met:

- Sectie 1 (analyse + situatie)
