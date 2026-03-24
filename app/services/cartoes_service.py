from typing import Optional, List
from app.services.postgres_service import PostgresService
from app.models.cartoes_model import CartoesModel    

class CartoesService:
    def __init__(self):
        self.postgres_service = PostgresService()
        self.cartao_model = CartoesModel()
        self.table_name = "cartoes"
    
    def get_all_cartoes(self) -> List[CartoesModel]:
        """Retorna todos os cartões de crédito."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}"')
                rows = cur.fetchall()
                return [self.cartao_model.from_dict(row) for row in rows]
    
    def get_cartao_by_id(self, id_cartao: int) -> Optional[CartoesModel]:
        """Retorna um cartão específico por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_cartao" = %s', (id_cartao,))
                row = cur.fetchone()
                return self.cartao_model.from_dict(row) if row else None
    
    def get_cartoes_by_banco(self, id_banco: int) -> List[CartoesModel]:
        """Retorna todos os cartões de um banco."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_banco" = %s', (id_banco,))
                rows = cur.fetchall()
                return [self.cartao_model.from_dict(row) for row in rows]
    
    def insert_cartao(self, id_banco: int, nome_cartao: str, tipo_cartao: int, dia_vencimento: int) -> int:
        """Insere um novo cartão de crédito."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'INSERT INTO "{self.table_name}" ("id_banco", "nome_cartao", "tipo_cartao", "dia_vencimento") VALUES (%s, %s, %s, %s) RETURNING "id_cartao"',
                    (id_banco, nome_cartao, tipo_cartao, dia_vencimento)
                )
                result = cur.fetchone()
                return result['id_cartao'] if isinstance(result, dict) else result[0]
    
    def update_cartao(self, id_cartao: int, id_banco: int = None, nome_cartao: str = None, tipo_cartao: int = None, dia_vencimento: int = None) -> bool:
        """Atualiza dados de um cartão."""
        updates = []
        params = []
        
        if id_banco is not None:
            updates.append('"id_banco" = %s')
            params.append(id_banco)
        if nome_cartao is not None:
            updates.append('"nome_cartao" = %s')
            params.append(nome_cartao)
        if tipo_cartao is not None:
            updates.append('"tipo_cartao" = %s')
            params.append(tipo_cartao)
        if dia_vencimento is not None:
            updates.append('"dia_vencimento" = %s')
            params.append(dia_vencimento)
        
        if not updates:
            return False
        
        params.append(id_cartao)
        query = f'UPDATE "{self.table_name}" SET {", ".join(updates)} WHERE "id_cartao" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_cartao(self, id_cartao: int) -> bool:
        """Deleta um cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM "{self.table_name}" WHERE "id_cartao" = %s', (id_cartao,))
                return cur.rowcount > 0