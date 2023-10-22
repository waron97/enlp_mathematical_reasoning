from typing import Dict, List, TypedDict


class MappedItem(TypedDict):
    question: str
    template_expression: str
    template_python: str
    vars: List[str]
    original_values: Dict[str, int]


class PromptMeta(TypedDict):
    n_calls: int
    duration: float
    answers: List[float]
    formulas: List[str]
    templates: List[str]
