from .base import Prompter


class GPT3 (Prompter):
    def prompt(self, p: str) -> str:
        return super().prompt(p)
