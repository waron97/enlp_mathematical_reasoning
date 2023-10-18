from arithmetic.dataset import get_multi_arith
from arithmetic.util.openai import get_openai_completion


def run_experiment():
    train, test = get_multi_arith()
    sample = train[0]
    prompt = sample["template_python"]
    for var in sample["original_values"]:
        prompt = prompt.replace(f":{var}:", str(
            sample["original_values"][var]))
    answer = get_openai_completion(prompt)
    print(answer)
