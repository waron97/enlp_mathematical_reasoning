import json
from arithmetic.MathPrompter.util import check_completion_convergence, eval_formula, extract_eval, extract_prompt_info
from arithmetic.util.progress import read_progress


def revisit_null_responses():
    progress = read_progress()

    revisited = []

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
            updated_results.sort(key=lambda x: updated_results.count(x))
            updated_results.reverse()
            record["result"] = updated_results[0]
            record["revisited"] = True
            revisited.append(record)

        else:
            revisited.append(record)

    with open("out/revisited.json", "w") as f:
        json.dump(revisited, f, indent=4)

    return revisited
