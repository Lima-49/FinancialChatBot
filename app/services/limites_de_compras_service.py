from typing import Optional, List
from app.services.postgres_service import PostgresService
from models.limites_de_compras_model import LimitesDeComprasModel

class LimitesDeComprasService():
    """Serviço para interações com limites de compras."""
    def __init__(self):
        self.postgres_service = PostgresService()
        self.limites_de_compras_model = LimitesDeComprasModel()
    
    def get_all_limites(self) -> List[LimitesDeComprasModel]:
        """Retorna todos os limites de compras."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "limites_compras"')
                rows = cur.fetchall()
                return [self.limites_de_compras_model.from_dict(row) for row in rows]
    
    def get_limite_by_id(self, id_limite: int) -> Optional[LimitesDeComprasModel]:
        """Retorna um limite específico por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "limites_compras" WHERE "id_limite_compra" = %s', (id_limite,))
                row = cur.fetchone()
                return self.limites_de_compras_model.from_dict(row) if row else None
    
    def get_limite_by_categoria(self, id_categoria: int) -> Optional[LimitesDeComprasModel]:
        """Retorna o limite de uma categoria específica."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "limites_compras" WHERE "id_categoria" = %s', (id_categoria,))
                row = cur.fetchone()
                return self.limites_de_compras_model.from_dict(row) if row else None
    
    def insert_limite(self, id_categoria: int, limite_categoria: float) -> int:
        """Insere um novo limite de compra."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "limites_compras" ("id_categoria", "limite_categoria") VALUES (%s, %s) RETURNING "id_limite_compra"',
                    (id_categoria, limite_categoria)
                )
                result = cur.fetchone()
                result_model = self.limites_de_compras_model.from_dict(result) if isinstance(result, dict) else result
                return result_model.id_limite_compra
    
    def update_limite(self, id_limite: int, id_categoria: int = None, limite_categoria: float = None) -> bool:
        """Atualiza dados de um limite."""
        updates = []
        params = []
        
        if id_categoria is not None:
            updates.append('"id_categoria" = %s')
            params.append(id_categoria)
        if limite_categoria is not None:
            updates.append('"limite_categoria" = %s')
            params.append(limite_categoria)
        
        if not updates:
            return False
        
        params.append(id_limite)
        query = f'UPDATE "limites_compras" SET {", ".join(updates)} WHERE "id_limite_compra" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_limite(self, id_limite: int) -> bool:
        """Deleta um limite."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "limites_compras" WHERE "id_limite_compra" = %s', (id_limite,))
                return cur.rowcount > 0
