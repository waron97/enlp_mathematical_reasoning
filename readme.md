# Reproducing MathPrompter: Mathematical Reasoning using Large Language Models

This repository contains reproducing code for the following paper:

```
Shima Imani, Liang Du, Harsh Shrivastava.
MathPrompter: Mathematical Reasoning using Large Language Models.
2023.
```

The codebase uses the MultiArith dataset, a copy of which is provided in the `data` folder.

All of the raw results of the reproduction attempt can be found in the `output.json` file.

## Requirements

To install the Python dependencies, run:

```bash
pip install -r requirements.txt
```

For any code to work, it is also necessary to set the correct environment variables.
To achieve this, create a `.env` file in the root directory and copy the contents of `.env.example` into it. Please make sure to add your own OpenAI API key to the `.env` file. In all, all the following environment variables must be set:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` the model wich will be used for the experiments. For an exact reproduction, leave it as "text-davinci-003"
- `WEBAPP_MODE` (`DEV` or `PROD`) determines whether the web application will require a password for prompting. The password is only required in `PROD`. This is to prevent abuse of the OpenAI API key in case the app is deployed to a public server.
- `WEBAPP_PASSWORD`, the password for the web application. Only required in `PROD` mode. If used, make sure to change it to a different value than in the example.

## Setup (experiment)

The experiment will be run automatically when the `main.py` script is executed. The results will be saved in the `out/progress.json` file. The experiment can be interrupted at any point, and will be automatically resumed from the last entry in the progress file when the script is run again.

It is also possible to paste the contents of the `output.json` file into the `out/progress.json` file to resume the experiment from a specific point, or to start processing from a point when all data has passed through MathPrompter. This can be useful if one wants to only examine after-the-fact tweaks to the outputs to gauge their effect on the results.

The resumability logic uses naive sequence length to track progress, so removing an entry from the `progress.json` file will not cause it to be re-processed unless it is the last one.

## Setup (web application)

Provided that the environment variables are set correctly, the web application can be started by running:

```bash
python -m flask --app webapp.webapp:app run
```

After this, one should follow the instructions in the terminal to access the web application or for troubleshooting.
