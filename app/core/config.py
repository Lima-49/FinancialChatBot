import os
from dotenv import load_dotenv
import traceback
from google.cloud import bigquery
from google.oauth2 import service_account
import logging

load_dotenv()

LOG_FILE = os.path.join(os.path.dirname(__file__), "../../app/logs/error_log.txt")

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=LOG_FILE,
    filemode="a",
)

logger = logging.getLogger("controle_financeiro")


def get_env_variable(name: str, default=None):
    return os.getenv(name, default)

def log_error_to_file(error):
    logger.error(str(error), exc_info=True)

# URL do site para configuração da conta (ex: Streamlit)
SITE_CONFIG_URL = get_env_variable("SITE_CONFIG_URL", "https://seu-site-de-config.com")

def get_site_config_url() -> str:
    return SITE_CONFIG_URL