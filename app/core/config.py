import os
from dotenv import load_dotenv
import logging
from cryptography.fernet import Fernet

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


def generate_encryption_key() -> str:
    """
    Gera uma nova chave de criptografia Fernet.
    Execute esta função UMA VEZ e salve o resultado no .env
    
    Exemplo de uso:
    >>> from app.core.config import generate_encryption_key
    >>> print(generate_encryption_key())
    """
    return Fernet.generate_key().decode()


def get_encryption_key() -> str:
    """Recupera a chave de criptografia das variáveis de ambiente"""
    key = get_env_variable("CONVERSATION_ENCRYPTION_KEY")
    if not key:
        raise ValueError(
            "CONVERSATION_ENCRYPTION_KEY não encontrada. "
            "Use generate_encryption_key() para gerar uma nova chave."
        )
    return key
