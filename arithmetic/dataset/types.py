from typing import Dict, List, TypedDict


class SourceDatasetRow(TypedDict):
    question: str
    final_answer: str


RawDataset = List[SourceDatasetRow]


class MappedItem(TypedDict):
    question: str
    final_answer: int
    template_expression: str
    template_python: str
    vars: List[str]
    original_values: Dict[str, int]


MultiArithMapped = List[MappedItem]
