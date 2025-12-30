from typing import Optional, List
from app.services.postgres_service import PostgresService
from datetime import date
from app.models.compras_cartoes_de_credito_model import ComprasCartoesDeCreditoModel

class ComprasCartaoDeCreditoService:
    def __init__(self):
        self.postgres_service = PostgresService()
        self.compras_cartoes_de_credito_model = ComprasCartoesDeCreditoModel()
    
    def get_all_compras_cartao(self) -> List[ComprasCartoesDeCreditoModel]:
        """Retorna todas as compras de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "compras_cartoes_de_credito"')
                rows = cur.fetchall()
                return [self.compras_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def get_compra_cartao_by_id(self, id_compra: int) -> Optional[ComprasCartoesDeCreditoModel]:
        """Retorna uma compra específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "compras_cartoes_de_credito" WHERE "id_compra_cartao_credito" = %s', (id_compra,))
                row = cur.fetchone()
                return self.compras_cartoes_de_credito_model.from_dict(row) if row else None
    
    def get_compras_by_cartao(self, id_cartao: int) -> List[ComprasCartoesDeCreditoModel]:
        """Retorna todas as compras de um cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "compras_cartoes_de_credito" WHERE "id_cartao" = %s', (id_cartao,))
                rows = cur.fetchall()
                return [self.compras_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def get_compras_by_categoria(self, id_categoria: int) -> List[ComprasCartoesDeCreditoModel]:
        """Retorna todas as compras de uma categoria."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "compras_cartoes_de_credito" WHERE "id_categoria" = %s', (id_categoria,))
                rows = cur.fetchall()
                return [self.compras_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def insert_compra_cartao(self, id_cartao: int, id_banco: int, data_compra: date, estabelecimento: str, 
                             parcelas: str, id_categoria: int, valor_compra: float, observacoes: str = None) -> int:
        """Insere uma nova compra de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "compras_cartoes_de_credito" ("id_cartao", "id_banco", "data_compra", "estabelecimento", "parcelas", "id_categoria", "valor_compra", "observacoes") VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "id_compra_cartao_credito"',
                    (id_cartao, id_banco, data_compra, estabelecimento, parcelas, id_categoria, valor_compra, observacoes)
                )
                result = cur.fetchone()
                return result['id_compra_cartao_credito'] if isinstance(result, dict) else result[0]
    
    def update_compra_cartao(self, id_compra: int, id_cartao: int = None, id_banco: int = None, data_compra: date = None, 
                            estabelecimento: str = None, parcelas: str = None, id_categoria: int = None, 
                            valor_compra: float = None, observacoes: str = None) -> bool:
        """Atualiza dados de uma compra de cartão."""
        updates = []
        params = []
        
        if id_cartao is not None:
            updates.append('"id_cartao" = %s')
            params.append(id_cartao)
        if id_banco is not None:
            updates.append('"id_banco" = %s')
            params.append(id_banco)
        if data_compra is not None:
            updates.append('"data_compra" = %s')
            params.append(data_compra)
        if estabelecimento is not None:
            updates.append('"estabelecimento" = %s')
            params.append(estabelecimento)
        if parcelas is not None:
            updates.append('"parcelas" = %s')
            params.append(parcelas)
        if id_categoria is not None:
            updates.append('"id_categoria" = %s')
            params.append(id_categoria)
        if valor_compra is not None:
            updates.append('"valor_compra" = %s')
            params.append(valor_compra)
        if observacoes is not None:
            updates.append('"observacoes" = %s')
            params.append(observacoes)
        
        if not updates:
            return False
        
        params.append(id_compra)
        query = f'UPDATE "compras_cartoes_de_credito" SET {", ".join(updates)} WHERE "id_compra_cartao_credito" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_compra_cartao(self, id_compra: int) -> bool:
        """Deleta uma compra de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "compras_cartoes_de_credito" WHERE "id_compra_cartao_credito" = %s', (id_compra,))
                return cur.rowcount > 0