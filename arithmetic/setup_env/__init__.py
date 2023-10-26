import os


def setup_env():
    """Create the output directory if it doesn't exist."""
    os.makedirs("out", exist_ok=True)
