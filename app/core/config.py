import os
from dotenv import load_dotenv
import traceback

load_dotenv()

def get_env_variable(name: str, default=None):
    return os.getenv(name, default)

def log_error_to_file(error):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{str(error)}\n")
        f.write(traceback.format_exc())
        f.write("\n---\n")