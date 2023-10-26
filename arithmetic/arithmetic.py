import os
from arithmetic.dataset.types import RawDataset
from arithmetic.revisit_null_responses import revisit_null_responses
from arithmetic.dataset import get_multi_arith
from arithmetic.MathPrompter import MathPrompter
from arithmetic.util.progress import Progress, read_progress, write_progress
from tqdm import tqdm


def get_meta(predicted: Progress):
    n_calls = []
    exec_time = 0
    for item in predicted:
        n_calls.append(item["meta"]["n_calls"])
        exec_time += item["meta"]["duration"]
    n_calls_avg = sum(n_calls) / len(n_calls)
    exec_time_avg = exec_time / len(n_calls)
    return n_calls_avg, exec_time_avg


def compute_results(predicted: Progress, gold: RawDataset):
    total = len(gold)
    correct = 0
    for item in predicted:
        if item["result"] is None:
            is_correct = False
        else:
            predicted = item["result"]
            answer = item["source"]["final_answer"]
            is_correct = int(predicted) == int(answer)
        if is_correct:
            correct += 1

    return correct, total


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

    n_calls, exec_time = get_meta(progress)

    progress_revisited = revisit_null_responses(individual_check=False)
    progress_re_revisited = revisit_null_responses(individual_check=True)

    correct_original, total_original = compute_results(progress, data)
    correct_revisited, total_revisited = compute_results(
        progress_revisited, data)
    correct_re_revisited, total_re_revisited = compute_results(
        progress_re_revisited, data)

    print("--------------------")
    print(
        f"Metadata on experiment:")
    print(f"\taverage calls per question {n_calls:.2f}")
    print(f"\taverage execution time per question {exec_time:.2f} seconds")
    print("--------------------")
    print("Accuracy over MultiArith:")
    print(
        f"\tOriginal experiment: {correct_original}/{total_original} ({correct_original/total_original:.2f})")
    print(
        f"\tIgnoring integer division: {correct_revisited}/{total_revisited} ({correct_revisited/total_revisited:.2f})"
    )
    print(
        f"\tWithout prompt convergence: {correct_re_revisited}/{total_re_revisited} ({correct_re_revisited/total_re_revisited:.2f})"
    )
