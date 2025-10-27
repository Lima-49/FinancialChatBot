from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2 import sql
import logging
from contextlib import contextmanager
import os
from dataclasses import dataclass
from app.models.config_account_model import ConfigAccountModelRequest, ConfigAccountModelResponse

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

    def create_account_table(self) -> ConfigAccountModelResponse:
        """Cria a tabela de contas bancárias se não existir"""
        create_bank_accounts_table = """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            account_id SERIAL PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL,
            account_balance DECIMAL(15,2) DEFAULT 0.0
        );
        """
        
        create_trigger = """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        
        DROP TRIGGER IF EXISTS update_bank_accounts_updated_at ON bank_accounts;
        CREATE TRIGGER update_bank_accounts_updated_at 
            BEFORE UPDATE ON bank_accounts 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_bank_accounts_table)
                    cursor.execute(create_trigger)
                    logger.info("Tabelas criadas com sucesso")
                    return ConfigAccountModelResponse(
                        success=True,
                        message="Tabelas criadas com sucesso"
                    )
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            return ConfigAccountModelResponse(
                success=False,
                message=f"Erro ao criar tabelas: {str(e)}"
            )
    
   
    def insert_bank_account(self, request: ConfigAccountModelRequest) -> ConfigAccountModelResponse:
            """
            Insere uma nova conta bancária usando o modelo ConfigAccountModelRequest
            Cria a tabela automaticamente se não existir
            """
            insert_query = """
            INSERT INTO bank_accounts (account_name, account_balance)
            VALUES (%(account_name)s, %(account_balance)s) 
            RETURNING account_id;
            """
            
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(insert_query, {
                            'account_name': request.account_name,
                            'account_balance': request.account_balance
                        })
                        account_id = cursor.fetchone()['account_id']
                        logger.info(f"Conta bancária inserida com ID: {account_id}")
                        return ConfigAccountModelResponse(
                            success=True,
                            message=f"Conta '{request.account_name}' criada com sucesso. ID: {account_id}"
                        )
            except psycopg2.errors.UndefinedTable:
                # Tabela não existe, criar e tentar novamente
                logger.info("Tabela não existe. Criando tabela e tentando novamente...")
                create_response = self.create_account_table()
                if not create_response.success:
                    return create_response
                
                # Tentar inserir novamente após criar a tabela
                try:
                    with self.get_connection() as conn:
                        with conn.cursor() as cursor:
                            cursor.execute(insert_query, {
                                'account_name': request.account_name,
                                'account_balance': request.account_balance
                            })
                            account_id = cursor.fetchone()['account_id']
                            logger.info(f"Conta bancária inserida com ID: {account_id} (após criar tabela)")
                            return ConfigAccountModelResponse(
                                success=True,
                                message=f"Tabela criada e conta '{request.account_name}' inserida com sucesso. ID: {account_id}"
                            )
                except Exception as e:
                    logger.error(f"Erro ao inserir conta após criar tabela: {e}")
                    return ConfigAccountModelResponse(
                        success=False,
                        message=f"Erro ao inserir conta após criar tabela: {str(e)}"
                    )
            except Exception as e:
                logger.error(f"Erro ao inserir conta bancária: {e}")
                return ConfigAccountModelResponse(
                    success=False,
                    message=f"Erro ao inserir conta: {str(e)}"
                )
        
    def update_bank_account(self, request: ConfigAccountModelRequest) -> ConfigAccountModelResponse:
        """Atualiza uma conta bancária usando ConfigAccountModelRequest"""
        update_query = """
        UPDATE bank_accounts 
        SET account_name = %(account_name)s, account_balance = %(account_balance)s
        WHERE id = %(account_id)s
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(update_query, {
                        'account_id': request.account_id,
                        'account_name': request.account_name,
                        'account_balance': request.account_balance
                    })
                    if cursor.rowcount > 0:
                        logger.info(f"Conta {request.account_id} atualizada com sucesso")
                        return ConfigAccountModelResponse(
                            success=True,
                            message=f"Conta '{request.account_name}' atualizada com sucesso"
                        )
                    else:
                        logger.warning(f"Conta {request.account_id} não encontrada para atualização")
                        return ConfigAccountModelResponse(
                            success=False,
                            message=f"Conta com ID {request.account_id} não encontrada"
                        )
        except Exception as e:
            logger.error(f"Erro ao atualizar conta {request.account_id}: {e}")
            return ConfigAccountModelResponse(
                success=False,
                message=f"Erro ao atualizar conta: {str(e)}"
            )
    
    def delete_bank_account(self, account_id: int, soft_delete: bool = True) -> ConfigAccountModelResponse:
        """
        Remove uma conta bancária
        soft_delete=True: apenas marca como inativa
        soft_delete=False: remove permanentemente
        """
        if soft_delete:
            query = "UPDATE bank_accounts SET ativo = FALSE WHERE id = %s"
        else:
            query = "DELETE FROM bank_accounts WHERE id = %s"
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (account_id,))
                    if cursor.rowcount > 0:
                        action = "desativada" if soft_delete else "removida"
                        logger.info(f"Conta {account_id} {action} com sucesso")
                        return ConfigAccountModelResponse(
                            success=True,
                            message=f"Conta {action} com sucesso"
                        )
                    else:
                        logger.warning(f"Conta {account_id} não encontrada")
                        return ConfigAccountModelResponse(
                            success=False,
                            message=f"Conta com ID {account_id} não encontrada"
                        )
        except Exception as e:
            logger.error(f"Erro ao remover conta {account_id}: {e}")
            return ConfigAccountModelResponse(
                success=False,
                message=f"Erro ao remover conta: {str(e)}"
            )
    
    def update_account_balance(self, account_id: int, new_balance: float) -> ConfigAccountModelResponse:
        """Atualiza apenas o saldo de uma conta"""
        query = "UPDATE bank_accounts SET account_balance = %s WHERE id = %s"
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (new_balance, account_id))
                    if cursor.rowcount > 0:
                        logger.info(f"Saldo da conta {account_id} atualizado para {new_balance}")
                        return ConfigAccountModelResponse(
                            success=True,
                            message=f"Saldo atualizado para R$ {new_balance:.2f}"
                        )
                    else:
                        return ConfigAccountModelResponse(
                            success=False,
                            message=f"Conta com ID {account_id} não encontrada"
                        )
        except Exception as e:
            logger.error(f"Erro ao atualizar saldo da conta {account_id}: {e}")
            return ConfigAccountModelResponse(
                success=False,
                message=f"Erro ao atualizar saldo: {str(e)}"
            )
