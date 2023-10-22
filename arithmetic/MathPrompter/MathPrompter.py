from .types import MappedItem, PromptMeta
from .util import extract_eval, extract_prompt_info, check_completion_convergence, eval_formula
from .errors import NoResults, ValidationTriesExceeded
from arithmetic.util import get_openai_completion
import time


class MathPrompter:
    def __init__(self, model="text-davinci-003", max_tries_validation=5, repeat=5):
        """
        :param model: The OpenAI model to use
        :param max_tries_validation: The maximum number of tries to get a valid prompt
        :param repeat: The number of times to repeat the process (majority response is returned)
        """
        self.model = model
        self.max_tries_validation = max_tries_validation
        self.repeat = repeat

        self._initial_meta: PromptMeta = {
            "n_calls": 0,
            "duration": None
        }

        # reset after every prompt
        self.prompt_meta = self._initial_meta

    def prompt(self, prompt: str) -> (float, PromptMeta):
        self.prompt_meta = self._initial_meta
        prompt_info = extract_prompt_info(prompt)
        results = []

        start = time.time()

        for _ in range(self.repeat):
            try:
                mapping_python, _ = self.get_valid_mappings(
                    prompt_info)

                formula = extract_eval(
                    mapping_python, completion_type="python")
                result = eval_formula(formula, prompt_info["original_values"])
                results.append(result)
            except ValidationTriesExceeded:
                print("ValidationTriesExceeded")
            except:
                pass

        print(results)

        if len(results) == 0:
            raise NoResults()

        results.sort(key=lambda x: results.count(x))
        results.reverse()

        self.prompt_meta["duration"] = time.time() - start

        return results[0], self.prompt_meta

    def get_valid_mappings(self, prompt: MappedItem) -> (str, str):
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

            current_try += 1
            generated_expression = None
            generated_python = None

        if generated_expression is None or generated_python is None:
            raise ValidationTriesExceeded(
                f"Could not find a valid mapping for prompt: {prompt['question']}")

        return generated_python, generated_expression

    def _call_openai(self, prompt: str):
        self.prompt_meta["n_calls"] += 1
        return get_openai_completion(prompt)
