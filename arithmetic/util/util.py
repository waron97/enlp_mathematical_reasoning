from ast import List
from typing import Dict


def get_most_frequent_item(list: List):
    """
    Returns the most frequent item in a list
    """
    counts = {}
    for item in list:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1
    return max(counts, key=counts.get)
