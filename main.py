from dotenv import load_dotenv
from arithmetic import arithmetic
from arithmetic.setup_env import setup_env


if __name__ == "__main__":
    load_dotenv()
    setup_env()
    arithmetic.run_experiment()
