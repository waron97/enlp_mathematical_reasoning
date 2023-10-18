from .base import Prompter


class GPT4(Prompter):
    def prompt(self, p: str) -> str:
        return super().prompt(p)
