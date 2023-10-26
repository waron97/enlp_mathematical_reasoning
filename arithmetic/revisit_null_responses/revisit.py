import json
from typing import List
from arithmetic.MathPrompter.util import check_completion_convergence, eval_formula, extract_eval, extract_prompt_info
from arithmetic.util.progress import Progress, ProgressItem, read_progress
from arithmetic.util.util import get_most_frequent_item


def revisit_null_responses(individual_check=False) -> Progress:
    """
        Revisit questions where MultiArith failed to provide a question. 
        If no configuration is specified, this only maps integer division to division.
        If individual_check is True, this will also check answers ignoring completion convergence.
    """
    progress = read_progress()

    revisited: List[ProgressItem] = []

    for record in progress:
        if record["result"] is not None:
            revisited.append(record)
            continue

        completions = record["meta"]["discarded_completions"]
        info = extract_prompt_info(record["source"]["question"])
        updated_results = []
        for python, expression in completions:
            try:
                converge = check_completion_convergence(
                    python, expression, info["vars"], purge_integer_division=True)
                if (converge):
                    formula = extract_eval(
                        python, completion_type="python", transform_integer_divison=True)
                    result = eval_formula(formula, info["original_values"])
                    updated_results.append(result)
            except:
                pass

        if len(updated_results) > 0:
            record["result"] = get_most_frequent_item(updated_results)
            record["revisited"] = True
            revisited.append(record)

        else:
            revisited.append(record)

    with open("out/revisited.json", "w") as f:
        json.dump(revisited, f, indent=4)

    if not individual_check:
        return revisited

    second_revisit: List[ProgressItem] = []

    for record in revisited:
        if record["result"] is not None:
            second_revisit.append(record)
            continue

        results = []

        for python, expression in record["meta"]["discarded_completions"]:
            r = None
            formula = extract_eval(
                python, completion_type="python", transform_integer_divison=True)
            r = eval_formula(formula, info["original_values"])

            if r is None:
                formula = extract_eval(
                    expression, completion_type="expression", transform_integer_divison=True)
                r = eval_formula(formula, info["original_values"])

            if r is not None:
                results.append(r)

        if len(results) > 0:
            maximum = get_most_frequent_item(results)
            record["result"] = maximum
            record["revisited"] = True
            second_revisit.append(record)
        else:
            second_revisit.append(record)

    with open("out/revisited2.json", "w") as f:
        json.dump(second_revisit, f, indent=4)

    return second_revisit
