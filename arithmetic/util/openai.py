import os
import requests


def make_openai_request(url, data):
    """
    Utility function to make a request to the OpenAI API.
    """
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


def get_openai_completion(prompt, model):
    """
    Utility function to get a completion from the OpenAI API.
    """
    response = make_openai_request(
        "/completions",
        {
            "prompt": prompt,
            "model": model,
            "max_tokens": 100,
            "n": 1
        }
    )

    return response["choices"][0]["text"]
