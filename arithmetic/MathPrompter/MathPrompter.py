import copy
import os
import time
from typing import Tuple

from arithmetic.util import get_openai_completion
from arithmetic.util.util import get_most_frequent_item

from .errors import NoResults, ValidationTriesExceeded
from .types import MappedItem, PromptMeta
from .util import (check_completion_convergence, eval_formula, extract_eval,
                   extract_prompt_info)


class MathPrompter:
    """
    Class that encapsulates the MathPrompter prompting process
    """

    def __init__(self, max_tries_validation=5, repeat=5):
        """
        :param max_tries_validation: The maximum number of tries to get a valid prompt
        :param repeat: The number of times to repeat the process (majority response is returned)
        """
        self.model = os.getenv("OPENAI_MODEL")
        self.max_tries_validation = max_tries_validation
        self.repeat = repeat

        self._initial_meta: PromptMeta = {
            "n_calls": 0,
            "duration": None,
            "templates": [],
            "answers": [],
            "completions": [],
            "discarded_completions": [],
        }

        # reset after every prompt
        self._reset_meta()

    def prompt(self, prompt: str) -> Tuple[float, PromptMeta]:
        """
        Use MathPrompter to get the solution to a math problem.
        :param prompt: The math problem to solve
        :return: The solution to the math problem and meta information about the process
        """
        self._reset_meta()
        prompt_info = extract_prompt_info(prompt)

        self.prompt_meta["templates"] = [
            prompt_info["template_python"], prompt_info["template_expression"]]

        results = []

        start = time.time()

        for _ in range(self.repeat):
            try:
                mapping_python, mapping_expression = self.get_valid_mappings(
                    prompt_info)

                formula = extract_eval(
                    mapping_python, completion_type="python")
                self.prompt_meta["completions"].append(
                    [mapping_python, mapping_expression])

                result = eval_formula(formula, prompt_info["original_values"])
                results.append(result)
            except:
                pass

        self.prompt_meta["duration"] = time.time() - start
        self.prompt_meta["answers"] = results

        if len(results) == 0:
            return None, self.prompt_meta

        return get_most_frequent_item(results), self.prompt_meta

    def get_valid_mappings(self, prompt: MappedItem) -> (str, str):
        """
        Derive the Python and expression prompts from the mathematical question
        """
        python = prompt["template_python"]
        expression = prompt["template_expression"]

        current_try = 0
        generated_python = None
        generated_expression = None

        while current_try < self.max_tries_validation:
            generated_python = self._call_openai(python)
            generated_expression = self._call_openai(expression)

            converge = check_completion_convergence(
                generated_python,
                generated_expression,
                prompt["vars"]
            )

            if converge:
                break

            self.prompt_meta["discarded_completions"].append(
                [generated_python, generated_expression])

            current_try += 1
            generated_expression = None
            generated_python = None

        if generated_expression is None or generated_python is None:
            raise ValidationTriesExceeded(
                f"Could not find a valid mapping for prompt: {prompt['question']}")

        return generated_python, generated_expression

    def _call_openai(self, prompt: str):
        """
        Call the OpenAI API to get a completion for a prompt.
        Record meta information about the call.
        """
        self.prompt_meta["n_calls"] += 1
        return get_openai_completion(prompt, self.model)

    def _reset_meta(self):
        """
        Reset the meta information to the initial state.
        """
        self.prompt_meta = copy.deepcopy(self._initial_meta)
