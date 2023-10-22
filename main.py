from dotenv import load_dotenv
from arithmetic.setup_env import setup_env
from arithmetic import run_experiment


if __name__ == "__main__":
    load_dotenv()
    setup_env()
    run_experiment()
