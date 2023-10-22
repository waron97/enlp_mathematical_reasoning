import json
import os

from .types import RawDataset


def map_dataset(split) -> RawDataset:
    return [
        {
            "question": item["sQuestion"],
            "final_answer": item["lSolutions"][0],
            "index": int(item["iIndex"])
        } for item in split
    ]


def get_multi_arith():
    with open(os.path.join("data", "MultiArith.json"), "r") as f:
        ds = json.load(f)
        return map_dataset(ds)
