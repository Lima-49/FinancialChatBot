import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str, default=None):
    return os.getenv(name, default)