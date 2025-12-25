from typing import Optional, List
from app.services.postgres_service import PostgresService
from models.bancos_model import BancosModel

class BancosService:
    def __init__(self):
        self.postgres_service = PostgresService()
        self.banco_model = BancosModel()

    def get_all_bancos(self) -> List[BancosModel]:
        """Retorna todos os bancos cadastrados."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "bancos"')
                rows = cur.fetchall()
                return [self.banco_model.from_dict(row).to_dict() for row in rows]
    
    def get_banco_by_id(self, id_banco: int) -> Optional[BancosModel]:
        """Retorna um banco específico por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "bancos" WHERE "id_banco" = %s', (id_banco,))
                row = cur.fetchone()
                return self.banco_model.from_dict(row).to_dict() if row else None
    
    def insert_banco(self, nome_banco: str, valor_em_conta: float = 0.0, valor_investido: float = 0.0) -> int:
        """Insere um novo banco e retorna o ID gerado."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "bancos" ("nome_banco", "valor_em_conta", "valor_investido") VALUES (%s, %s, %s) RETURNING "id_banco"',
                    (nome_banco, valor_em_conta, valor_investido)
                )
                result = cur.fetchone()
                return result['id_banco'] if isinstance(result, dict) else result[0]
    
    def update_banco(self, id_banco: int, nome_banco: str = None, valor_em_conta: float = None, valor_investido: float = None) -> bool:
        """Atualiza dados de um banco."""
        updates = []
        params = []
        
        if nome_banco is not None:
            updates.append('"nome_banco" = %s')
            params.append(nome_banco)
        if valor_em_conta is not None:
            updates.append('"valor_em_conta" = %s')
            params.append(valor_em_conta)
        if valor_investido is not None:
            updates.append('"valor_investido" = %s')
            params.append(valor_investido)
        
        if not updates:
            return False
        
        params.append(id_banco)
        query = f'UPDATE "bancos" SET {", ".join(updates)} WHERE "id_banco" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_banco(self, id_banco: int) -> bool:
        """Deleta um banco."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "bancos" WHERE "id_banco" = %s', (id_banco,))
                return cur.rowcount > 0

  