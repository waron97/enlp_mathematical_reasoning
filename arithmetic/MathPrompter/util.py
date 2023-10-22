
from typing import Dict, List
import re
from .types import MappedItem
import random


var_sequence = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H"
    "I",
    "J",
]


def get_template_expression(template: str) -> str:
    return template + "\nWrite a mathematical equation and generate the answer format starting with'Answer ='"


def get_template_python(template: str) -> str:
    return template + "\nWrite a Python function that returns the answer."


def get_template_from_question(question: str) -> (str, List[str], Dict[str, int]):
    pat = re.compile(" \d+ |^\d+ | \d+$| \d+\.", re.MULTILINE)
    matches = []

    for m in pat.finditer(question.strip()):
        start = m.start()
        end = m.end()
        string = question[start:end]
        matches.append((start, end, string))

    template = question
    vars = []
    original_values = {}
    reduced_space = 0

    for i in range((len(matches))):
        match = matches[i]
        start, end, string = match
        start = start - reduced_space
        end = end - reduced_space
        var = var_sequence[i]
        digits = re.compile("\d+").findall(match[2])[0]
        before, after = string.split(digits)

        vars.append(var)
        template = template[:start] + f"{before}{var}{after}" + template[end:]
        reduced_space += len(digits) - len(var)
        original_values[var] = int(digits)

    vars_str = ", ".join([f"{var}: :{var}:" for var in vars])
    template += f"\n\nMapping: {{{vars_str}}}"

    return template, vars, original_values


def extract_prompt_info(prompt: str) -> MappedItem:
    template, vars, original_values = get_template_from_question(
        prompt.strip())

    return {
        "question": prompt.strip(),
        "template_expression": get_template_expression(template),
        "template_python": get_template_python(template),
        "vars": vars,
        "original_values": original_values,
    }


def extract_eval(completion: str, completion_type="python"):
    if (completion_type == "python"):
        line = [line for line in completion.split(
            "\n") if "return " in line][0]
        return line.replace("return ", "").strip()

    elif (completion_type == "expression"):
        line = [line for line in completion.split(
            "\n") if "Answer =" in line][0]
        return line.replace("Answer =", "").strip()


def eval_formula(formula: str, vars: Dict[str, int]) -> float:
    for var in vars:
        formula = formula.replace(var, str(vars[var]))

    return round(float(eval(formula)), 2)


def check_completion_convergence(python: str, expression: str, vars: List[str]) -> bool:
    python_eval = extract_eval(python, "python")
    expression_eval = extract_eval(expression, "expression")
    random_values = {
        var: random.randint(1, 100) for var in vars
    }

    try:
        python_evalled = eval_formula(python_eval, random_values)
        expression_evalled = eval_formula(expression_eval, random_values)
        return python_evalled == expression_evalled
    except:
        return False
