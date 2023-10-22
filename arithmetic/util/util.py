from typing import Dict


def fill_template(template: str, vars: Dict[str, int]):
    for var, value in vars.items():
        template = template.replace(f":{var}:", str(value))
    return template
