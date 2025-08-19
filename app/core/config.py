import os
from dotenv import load_dotenv
import traceback
from google.cloud import bigquery
from google.oauth2 import service_account

load_dotenv()

def get_env_variable(name: str, default=None):
    return os.getenv(name, default)

def log_error_to_file(error):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{str(error)}\n")
        f.write(traceback.format_exc())
        f.write("\n---\n")

def get_bigquery_client():
    prod_credentials = get_env_variable("GCP_SERVICE_ACCOUNT")
    credentials = service_account.Credentials.from_service_account_file(prod_credentials)
    client = bigquery.Client(credentials=credentials)
    return client