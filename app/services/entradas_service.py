from typing import Any, Optional, List
from app.services.postgres_service import PostgresService
from app.models.entradas_model import EntradasModel

class EntradasService():
    def __init__(self):
        self.postgres_service = PostgresService()
        self.entradas_model = EntradasModel()

    def get_all_entradas(self) -> List[EntradasModel]:
        """Retorna todas as entradas."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "entradas"')
                rows = cur.fetchall()
                return [self.entradas_model.from_dict(row).to_dict() for row in rows]
    
    def get_entrada_by_id(self, id_entrada: int) -> Optional[EntradasModel]:
        """Retorna uma entrada específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "entradas" WHERE "id_entrada" = %s', (id_entrada,))
                row = cur.fetchone()
                return self.entradas_model.from_dict(row).to_dict() if row else None
    
    def get_entradas_by_banco(self, id_banco: int) -> List[EntradasModel]:
        """Retorna todas as entradas de um banco."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "entradas" WHERE "id_banco" = %s', (id_banco,))
                rows = cur.fetchall()
                return [self.entradas_model.from_dict(row).to_dict() for row in rows]
    
    def insert_entrada(self, id_banco: int, nome_entrada: str, tipo_entrada: str, valor_entrada: float, dia_entrada: int) -> int:
        """Insere uma nova entrada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "entradas" ("id_banco", "nome_entrada", "tipo_entrada", "valor_entrada", "dia_entrada") VALUES (%s, %s, %s, %s, %s) RETURNING "id_entrada"',
                    (id_banco, nome_entrada, tipo_entrada, valor_entrada, dia_entrada)
                )
                result = cur.fetchone()
                return result['id_entrada'] if isinstance(result, dict) else result[0]
            
    def update_entrada(self, id_entrada: int, id_banco: int = None, nome_entrada: str = None, tipo_entrada: str = None, valor_entrada: float = None, dia_entrada: int = None) -> bool:
        """Atualiza dados de uma entrada."""
        updates = []
        params = []
        
        if id_banco is not None:
            updates.append('"id_banco" = %s')
            params.append(id_banco)
        if nome_entrada is not None:
            updates.append('"nome_entrada" = %s')
            params.append(nome_entrada)
        if tipo_entrada is not None:
            updates.append('"tipo_entrada" = %s')
            params.append(tipo_entrada)
        if valor_entrada is not None:
            updates.append('"valor_entrada" = %s')
            params.append(valor_entrada)
        if dia_entrada is not None:
            updates.append('"dia_entrada" = %s')
            params.append(dia_entrada)
        
        if not updates:
            return False
        
        params.append(id_entrada)
        query = f'UPDATE "entradas" SET {", ".join(updates)} WHERE "id_entrada" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_entrada(self, id_entrada: int) -> bool:
        """Deleta uma entrada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "entradas" WHERE "id_entrada" = %s', (id_entrada,))
                return cur.rowcount > 0