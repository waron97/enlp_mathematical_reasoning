from arithmetic.MathPrompter import MathPrompter
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, template_folder="templates", static_folder="static")
mp = MathPrompter(model="text-davinci-003", max_tries_validation=5, repeat=1)


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
            result, meta = mp.prompt(prompt)
            if result is None:
                return render_template("index.html", result="MathPrompter failed to process your prompt, or language model was unable to provide a parse-able solution.", error=True)
            return render_template("index.html", result=result, meta=meta)
        except Exception as e:
            return render_template("index.html", result=str(e), error=True)

    return render_template("index.html")
