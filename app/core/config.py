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

def get_bigquery_client():
    prod_credentials = get_env_variable("GCP_SERVICE_ACCOUNT")
    credentials = service_account.Credentials.from_service_account_file(prod_credentials)
    client = bigquery.Client(credentials=credentials)
    return client