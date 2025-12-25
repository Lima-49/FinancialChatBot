from typing import Dict
import psycopg2
import logging
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

class PostgresService:
    """Serviço para interações com PostgreSQL seguindo o modelo ConfigAccountModel"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self._connection = None
        
    def _ensure_connection(self):
        """
        Garante que existe uma conexão ativa. Cria uma nova se necessário.
        Usa RealDictCursor para retornar resultados como dicionários.
        """
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                self.database_url,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        return self._connection
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco - reutiliza conexão existente"""
        conn = None
        try:
            conn = self._ensure_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro na conexão com o banco: {e}")
            raise
    
    def close(self):
        """Fecha a conexão manualmente quando necessário"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None
    
    def _count_rows_for_table(self, table_name: str) -> int:
        """Conta linhas em uma tabela, tentando nomes não-aspados e aspados.
        Retorna -1 se a tabela não existir em ambos os casos.
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Primeiro tenta sem aspas (tabelas criadas sem aspas viram minúsculas)
                try:
                    cur.execute(f"SELECT COUNT(*) AS c FROM {table_name}")
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    pass
                # Depois tenta com aspas e nome conforme recebido
                try:
                    cur.execute(f'SELECT COUNT(*) AS c FROM "{table_name}"')
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    return -1

    def check_required_tables_status(self) -> Dict[str, int]:
        """Verifica o status das tabelas obrigatórias do sistema."""
        required_tables = [
            "bancos",
            "cartoes_de_credito",
            "entradas",
            "saidas_frequentes",
            "categorias_de_compras",
            "faturas_cartoes_de_credito",
        ]
        status = {}
        try:
            for t in required_tables:
                count = self._count_rows_for_table(t)
                status[t] = count
        except Exception:
            # Em caso de falha geral de conexão, marque todas como -1 (indefinido/não acessível)
            for t in required_tables:
                status[t] = -1
        return status