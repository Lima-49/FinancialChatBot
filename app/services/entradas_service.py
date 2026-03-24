from datetime import datetime
from typing import Optional, List
from app.services.postgres_service import PostgresService
from app.models.entradas_realizadas_model import EntradasRealizadasModel

class EntradasService():
    def __init__(self):
        self.postgres_service = PostgresService()
        self.entradas_model = EntradasRealizadasModel()
        self.table_name = "entradas_realizadas"

    def get_all_entradas(self) -> List[EntradasRealizadasModel]:
        """Retorna todas as entradas."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}"')
                rows = cur.fetchall()
                return [self.entradas_model.from_dict(row) for row in rows]
    
    def get_entrada_by_id(self, id_entrada: int) -> Optional[EntradasRealizadasModel]:
        """Retorna uma entrada específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_entrada" = %s', (id_entrada,))
                row = cur.fetchone()
                return self.entradas_model.from_dict(row) if row else None
    
    def get_entradas_by_banco(self, id_banco: int) -> List[EntradasRealizadasModel]:
        """Retorna todas as entradas de um banco."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_banco" = %s', (id_banco,))
                rows = cur.fetchall()
                return [self.entradas_model.from_dict(row) for row in rows]
    
    def insert_entrada(self, id_banco: int, id_categoria: int, valor_entrada: float, data_entrada: datetime, descricao: str = None) -> int:
        """Insere uma nova entrada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'INSERT INTO "{self.table_name}" ("id_banco", "id_categoria", "valor", "data_entrada", "descricao") VALUES (%s, %s, %s, %s, %s) RETURNING "id_entrada"',
                    (id_banco, id_categoria, valor_entrada, data_entrada, descricao)
                )
                result = cur.fetchone()
                return result['id_entrada'] if isinstance(result, dict) else result[0]

    def update_entrada(self, id_entrada: int, id_banco: int = None, id_categoria: int = None, valor: float = None, data_entrada: datetime = None, descricao: str = None) -> bool:
        """Atualiza dados de uma entrada."""
        updates = []
        params = []
        
        if id_banco is not None:
            updates.append('"id_banco" = %s')
            params.append(id_banco)
        if data_entrada is not None:
            updates.append('"data_entrada" = %s')
            params.append(data_entrada)
        if valor is not None:
            updates.append('"valor" = %s')
            params.append(valor)
        if descricao is not None:
            updates.append('"descricao" = %s')
            params.append(descricao)
        if id_categoria is not None:
            updates.append('"id_categoria" = %s')
            params.append(id_categoria)
        
        if not updates:
            return False
        
        params.append(id_entrada)
        query = f'UPDATE "{self.table_name}" SET {", ".join(updates)} WHERE "id_entrada" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_entrada(self, id_entrada: int) -> bool:
        """Deleta uma entrada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM "{self.table_name}" WHERE "id_entrada" = %s', (id_entrada,))
                return cur.rowcount > 0