import os
from contextlib import contextmanager
from typing import Dict

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Lazy import to avoid circular dependency
def get_log_service():
    try:
        from app.services.logs_service import log_service

        return log_service
    except ImportError:
        # Fallback to not break during initialization
        return None


from app.core.config import get_database_url


class PostgresService:
    """Service for PostgreSQL interactions following the ConfigAccountModel"""

    def __init__(self):
        self.database_url = get_database_url()
        self._connection = None

    def _ensure_connection(self):
        """
        Ensures an active connection exists. Creates a new one if necessary.
        Uses RealDictCursor to return results as dictionaries.
        """
        if self._connection is None or self._connection.closed:
            if not self.database_url:
                raise RuntimeError("DATABASE_URL is not configured in environment")

            try:
                self._connection = psycopg2.connect(
                    self.database_url,
                    cursor_factory=psycopg2.extras.RealDictCursor,
                )
            except Exception as e:
                log_svc = get_log_service()
                if log_svc:
                    log_svc.error(
                        f"Falha ao conectar no banco de dados ({self.database_url}): {e}",
                        exc_info=True,
                    )
                raise

        return self._connection

    @contextmanager
    def get_connection(self):
        """Context manager for database connections - reuses existing connection"""
        conn = None
        try:
            conn = self._ensure_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            log_svc = get_log_service()
            if log_svc:
                log_svc.error(f"Database connection error: {e}", exc_info=True)
            raise

    def close(self):
        """Manually closes the connection when necessary"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None

    def _count_rows_for_table(self, table_name: str) -> int:
        """Counts rows in a table, trying unquoted and quoted names.
        Returns -1 if the table does not exist in both cases.
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # First try without quotes (tables created without quotes become lowercase)
                try:
                    cur.execute(f"SELECT COUNT(*) AS c FROM {table_name}")
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    pass
                # Then try with quotes and name as received
                try:
                    cur.execute(f'SELECT COUNT(*) AS c FROM "{table_name}"')
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    return -1

    def check_required_tables_status(self) -> Dict[str, int]:
        """Checks the status of required system tables."""
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
            # In case of general connection failure, mark all as -1 (undefined/inaccessible)
            for t in required_tables:
                status[t] = -1
        return status
