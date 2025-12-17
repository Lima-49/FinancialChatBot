from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuração do banco de dados"""
    host: str
    port: int
    database: str
    user: str
    password: str

class PostgresService:
    """Serviço para interações com PostgreSQL seguindo o modelo ConfigAccountModel"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        if config is None:
            config = self._load_config_from_env()
        self.config = config
        self._connection = None
        
    def _load_config_from_env(self) -> DatabaseConfig:
        """Carrega configuração das variáveis de ambiente"""
        return DatabaseConfig(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
            database=os.getenv('POSTGRES_DB', 'CONTROLE_FINANCEIRO'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', '1234')
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                cursor_factory=RealDictCursor
            )
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro na conexão com o banco: {e}")
            raise
        finally:
            if conn:
                conn.close()
