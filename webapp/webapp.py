from arithmetic.MathPrompter import MathPrompter
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

from arithmetic.MathPrompter.util import extract_prompt_info

load_dotenv()


app = Flask(__name__, template_folder="templates", static_folder="static")
mp = MathPrompter(
    max_tries_validation=5, repeat=1)


def is_sensible_prompt(p):
    info = extract_prompt_info(p)
    return len(info["vars"]) > 0


@app.route("/", methods=["GET", "POST"])
def webapp():
    if request.method == "POST":
        admin_pwd = os.getenv("WEBAPP_PASSWORD")
        mode = os.getenv("WEBAPP_MODE")
        prompt = request.form["prompt"]
        password = request.form["password"]

        if mode == "PROD" and password != admin_pwd:
            return render_template("index.html", result="Incorrect password", error=True)
        elif not prompt:
            return render_template("index.html", result="Please enter a prompt", error=True)
        try:
            if not is_sensible_prompt(prompt):
                return render_template("index.html", result="MathPrompter could not identify your prompt as a calculation question.", error=True)
            result, meta = mp.prompt(prompt)
            if result is None:
                return render_template("index.html", result="MathPrompter failed to process your prompt, or language model was unable to provide a parse-able solution.", error=True)
            return render_template("index.html", result=result, meta=meta)
        except Exception as e:
            return render_template("index.html", result=str(e), error=True)

    return render_template("index.html")
