import datetime
from typing import Optional, List
from app.services.postgres_service import PostgresService
from app.models.faturas_cartoes_de_credito_model import FaturasCartoesDeCreditoModel

class FaturasCartoesDeCreditoService():
 
    def __init__(self):
        self.postgres_service = PostgresService()
        self.faturas_cartoes_de_credito_model = FaturasCartoesDeCreditoModel()
        self.table_name = "faturas_cartoes_de_credito"

    def get_all_faturas(self) -> List[FaturasCartoesDeCreditoModel]:
        """Retorna todas as faturas."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}"')
                rows = cur.fetchall()
                return [self.faturas_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def get_fatura_by_id(self, id_fatura: int) -> Optional[FaturasCartoesDeCreditoModel]:
        """Retorna uma fatura específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_fatura_cartao_credito" = %s', (id_fatura,))
                row = cur.fetchone()
                return self.faturas_cartoes_de_credito_model.from_dict(row) if row else None
    
    def get_faturas_by_cartao(self, id_cartao: int) -> List[FaturasCartoesDeCreditoModel]:
        """Retorna todas as faturas de um cartão."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "id_cartao" = %s', (id_cartao,))
                rows = cur.fetchall()
                return [self.faturas_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def get_faturas_by_mes_ano(self, mes: int, ano: int) -> List[FaturasCartoesDeCreditoModel]:
        """Retorna todas as faturas de um mês e ano específicos."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'SELECT * FROM "{self.table_name}" WHERE "mes_fatura" = %s AND "ano_fatura" = %s',
                    (mes, ano)
                )
                rows = cur.fetchall()
                return [self.faturas_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def get_faturas_nao_pagas(self) -> List[FaturasCartoesDeCreditoModel]:
        """Retorna todas as faturas não pagas."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM "{self.table_name}" WHERE "paga" = false'   )
                rows = cur.fetchall()
                return [self.faturas_cartoes_de_credito_model.from_dict(row) for row in rows]
    
    def insert_fatura(self, id_cartao: int, data_fatura: datetime, data_vencimento: datetime, mes_fatura: int, ano_fatura: int, 
                     valor_fatura: float, paga: bool = False) -> int:
        """Insere uma nova fatura."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f'INSERT INTO "{self.table_name}" ("id_cartao", "data_fatura", "data_vencimento", "mes_fatura", "ano_fatura", "valor_fatura", "paga") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING "id_fatura_cartao_credito"',
                    (id_cartao, data_fatura, data_vencimento, mes_fatura, ano_fatura, valor_fatura, paga)
                )
                result = cur.fetchone()
                result_model = self.faturas_cartoes_de_credito_model.from_dict(result) if isinstance(result, dict) else result
                return result_model.id_fatura_cartao_credito
            
    def update_fatura(self, id_fatura: int, id_cartao: int = None, data_fatura: datetime = None, data_vencimento: datetime = None, valor_fatura: float = None, paga: bool = None) -> bool:
        """Atualiza dados de uma fatura."""
        updates = []
        params = []
        
        if id_cartao is not None:
            updates.append('"id_cartao" = %s')
            params.append(id_cartao)
        if data_fatura is not None:
            updates.append('"data_fatura" = %s')
            params.append(data_fatura)
        if data_vencimento is not None:
            updates.append('"data_vencimento" = %s')
            params.append(data_vencimento)
        if valor_fatura is not None:
            updates.append('"valor_fatura" = %s')
            params.append(valor_fatura)
        if paga is not None:
            updates.append('"paga" = %s')
            params.append(paga)
        
        if not updates:
            return False
        
        params.append(id_fatura)
        query = f'UPDATE "{self.table_name}" SET {", ".join(updates)} WHERE "id_fatura_cartao_credito" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_fatura(self, id_fatura: int) -> bool:
        """Deleta uma fatura."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DELETE FROM "{self.table_name}" WHERE "id_fatura_cartao_credito" = %s', (id_fatura,))
                return cur.rowcount > 0
