class ValidationTriesExceeded(Exception):
    def __init__(self, message="MathPrompter failed to obtain convergent prompts within max_tries_validation"):
        super().__init__(message)


class NoResults(Exception):
    def __init__(self, message="MathPrompter failed to obtain any results with the variables provided for the problem"):
        super().__init__(message)
