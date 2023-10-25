import os
from arithmetic.revisit_null_responses import revisit_null_responses
from arithmetic.dataset import get_multi_arith
from arithmetic.MathPrompter import MathPrompter
from arithmetic.util.progress import read_progress, write_progress
from tqdm import tqdm


def run_experiment():
    data = get_multi_arith()
    mp = MathPrompter(
        max_tries_validation=5, repeat=5)

    progress = read_progress()
    index = len(progress)

    if (index == 0):
        print("No previous progress recorded - booting experiment")
    elif (len(progress) == len(data)):
        print("Experiment already completed, loading from previous data")
    else:
        print("Resuming experiment from previous progress at index", index)

    with tqdm(total=len(data)) as pbar:
        pbar.update(index)
        for i in range(index, len(data)):
            sample = data[i]
            try:
                result, meta = mp.prompt(sample["question"])
                progress.append(
                    {"result": result, "meta": meta, "source": sample})
                write_progress(progress)
            except:
                progress.append({
                    "result": None,
                    "meta": None,
                    "source": sample
                })
            pbar.update(1)

    total = len(data)
    correct = 0

    for item in progress:
        if item["result"] is None:
            is_correct = False
        else:
            predicted = item["result"]
            answer = item["source"]["final_answer"]
            is_correct = int(predicted) == int(answer)
        if is_correct:
            correct += 1

    print((correct / total) * 100)
    progress_revisited = revisit_null_responses()

    correct = 0
    for item in progress_revisited:
        if item["result"] is None:
            is_correct = False
        else:
            predicted = item["result"]
            answer = item["source"]["final_answer"]
            is_correct = int(predicted) == int(answer)
        if is_correct:
            correct += 1

    print((correct / total) * 100)
