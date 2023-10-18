import datasets
from datasets import Dataset

from .preprocess_dataset import preprocess_dataset
from .types import RawDataset


def map_dataset(split: Dataset) -> RawDataset:
    return [{"question": item["question"], "final_answer": item["final_ans"]} for item in split]


def get_multi_arith():
    ds = datasets.load_dataset("ChilleD/MultiArith")
    train, test = ds["train"], ds["test"]
    train, test = map_dataset(train), map_dataset(test)
    return preprocess_dataset(train), preprocess_dataset(test)
