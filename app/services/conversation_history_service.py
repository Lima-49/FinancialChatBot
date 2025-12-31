from typing import List, Optional
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from app.services.postgres_service import PostgresService
from app.models.historico_de_mensagens_model import ConversationHistory, ConversationMessage
from app.models.message_models import Message
from app.services.logs_service import log_service
import os


class ConversationHistoryService:
    """Serviço para gerenciar histórico de conversas com criptografia"""
    
    def __init__(self):
        self.db = PostgresService()
        self.encryption_key = os.getenv("CONVERSATION_ENCRYPTION_KEY")
        
        if not self.encryption_key:
            raise ValueError("CONVERSATION_ENCRYPTION_KEY não encontrada nas variáveis de ambiente")
        
        # Inicializa o cipher para criptografia/descriptografia
        self.cipher = Fernet(self.encryption_key.encode())
    
    def _encrypt_conteudo_mensagem(self, conteudo_mensagem: str) -> str:
        """Criptografa o conteúdo da mensagem"""
        try:
            encrypted = self.cipher.encrypt(conteudo_mensagem.encode())
            return encrypted.decode()
        except Exception as e:
            log_service.error(f"Erro ao criptografar mensagem: {e}", exc_info=True)
            raise
    
    def _decrypt_conteudo_mensagem(self, encrypted_conteudo_mensagem: str) -> str:
        """Descriptografa o conteúdo da mensagem"""
        try:
            decrypted = self.cipher.decrypt(encrypted_conteudo_mensagem.encode())
            return decrypted.decode()
        except Exception as e:
            log_service.error(f"Erro ao descriptografar mensagem: {e}", exc_info=True)
            raise
    
    def save_message(self, numero_telefone: str, tipo_mensageiro: str, conteudo_mensagem: str) -> bool:
        """
        Salva uma mensagem no histórico (criptografada)
        
        Args:
            numero_telefone: Número do WhatsApp do usuário
            tipo_mensageiro: 'user' ou 'assistant'
            conteudo_mensagem: Conteúdo da mensagem
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            encrypted_conteudo_mensagem = self._encrypt_conteudo_mensagem(conteudo_mensagem)
            
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO historico_de_mensagens 
                    (numero_telefone, tipo_mensageiro, conteudo_mensagem, data_criacao)
                    VALUES (%s, %s, %s, %s)
                """, (numero_telefone, tipo_mensageiro, encrypted_conteudo_mensagem, datetime.now()))
                
            log_service.info(f"Mensagem salva para {numero_telefone}")
            return True
            
        except Exception as e:
            log_service.error(f"Erro ao salvar mensagem: {e}", exc_info=True)
            return False
    
    def get_history(
        self, 
        numero_telefone: str, 
        limit: int = 10,
        hours_back: Optional[int] = 24
    ) -> List[Message]:
        """
        Recupera o histórico de mensagens de um usuário (descriptografadas)
        
        Args:
            numero_telefone: Número do WhatsApp do usuário
            limit: Número máximo de mensagens a retornar
            hours_back: Quantas horas atrás buscar (None = sem limite)
            
        Returns:
            List[Message]: Lista de mensagens no formato do message_models
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                if hours_back:
                    time_filter = datetime.now() - timedelta(hours=hours_back)
                    cursor.execute("""
                        SELECT tipo_mensageiro, conteudo_mensagem, data_criacao
                        FROM historico_de_mensagens
                        WHERE numero_telefone = %s 
                        AND data_criacao >= %s
                        ORDER BY data_criacao ASC
                        LIMIT %s
                    """, (numero_telefone, time_filter, limit))
                else:
                    cursor.execute("""
                        SELECT tipo_mensageiro, conteudo_mensagem, data_criacao
                        FROM historico_de_mensagens
                        WHERE numero_telefone = %s
                        ORDER BY data_criacao DESC
                        LIMIT %s
                    """, (numero_telefone, limit))
                
                rows = cursor.fetchall()
                
                # Descriptografa e converte para o modelo Message
                messages = []
                for row in rows:
                    try:
                        decrypted_conteudo_mensagem = self._decrypt_conteudo_mensagem(row['conteudo_mensagem'])
                        
                        # Ajusta o tipo_mensageiro para o formato esperado pelo sistema
                        tipo_mensageiro = 'user' if row['tipo_mensageiro'] == 'user' else 'bot'
                        
                        messages.append(Message(
                            role=tipo_mensageiro,
                            content=decrypted_conteudo_mensagem
                        ))
                    except Exception as e:
                        log_service.error(f"Erro ao descriptografar mensagem: {e}", exc_info=True)
                        continue
                
                # Se usou DESC, inverte para ordem cronológica
                if not hours_back:
                    messages.reverse()
                
                log_service.info(f"Recuperadas {len(messages)} mensagens para {numero_telefone}")
                return messages
                
        except Exception as e:
            log_service.error(f"Erro ao buscar histórico: {e}", exc_info=True)
            return []
    
    def clear_old_messages(self, days_old: int = 30) -> int:
        """
        Remove mensagens antigas do banco (GDPR compliance)
        
        Args:
            days_old: Idade mínima das mensagens para remoção
            
        Returns:
            int: Número de mensagens removidas
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM historico_de_mensagens
                    WHERE data_criacao < %s
                """, (cutoff_date,))
                
                deleted_count = cursor.rowcount
                
            log_service.info(f"Removidas {deleted_count} mensagens antigas")
            return deleted_count
            
        except Exception as e:
            log_service.error(f"Erro ao limpar mensagens antigas: {e}", exc_info=True)
            return 0
    
    def delete_user_history(self, numero_telefone: str) -> bool:
        """
        Remove todo histórico de um usuário específico
        
        Args:
            numero_telefone: Número do WhatsApp do usuário
            
        Returns:
            bool: True se removeu com sucesso
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM historico_de_mensagens
                    WHERE numero_telefone = %s
                """, (numero_telefone,))
                
            log_service.info(f"Histórico removido para {numero_telefone}")
            return True
            
        except Exception as e:
            log_service.error(f"Erro ao deletar histórico: {e}", exc_info=True)
            return False
