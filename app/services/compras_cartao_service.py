from typing import Optional, List
from app.services.postgres_service import PostgresService
from datetime import date
from app.models.compras_cartoes_model import ComprasCartoesModel

class ComprasCartaoService:
    def __init__(self):
        self.postgres_service = PostgresService()
        self.compras_cartoes_model = ComprasCartoesModel()
        self.table_name = "compras_cartao"
    
    def get_all_compras_cartao(self) -> List[ComprasCartoesModel]:
        """Retorna todas as compras de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}"')
                rows = cur.fetchall()
                return [self.compras_cartoes_model.from_dict(row) for row in rows]
    
    def get_compra_cartao_by_id(self, id_compra: int) -> Optional[ComprasCartoesModel]:
        """Retorna uma compra específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_compra_cartao" = %s', (id_compra,))
                row = cur.fetchone()
                return self.compras_cartoes_model.from_dict(row) if row else None
    
    def get_compras_by_cartao(self, id_cartao: int) -> List[ComprasCartoesModel]:
        """Retorna todas as compras de um cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_cartao" = %s', (id_cartao,))
                rows = cur.fetchall()
                return [self.compras_cartoes_model.from_dict(row) for row in rows]
    
    def get_compras_by_categoria(self, id_categoria: int) -> List[ComprasCartoesModel]:
        """Retorna todas as compras de uma categoria."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_categoria" = %s', (id_categoria,))
                rows = cur.fetchall()
                return [self.compras_cartoes_model.from_dict(row) for row in rows]
    
    def insert_compra_cartao(self, id_cartao: int, data_compra: date, estabelecimento: str,
                             id_categoria: int, valor_compra: float, observacoes: str = None,
                             numero_parcelas: int = 1, parcela_atual: int = 1) -> int:
        """Insere uma nova compra de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'INSERT INTO "{self.table_name}" ("id_cartao", "data_compra", "estabelecimento", "id_categoria", "valor_compra", "observacoes", "numero_parcelas", "parcela_atual") VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "id_compra_cartao"',
                    (id_cartao, data_compra, estabelecimento, id_categoria, valor_compra, observacoes, numero_parcelas, parcela_atual)
                )
                result = cur.fetchone()
                return result['id_compra_cartao'] if isinstance(result, dict) else result[0]
    
    def update_compra_cartao(self, id_compra: int, id_cartao: int = None, data_compra: date = None, 
                            estabelecimento: str = None, id_categoria: int = None, 
                            valor_compra: float = None, observacoes: str = None,
                            numero_parcelas: int = None, parcela_atual: int = None) -> bool:
        """Atualiza dados de uma compra de cartão."""
        updates = []
        params = []
        
        if id_cartao is not None:
            updates.append('"id_cartao" = %s')
            params.append(id_cartao)
        if data_compra is not None:
            updates.append('"data_compra" = %s')
            params.append(data_compra)
        if estabelecimento is not None:
            updates.append('"estabelecimento" = %s')
            params.append(estabelecimento)
        if id_categoria is not None:
            updates.append('"id_categoria" = %s')
            params.append(id_categoria)
        if valor_compra is not None:
            updates.append('"valor_compra" = %s')
            params.append(valor_compra)
        if observacoes is not None:
            updates.append('"observacoes" = %s')
            params.append(observacoes)
        if numero_parcelas is not None:
            updates.append('"numero_parcelas" = %s')
            params.append(numero_parcelas)
        if parcela_atual is not None:
            updates.append('"parcela_atual" = %s')
            params.append(parcela_atual)
        
        if not updates:
            return False
        
        params.append(id_compra)
        query = f'UPDATE "{self.table_name}" SET {", ".join(updates)} WHERE "id_compra_cartao" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_compra_cartao(self, id_compra: int) -> bool:
        """Deleta uma compra de cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM "{self.table_name}" WHERE "id_compra_cartao" = %s', (id_compra,))
                return cur.rowcount > 0