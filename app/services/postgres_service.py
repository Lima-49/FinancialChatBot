from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
import os
from dataclasses import dataclass
from datetime import date

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuração do banco de dados"""
    host: str
    port: int
    database: str
    user: str
    password: str

class PostgresService:
    """Serviço para interações com PostgreSQL seguindo o modelo ConfigAccountModel"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        if config is None:
            config = self._load_config_from_env()
        self.config = config
        self._connection = None
        
    def _load_config_from_env(self) -> DatabaseConfig:
        """Carrega configuração das variáveis de ambiente"""
        return DatabaseConfig(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
            database=os.getenv('POSTGRES_DB', 'CONTROLE_FINANCEIRO'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', '1234')
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                cursor_factory=RealDictCursor
            )
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Erro na conexão com o banco: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _count_rows_for_table(self, table_name: str) -> int:
        """Conta linhas em uma tabela, tentando nomes não-aspados e aspados.
        Retorna -1 se a tabela não existir em ambos os casos.
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Primeiro tenta sem aspas (tabelas criadas sem aspas viram minúsculas)
                try:
                    cur.execute(f"SELECT COUNT(*) AS c FROM {table_name}")
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    pass
                # Depois tenta com aspas e nome conforme recebido
                try:
                    cur.execute(f'SELECT COUNT(*) AS c FROM "{table_name}"')
                    row = cur.fetchone()
                    return int(row["c"]) if isinstance(row, dict) else int(row[0])
                except Exception:
                    return -1

    def check_required_tables_status(self) -> Dict[str, int]:
        """Verifica o status das tabelas obrigatórias do sistema."""
        required_tables = [
            "BANCOS",
            "CARTOES_DE_CREDITO",
            "ENTRADAS",
            "SAIDAS_FREQUENTES",
            "CATEGORIAS_DE_COMPRAS",
            "FATURAS_CARTOES_DE_CREDITO",
        ]
        status = {}
        try:
            for t in required_tables:
                count = self._count_rows_for_table(t)
                status[t] = count
        except Exception:
            # Em caso de falha geral de conexão, marque todas como -1 (indefinido/não acessível)
            for t in required_tables:
                status[t] = -1
        return status

    # ==================== BANCOS ====================
    
    def get_all_bancos(self) -> List[Dict[str, Any]]:
        """Retorna todos os bancos cadastrados."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "BANCOS"')
                return cur.fetchall()
    
    def get_banco_by_id(self, id_banco: int) -> Optional[Dict[str, Any]]:
        """Retorna um banco específico por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "BANCOS" WHERE "ID_BANCO" = %s', (id_banco,))
                return cur.fetchone()
    
    def insert_banco(self, nome_banco: str, valor_em_conta: float = 0.0, valor_investido: float = 0.0) -> int:
        """Insere um novo banco e retorna o ID gerado."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "BANCOS" ("NOME_BANCO", "VALOR_EM_CONTA", "VALOR_INVESTIDO") VALUES (%s, %s, %s) RETURNING "ID_BANCO"',
                    (nome_banco, valor_em_conta, valor_investido)
                )
                result = cur.fetchone()
                return result['ID_BANCO'] if isinstance(result, dict) else result[0]
    
    def update_banco(self, id_banco: int, nome_banco: str = None, valor_em_conta: float = None, valor_investido: float = None) -> bool:
        """Atualiza dados de um banco."""
        updates = []
        params = []
        
        if nome_banco is not None:
            updates.append('"NOME_BANCO" = %s')
            params.append(nome_banco)
        if valor_em_conta is not None:
            updates.append('"VALOR_EM_CONTA" = %s')
            params.append(valor_em_conta)
        if valor_investido is not None:
            updates.append('"VALOR_INVESTIDO" = %s')
            params.append(valor_investido)
        
        if not updates:
            return False
        
        params.append(id_banco)
        query = f'UPDATE "BANCOS" SET {", ".join(updates)} WHERE "ID_BANCO" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_banco(self, id_banco: int) -> bool:
        """Deleta um banco."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "BANCOS" WHERE "ID_BANCO" = %s', (id_banco,))
                return cur.rowcount > 0

    # ==================== CARTÕES DE CRÉDITO ====================
    
    def get_all_cartoes(self) -> List[Dict[str, Any]]:
        """Retorna todos os cartões de crédito."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "CARTOES_DE_CREDITO"')
                return cur.fetchall()
    
    def get_cartao_by_id(self, id_cartao: int) -> Optional[Dict[str, Any]]:
        """Retorna um cartão específico por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "CARTOES_DE_CREDITO" WHERE "ID_CARTAO" = %s', (id_cartao,))
                return cur.fetchone()
    
    def get_cartoes_by_banco(self, id_banco: int) -> List[Dict[str, Any]]:
        """Retorna todos os cartões de um banco."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "CARTOES_DE_CREDITO" WHERE "ID_BANCO" = %s', (id_banco,))
                return cur.fetchall()
    
    def insert_cartao(self, id_banco: int, nome_cartao: str, tipo_cartao: int, dia_vencimento: int) -> int:
        """Insere um novo cartão de crédito."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "CARTOES_DE_CREDITO" ("ID_BANCO", "NOME_CARTAO", "TIPO_CARTAO", "DIA_VENCIMENTO") VALUES (%s, %s, %s, %s) RETURNING "ID_CARTAO"',
                    (id_banco, nome_cartao, tipo_cartao, dia_vencimento)
                )
                result = cur.fetchone()
                return result['ID_CARTAO'] if isinstance(result, dict) else result[0]
    
    def update_cartao(self, id_cartao: int, id_banco: int = None, nome_cartao: str = None, tipo_cartao: int = None, dia_vencimento: int = None) -> bool:
        """Atualiza dados de um cartão."""
        updates = []
        params = []
        
        if id_banco is not None:
            updates.append('"ID_BANCO" = %s')
            params.append(id_banco)
        if nome_cartao is not None:
            updates.append('"NOME_CARTAO" = %s')
            params.append(nome_cartao)
        if tipo_cartao is not None:
            updates.append('"TIPO_CARTAO" = %s')
            params.append(tipo_cartao)
        if dia_vencimento is not None:
            updates.append('"DIA_VENCIMENTO" = %s')
            params.append(dia_vencimento)
        
        if not updates:
            return False
        
        params.append(id_cartao)
        query = f'UPDATE "CARTOES_DE_CREDITO" SET {", ".join(updates)} WHERE "ID_CARTAO" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_cartao(self, id_cartao: int) -> bool:
        """Deleta um cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "CARTOES_DE_CREDITO" WHERE "ID_CARTAO" = %s', (id_cartao,))
                return cur.rowcount > 0

    # ==================== ENTRADAS ====================
    
    def get_all_entradas(self) -> List[Dict[str, Any]]:
        """Retorna todas as entradas."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "ENTRADAS"')
                return cur.fetchall()
    
    def get_entrada_by_id(self, id_entrada: int) -> Optional[Dict[str, Any]]:
        """Retorna uma entrada específica por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "ENTRADAS" WHERE "ID_ENTRADA" = %s', (id_entrada,))
                return cur.fetchone()
    
    def get_entradas_by_banco(self, id_banco: int) -> List[Dict[str, Any]]:
        """Retorna todas as entradas de um banco."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "ENTRADAS" WHERE "ID_BANCO" = %s', (id_banco,))
                return cur.fetchall()
    
    def insert_entrada(self, id_banco: int, nome_entrada: str, tipo_entrada: str, valor_entrada: float, dia_entrada: int) -> int:
        """Insere uma nova entrada."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "ENTRADAS" ("ID_BANCO", "NOME_ENTRADA", "TIPO_ENTRADA", "VALOR_ENTRADA", "DIA_ENTRADA") VALUES (%s, %s, %s, %s, %s) RETURNING "ID_ENTRADA"',
                    (id_banco, nome_entrada, tipo_entrada, valor_entrada, dia_entrada)
                )
                result = cur.fetchone()
                return result['ID_ENTRADA'] if isinstance(result, dict) else result[0]
    
    def update_entrada(self, id_entrada: int, id_banco: int = None, nome_entrada: str = None, tipo_entrada: str = None, valor_entrada: float = None, dia_entrada: int = None) -> bool:
        """Atualiza dados de uma entrada."""
        updates = []
        params = []
        
        if id_banco is not None:
            updates.append('"ID_BANCO" = %s')
            params.append(id_banco)
        if nome_entrada is not None:
            updates.append('"NOME_ENTRADA" = %s')
            params.append(nome_entrada)
        if tipo_entrada is not None:
            updates.append('"TIPO_ENTRADA" = %s')
            params.append(tipo_entrada)
        if valor_entrada is not None:
            updates.append('"VALOR_ENTRADA" = %s')
            params.append(valor_entrada)
        if dia_entrada is not None:
            updates.append('"DIA_ENTRADA" = %s')
            params.append(dia_entrada)
        
        if not updates:
            return False
        
        params.append(id_entrada)
        query = f'UPDATE "ENTRADAS" SET {", ".join(updates)} WHERE "ID_ENTRADA" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_entrada(self, id_entrada: int) -> bool:
        """Deleta uma entrada."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "ENTRADAS" WHERE "ID_ENTRADA" = %s', (id_entrada,))
                return cur.rowcount > 0

    # ==================== SAÍDAS FREQUENTES ====================
    
    def get_all_saidas_frequentes(self) -> List[Dict[str, Any]]:
        """Retorna todas as saídas frequentes."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "SAIDAS_FREQUENTES"')
                return cur.fetchall()
    
    def get_saida_frequente_by_id(self, id_saida: int) -> Optional[Dict[str, Any]]:
        """Retorna uma saída frequente específica por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "SAIDAS_FREQUENTES" WHERE "ID_SAIDA_FREQUENTE" = %s', (id_saida,))
                return cur.fetchone()
    
    def insert_saida_frequente(self, nome_saida: str, tipo_saida: str, valor_saida: float, dia_saida: int) -> int:
        """Insere uma nova saída frequente."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "SAIDAS_FREQUENTES" ("NOME_SAIDA", "TIPO_SAIDA", "VALOR_SAIDA", "DIA_SAIDA") VALUES (%s, %s, %s, %s) RETURNING "ID_SAIDA_FREQUENTE"',
                    (nome_saida, tipo_saida, valor_saida, dia_saida)
                )
                result = cur.fetchone()
                return result['ID_SAIDA_FREQUENTE'] if isinstance(result, dict) else result[0]
    
    def update_saida_frequente(self, id_saida: int, nome_saida: str = None, tipo_saida: str = None, valor_saida: float = None, dia_saida: int = None) -> bool:
        """Atualiza dados de uma saída frequente."""
        updates = []
        params = []
        
        if nome_saida is not None:
            updates.append('"NOME_SAIDA" = %s')
            params.append(nome_saida)
        if tipo_saida is not None:
            updates.append('"TIPO_SAIDA" = %s')
            params.append(tipo_saida)
        if valor_saida is not None:
            updates.append('"VALOR_SAIDA" = %s')
            params.append(valor_saida)
        if dia_saida is not None:
            updates.append('"DIA_SAIDA" = %s')
            params.append(dia_saida)
        
        if not updates:
            return False
        
        params.append(id_saida)
        query = f'UPDATE "SAIDAS_FREQUENTES" SET {", ".join(updates)} WHERE "ID_SAIDA_FREQUENTE" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_saida_frequente(self, id_saida: int) -> bool:
        """Deleta uma saída frequente."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "SAIDAS_FREQUENTES" WHERE "ID_SAIDA_FREQUENTE" = %s', (id_saida,))
                return cur.rowcount > 0

    # ==================== CATEGORIAS DE COMPRAS ====================
    
    def get_all_categorias(self) -> List[Dict[str, Any]]:
        """Retorna todas as categorias de compras."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "CATEGORIAS_DE_COMPRAS"')
                return cur.fetchall()
    
    def get_categoria_by_id(self, id_categoria: int) -> Optional[Dict[str, Any]]:
        """Retorna uma categoria específica por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "CATEGORIAS_DE_COMPRAS" WHERE "ID_CATEGORIA" = %s', (id_categoria,))
                return cur.fetchone()
    
    def insert_categoria(self, nome_categoria: str) -> int:
        """Insere uma nova categoria."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "CATEGORIAS_DE_COMPRAS" ("NOME_CATEGORIA") VALUES (%s) RETURNING "ID_CATEGORIA"',
                    (nome_categoria,)
                )
                result = cur.fetchone()
                return result['ID_CATEGORIA'] if isinstance(result, dict) else result[0]
    
    def update_categoria(self, id_categoria: int, nome_categoria: str) -> bool:
        """Atualiza dados de uma categoria."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'UPDATE "CATEGORIAS_DE_COMPRAS" SET "NOME_CATEGORIA" = %s WHERE "ID_CATEGORIA" = %s',
                    (nome_categoria, id_categoria)
                )
                return cur.rowcount > 0
    
    def delete_categoria(self, id_categoria: int) -> bool:
        """Deleta uma categoria."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "CATEGORIAS_DE_COMPRAS" WHERE "ID_CATEGORIA" = %s', (id_categoria,))
                return cur.rowcount > 0

    # ==================== COMPRAS CARTÕES DE CRÉDITO ====================
    
    def get_all_compras_cartao(self) -> List[Dict[str, Any]]:
        """Retorna todas as compras de cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "COMPRAS_CARTOES_DE_CREDITO"')
                return cur.fetchall()
    
    def get_compra_cartao_by_id(self, id_compra: int) -> Optional[Dict[str, Any]]:
        """Retorna uma compra específica por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "COMPRAS_CARTOES_DE_CREDITO" WHERE "ID_COMPRA_CARTAO_CREDITO" = %s', (id_compra,))
                return cur.fetchone()
    
    def get_compras_by_cartao(self, id_cartao: int) -> List[Dict[str, Any]]:
        """Retorna todas as compras de um cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "COMPRAS_CARTOES_DE_CREDITO" WHERE "ID_CARTAO" = %s', (id_cartao,))
                return cur.fetchall()
    
    def get_compras_by_categoria(self, id_categoria: int) -> List[Dict[str, Any]]:
        """Retorna todas as compras de uma categoria."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "COMPRAS_CARTOES_DE_CREDITO" WHERE "ID_CATEGORIA" = %s', (id_categoria,))
                return cur.fetchall()
    
    def insert_compra_cartao(self, id_cartao: int, id_banco: int, data_compra: date, estabelecimento: str, 
                             parcelas: str, id_categoria: int, valor_compra: float, observacoes: str = None) -> int:
        """Insere uma nova compra de cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "COMPRAS_CARTOES_DE_CREDITO" ("ID_CARTAO", "ID_BANCO", "DATA_COMPRA", "ESTABELECIMENTO", "PARCELAS", "ID_CATEGORIA", "VALOR_COMPRA", "OBSERVACOES") VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "ID_COMPRA_CARTAO_CREDITO"',
                    (id_cartao, id_banco, data_compra, estabelecimento, parcelas, id_categoria, valor_compra, observacoes)
                )
                result = cur.fetchone()
                return result['ID_COMPRA_CARTAO_CREDITO'] if isinstance(result, dict) else result[0]
    
    def update_compra_cartao(self, id_compra: int, id_cartao: int = None, id_banco: int = None, data_compra: date = None, 
                            estabelecimento: str = None, parcelas: str = None, id_categoria: int = None, 
                            valor_compra: float = None, observacoes: str = None) -> bool:
        """Atualiza dados de uma compra de cartão."""
        updates = []
        params = []
        
        if id_cartao is not None:
            updates.append('"ID_CARTAO" = %s')
            params.append(id_cartao)
        if id_banco is not None:
            updates.append('"ID_BANCO" = %s')
            params.append(id_banco)
        if data_compra is not None:
            updates.append('"DATA_COMPRA" = %s')
            params.append(data_compra)
        if estabelecimento is not None:
            updates.append('"ESTABELECIMENTO" = %s')
            params.append(estabelecimento)
        if parcelas is not None:
            updates.append('"PARCELAS" = %s')
            params.append(parcelas)
        if id_categoria is not None:
            updates.append('"ID_CATEGORIA" = %s')
            params.append(id_categoria)
        if valor_compra is not None:
            updates.append('"VALOR_COMPRA" = %s')
            params.append(valor_compra)
        if observacoes is not None:
            updates.append('"OBSERVACOES" = %s')
            params.append(observacoes)
        
        if not updates:
            return False
        
        params.append(id_compra)
        query = f'UPDATE "COMPRAS_CARTOES_DE_CREDITO" SET {", ".join(updates)} WHERE "ID_COMPRA_CARTAO_CREDITO" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_compra_cartao(self, id_compra: int) -> bool:
        """Deleta uma compra de cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "COMPRAS_CARTOES_DE_CREDITO" WHERE "ID_COMPRA_CARTAO_CREDITO" = %s', (id_compra,))
                return cur.rowcount > 0

    # ==================== LIMITES DE COMPRAS ====================
    
    def get_all_limites(self) -> List[Dict[str, Any]]:
        """Retorna todos os limites de compras."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "LIMITES_COMPRAS"')
                return cur.fetchall()
    
    def get_limite_by_id(self, id_limite: int) -> Optional[Dict[str, Any]]:
        """Retorna um limite específico por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "LIMITES_COMPRAS" WHERE "ID_LIMITE_COMPRA" = %s', (id_limite,))
                return cur.fetchone()
    
    def get_limite_by_categoria(self, id_categoria: int) -> Optional[Dict[str, Any]]:
        """Retorna o limite de uma categoria específica."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "LIMITES_COMPRAS" WHERE "ID_CATEGORIA" = %s', (id_categoria,))
                return cur.fetchone()
    
    def insert_limite(self, id_categoria: int, limite_categoria: float) -> int:
        """Insere um novo limite de compra."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "LIMITES_COMPRAS" ("ID_CATEGORIA", "LIMITE_CATEGORIA") VALUES (%s, %s) RETURNING "ID_LIMITE_COMPRA"',
                    (id_categoria, limite_categoria)
                )
                result = cur.fetchone()
                return result['ID_LIMITE_COMPRA'] if isinstance(result, dict) else result[0]
    
    def update_limite(self, id_limite: int, id_categoria: int = None, limite_categoria: float = None) -> bool:
        """Atualiza dados de um limite."""
        updates = []
        params = []
        
        if id_categoria is not None:
            updates.append('"ID_CATEGORIA" = %s')
            params.append(id_categoria)
        if limite_categoria is not None:
            updates.append('"LIMITE_CATEGORIA" = %s')
            params.append(limite_categoria)
        
        if not updates:
            return False
        
        params.append(id_limite)
        query = f'UPDATE "LIMITES_COMPRAS" SET {", ".join(updates)} WHERE "ID_LIMITE_COMPRA" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_limite(self, id_limite: int) -> bool:
        """Deleta um limite."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "LIMITES_COMPRAS" WHERE "ID_LIMITE_COMPRA" = %s', (id_limite,))
                return cur.rowcount > 0

    # ==================== FATURAS CARTÕES DE CRÉDITO ====================
    
    def get_all_faturas(self) -> List[Dict[str, Any]]:
        """Retorna todas as faturas."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "FATURAS_CARTOES_DE_CREDITO"')
                return cur.fetchall()
    
    def get_fatura_by_id(self, id_fatura: int) -> Optional[Dict[str, Any]]:
        """Retorna uma fatura específica por ID."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "FATURAS_CARTOES_DE_CREDITO" WHERE "ID_FATURA_CARTAO_CREDITO" = %s', (id_fatura,))
                return cur.fetchone()
    
    def get_faturas_by_cartao(self, id_cartao: int) -> List[Dict[str, Any]]:
        """Retorna todas as faturas de um cartão."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "FATURAS_CARTOES_DE_CREDITO" WHERE "ID_CARTAO" = %s', (id_cartao,))
                return cur.fetchall()
    
    def get_faturas_by_mes_ano(self, mes: int, ano: int) -> List[Dict[str, Any]]:
        """Retorna todas as faturas de um mês e ano específicos."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT * FROM "FATURAS_CARTOES_DE_CREDITO" WHERE "MES_FATURA" = %s AND "ANO_FATURA" = %s',
                    (mes, ano)
                )
                return cur.fetchall()
    
    def get_faturas_nao_pagas(self) -> List[Dict[str, Any]]:
        """Retorna todas as faturas não pagas."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "FATURAS_CARTOES_DE_CREDITO" WHERE "PAGA" = false')
                return cur.fetchall()
    
    def insert_fatura(self, id_cartao: int, id_banco: int, mes_fatura: int, ano_fatura: int, 
                     valor_fatura: float, paga: bool = False) -> int:
        """Insere uma nova fatura."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "FATURAS_CARTOES_DE_CREDITO" ("ID_CARTAO", "ID_BANCO", "MES_FATURA", "ANO_FATURA", "VALOR_FATURA", "PAGA") VALUES (%s, %s, %s, %s, %s, %s) RETURNING "ID_FATURA_CARTAO_CREDITO"',
                    (id_cartao, id_banco, mes_fatura, ano_fatura, valor_fatura, paga)
                )
                result = cur.fetchone()
                return result['ID_FATURA_CARTAO_CREDITO'] if isinstance(result, dict) else result[0]
    
    def update_fatura(self, id_fatura: int, id_cartao: int = None, id_banco: int = None, mes_fatura: int = None, 
                     ano_fatura: int = None, valor_fatura: float = None, paga: bool = None) -> bool:
        """Atualiza dados de uma fatura."""
        updates = []
        params = []
        
        if id_cartao is not None:
            updates.append('"ID_CARTAO" = %s')
            params.append(id_cartao)
        if id_banco is not None:
            updates.append('"ID_BANCO" = %s')
            params.append(id_banco)
        if mes_fatura is not None:
            updates.append('"MES_FATURA" = %s')
            params.append(mes_fatura)
        if ano_fatura is not None:
            updates.append('"ANO_FATURA" = %s')
            params.append(ano_fatura)
        if valor_fatura is not None:
            updates.append('"VALOR_FATURA" = %s')
            params.append(valor_fatura)
        if paga is not None:
            updates.append('"PAGA" = %s')
            params.append(paga)
        
        if not updates:
            return False
        
        params.append(id_fatura)
        query = f'UPDATE "FATURAS_CARTOES_DE_CREDITO" SET {", ".join(updates)} WHERE "ID_FATURA_CARTAO_CREDITO" = %s'
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount > 0
    
    def delete_fatura(self, id_fatura: int) -> bool:
        """Deleta uma fatura."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "FATURAS_CARTOES_DE_CREDITO" WHERE "ID_FATURA_CARTAO_CREDITO" = %s', (id_fatura,))
                return cur.rowcount > 0
