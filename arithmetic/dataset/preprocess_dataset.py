import json
from pprint import pprint
import random
from typing import Dict, List
from .var_sequence import var_sequence
from arithmetic.dataset.types import MultiArithMapped, RawDataset
import re


def get_template_from_question(question: str) -> (str, List[str], Dict[str, int]):
    pat = re.compile(" \d+ ", re.MULTILINE)
    matches = []

    for m in pat.finditer(question):
        start = m.start()
        end = m.end()
        string = question[start:end]
        matches.append((start, end, string))

    template = question
    vars = []
    original_values = {}
    reduced_space = 0

    for i in range(len(matches)):
        start, end, string = matches[i]
        start = start - reduced_space
        end = end - reduced_space
        var = var_sequence[i]

        vars.append(var)
        template = template[:start] + f" {var} " + template[end:]
        reduced_space += len(string.strip()) - len(var)
        original_values[var] = int(string.strip())

    vars_str = ", ".join([f"{var}: :{var}:" for var in vars])
    template += f"\n\nMapping: {{{vars_str}}}"

    return template, vars, original_values


def get_template_expression(template: str) -> str:
    return template + "\nWrite a mathematical equation and generate the answer format starting with'Answer ='"


def get_template_python(template: str) -> str:
    return template + "\nWrite a Python function that returns the answer."


def preprocess_dataset(ds: RawDataset) -> MultiArithMapped:
    mapped: MultiArithMapped = []
    for item in ds:
        template, vars, original_values = get_template_from_question(
            item["question"].strip())
        mapped.append(
            {
                "final_answer": int(item["final_answer"]),
                "question": item["question"].strip(),
                "template_expression": get_template_expression(template),
                "template_python": get_template_python(template),
                "vars": vars,
                "original_values": original_values,
            }
        )
    return mapped
