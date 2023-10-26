import json
import os
from typing import List, TypedDict

from arithmetic.MathPrompter.types import PromptMeta
from arithmetic.dataset.types import SourceDatasetRow


class ProgressItem (TypedDict):
    result: float
    meta: PromptMeta
    source: SourceDatasetRow


Progress = List[ProgressItem]

p = os.path.join("out", "progress.json")


def read_progress() -> Progress:
    """
    Load experiment progress from disk.
    """
    if not os.path.exists(p):
        return []
    with open(p, "r") as f:
        return json.load(f)


def write_progress(progress: Progress):
    """
    Write experiment progress to disk.
    """
    with open(p, "w") as f:
        json.dump(progress, f, indent=2)
