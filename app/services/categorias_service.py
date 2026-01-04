from typing import Optional, List
from app.services.postgres_service import PostgresService
from app.models.categorias_model import CategoriasModel 

class CategoriasService():
    def __init__(self):
        self.postgres_service = PostgresService()
        self.categorias_model = CategoriasModel()

    def get_all_categorias(self) -> List[CategoriasModel]:
        """Retorna todas as categorias de compras."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "categorias_de_compras"')
                rows = cur.fetchall()
                return [self.categorias_model.from_dict(row) for row in rows]
    
    def get_categoria_by_id(self, id_categoria: int) -> Optional[CategoriasModel]:
        """Retorna uma categoria específica por ID."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "categorias_de_compras" WHERE "id_categoria" = %s', (id_categoria,))
                row = cur.fetchone()
                return self.categorias_model.from_dict(row) if row else None
    
    def get_categoria_by_nome(self, nome_categoria: str) -> Optional[CategoriasModel]:
        """Retorna uma categoria específica por nome (case-insensitive)."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "categorias_de_compras" WHERE LOWER("nome_categoria") = LOWER(%s)', (nome_categoria,))
                row = cur.fetchone()
                return self.categorias_model.from_dict(row) if row else None
    
    def get_or_create_categoria(self, nome_categoria: str) -> int:
        """Busca categoria por nome ou cria se não existir. Retorna o ID da categoria."""
        categoria = self.get_categoria_by_nome(nome_categoria)
        if categoria:
            return categoria.id_categoria
        return self.insert_categoria(nome_categoria)
    
    def insert_categoria(self, nome_categoria: str) -> int:
        """Insere uma nova categoria."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "categorias_de_compras" ("nome_categoria") VALUES (%s) RETURNING "id_categoria"',
                    (nome_categoria,)
                )
                result = cur.fetchone()
                return result['id_categoria'] if isinstance(result, dict) else result[0]
    
    def update_categoria(self, id_categoria: int, nome_categoria: str) -> bool:
        """Atualiza dados de uma categoria."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE "categorias_de_compras" SET "nome_categoria" = %s WHERE "id_categoria" = %s',
                    (nome_categoria, id_categoria)
                )
                return cur.rowcount > 0
    
    def delete_categoria(self, id_categoria: int) -> bool:
        """Deleta uma categoria."""
        with self.postgres_service.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "categorias_de_compras" WHERE "id_categoria" = %s', (id_categoria,))
                return cur.rowcount > 0