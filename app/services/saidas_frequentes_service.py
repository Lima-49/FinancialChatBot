from typing import Optional, List
from app.services.postgres_service import PostgresService
from models.saidas_frequentes_model import SaidasFrequentesModel

class SaidasFrequentesService():
    def __init__(self):
        self.postgres_service = PostgresService()

    def get_all_saidas_frequentes(self) -> List[SaidasFrequentesModel]:
        """Retorna todas as saídas frequentes."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "saidas_frequentes"')
                rows = cur.fetchall()
                return [SaidasFrequentesModel.from_dict(row) for row in rows]
    
    def get_saida_frequente_by_id(self, id_saida: int) -> Optional[SaidasFrequentesModel]:
        """Retorna uma saída frequente específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "saidas_frequentes" WHERE "id_saida_frequente" = %s', (id_saida,))
                row = cur.fetchone()
                return SaidasFrequentesModel.from_dict(row) if row else None
    
    def insert_saida_frequente(self, nome_saida: str, tipo_saida: str, valor_saida: float, dia_saida: int) -> int:
        """Insere uma nova saída frequente."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "saidas_frequentes" ("nome_saida", "tipo_saida", "valor_saida", "dia_saida") VALUES (%s, %s, %s, %s) RETURNING "id_saida_frequente"',
                    (nome_saida, tipo_saida, valor_saida, dia_saida)
                )
                result = cur.fetchone()
                return result['id_saida_frequente'] if isinstance(result, dict) else result[0]
    
    def update_saida_frequente(self, id_saida: int, nome_saida: str = None, tipo_saida: str = None, valor_saida: float = None, dia_saida: int = None) -> bool:
        """Atualiza dados de uma saída frequente."""
        updates = []
        params = []
        
        if nome_saida is not None:
            updates.append('"nome_saida" = %s')
            params.append(nome_saida)
        if tipo_saida is not None:
            updates.append('"tipo_saida" = %s')
            params.append(tipo_saida)
        if valor_saida is not None:
            updates.append('"valor_saida" = %s')
            params.append(valor_saida)
        if dia_saida is not None:
            updates.append('"dia_saida" = %s')
            params.append(dia_saida)
        
        if not updates:
            return False
        
        params.append(id_saida)
        query = f'UPDATE "saidas_frequentes" SET {", ".join(updates)} WHERE "id_saida_frequente" = %s'
        
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_saida_frequente(self, id_saida: int) -> bool:
        """Deleta uma saída frequente."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "saidas_frequentes" WHERE "id_saida_frequente" = %s', (id_saida,))
                return cur.rowcount > 0