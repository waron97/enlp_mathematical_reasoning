from ast import List
from typing import Dict


def fill_template(template: str, vars: Dict[str, int]):
    for var, value in vars.items():
        template = template.replace(f":{var}:", str(value))
    return template


def get_most_frequent_item(list: List):
    counts = {}
    for item in list:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1
    return max(counts, key=counts.get)
