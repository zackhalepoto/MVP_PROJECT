import os
import requests

def generate_text_from_synthflow(prompt):
    api_key = os.getenv("SYNTHFLOW_API_KEY")
    url = os.getenv("SYNTHFLOW_URL", "https://api.synthflow.ai/generate")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("text")
    else:
        raise Exception("Synthflow error: " + response.text)