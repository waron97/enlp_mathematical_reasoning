import os
import requests


def make_openai_request(url, data):
    final_url = "https://api.openai.com/v1" + url
    token = os.environ.get("OPENAI_API_KEY")
    response = requests.post(
        final_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=data
    )
    return response.json()


def get_openai_completion(prompt, model="text-davinci-003", n_completions=1):
    return make_openai_request(
        "/completions",
        {
            "prompt": prompt,
            "model": model,
            "max_tokens": 100,
            "n": n_completions
        }
    )
