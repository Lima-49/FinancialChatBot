from datetime import datetime
from typing import Optional, List
from app.services.postgres_service import PostgresService
from app.models.saidas_realizadas_model import SaidasRealizadasModel

class SaidasRealizadasService():
    def __init__(self):
        self.postgres_service = PostgresService()
        self.table_name = "saidas_realizadas"

    def get_all_saidas_realizadas(self) -> List[SaidasRealizadasModel]:
        """Retorna todas as saídas realizadas."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}"')
                rows = cur.fetchall()
                return [SaidasRealizadasModel.from_dict(row) for row in rows]
    
    def get_saida_realizada_by_id(self, id_saida: int) -> Optional[SaidasRealizadasModel]:
        """Retorna uma saída realizada específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_saida" = %s', (id_saida,))
                row = cur.fetchone()
                return SaidasRealizadasModel.from_dict(row) if row else None
    
    def insert_saida_realizada(self, id_categoria: int, id_banco: int, data_saida: datetime, valor: float, descricao: str) -> int:
        """Insere uma nova saída realizada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'INSERT INTO "{self.table_name}" ("id_categoria", "id_banco", "data_saida", "valor_saida", "descricao") VALUES (%s, %s, %s, %s, %s) RETURNING "id_saida"',
                    (id_categoria, id_banco, data_saida, valor, descricao)
                )
                result = cur.fetchone()
                return result['id_saida'] if isinstance(result, dict) else result[0]
    
    def update_saida_realizada(self, id_saida: int, id_categoria: int, id_banco: int, data_saida: datetime, valor: float, descricao: str) -> bool:
        """Atualiza dados de uma saída realizada."""
        updates = []
        params = []
        
        if id_categoria is not None:
            updates.append('"id_categoria" = %s')
            params.append(id_categoria)
        if id_banco is not None:
            updates.append('"id_banco" = %s')
            params.append(id_banco)
        if data_saida is not None:
            updates.append('"data_saida" = %s')
            params.append(data_saida)
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
        
        params.append(id_saida)
        query = f'UPDATE "{self.table_name}" SET {", ".join(updates)} WHERE "id_saida" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_saida_realizada(self, id_saida: int) -> bool:
        """Deleta uma saída realizada."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM "{self.table_name}" WHERE "id_saida" = %s', (id_saida,))
                return cur.rowcount > 0