from typing import List, TypedDict


class SourceDatasetRow(TypedDict):
    question: str
    final_answer: str


RawDataset = List[SourceDatasetRow]
