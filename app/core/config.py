import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


# Import do serviço de logs - importação lazy para evitar dependência circular
def get_log_service():
    from app.services.logs_service import log_service

    return log_service


def get_env_variable(name: str, default=None):
    return os.getenv(name, default)


def log_error_to_file(error):
    get_log_service().error(str(error), exc_info=True)


# Ambiente da aplicação: local, development, production
APP_ENV = get_env_variable("APP_ENV", "local").strip().lower()


def is_local_environment() -> bool:
    return APP_ENV in ("local", "development", "dev")


def is_production_environment() -> bool:
    return APP_ENV == "production"


def get_database_url() -> str:
    """Retorna a URL de conexão para o banco de dados, preferindo variável explícita."""
    database_url = get_env_variable("DATABASE_URL")
    if database_url:
        return database_url

    # Fallbacks de convenção (para desenvolvimento local rápido)
    if is_local_environment():
        return "postgresql://user:password@localhost:5432/financial_control"

    raise RuntimeError("DATABASE_URL não encontrado. Defina DATABASE_URL no .env ou nas variáveis de ambiente.")


# URL do site para configuração da conta (ex: Streamlit)
SITE_CONFIG_URL = get_env_variable("SITE_CONFIG_URL", "https://seu-site-de-config.com")


def get_site_config_url() -> str:
    return SITE_CONFIG_URL


def generate_encryption_key() -> str:
    """
    Generates a new Fernet encryption key.
    Run this function ONCE and save the result in .env

    Example usage:
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
