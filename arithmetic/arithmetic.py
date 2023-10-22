import json
from arithmetic.dataset import get_multi_arith
from arithmetic.MathPrompter import MathPrompter


def run_experiment():
    data = get_multi_arith()
    mp = MathPrompter(model="text-davinci-003",
                      max_tries_validation=5, repeat=5)

    sample = data[0]
    result = mp.prompt(sample["question"])
