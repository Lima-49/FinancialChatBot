import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# Import do serviço de logs - importação lazy para evitar dependência circular
def get_log_service():
    from app.services.logs_service import log_service
    return log_service


def get_env_variable(name: str, default=None):
    return os.getenv(name, default)

def log_error_to_file(error):
    get_log_service().error(str(error), exc_info=True)

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
