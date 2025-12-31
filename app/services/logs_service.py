from typing import Optional, List
from datetime import datetime, timedelta
import traceback as tb
import inspect
from app.models.logs_model import LogModel, LogCreateModel
from app.services.postgres_service import PostgresService


class LogService:
    """Serviço para gerenciar logs no Supabase"""
    
    def __init__(self):
        self.postgres_service = PostgresService()
        self.table_name = "logs"
    
    def _get_caller_info(self):
        """Obtém informações sobre quem chamou o log"""
        try:
            # Pega o frame 3 níveis acima (0=aqui, 1=método de log, 2=método público)
            frame = inspect.currentframe()
            if frame:
                caller_frame = frame.f_back.f_back.f_back
                if caller_frame:
                    return {
                        'modulo': caller_frame.f_globals.get('__name__', 'unknown'),
                        'funcao': caller_frame.f_code.co_name,
                        'linha': caller_frame.f_lineno
                    }
        except Exception:
            pass
        return {'modulo': None, 'funcao': None, 'linha': None}
    
    def _salvar_log(
        self,
        nivel: str,
        mensagem: str,
        include_traceback: bool = False,
        modulo: Optional[str] = None,
        funcao: Optional[str] = None,
        linha: Optional[int] = None
    ):
        """Método interno para salvar log no banco"""
        try:
            # Se não fornecidos, buscar info do chamador
            if modulo is None or funcao is None or linha is None:
                caller_info = self._get_caller_info()
                modulo = modulo or caller_info['modulo']
                funcao = funcao or caller_info['funcao']
                linha = linha or caller_info['linha']
            
            traceback_str = None
            if include_traceback:
                traceback_str = tb.format_exc()
            
            log_data = LogCreateModel(
                nivel=nivel,
                mensagem=mensagem,
                modulo=modulo,
                funcao=funcao,
                linha=linha,
                traceback=traceback_str
            )
            
            with self.postgres_service.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    INSERT INTO {self.table_name} 
                    (nivel, mensagem, modulo, funcao, linha, traceback, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        log_data.nivel,
                        log_data.mensagem,
                        log_data.modulo,
                        log_data.funcao,
                        log_data.linha,
                        log_data.traceback,
                        datetime.now()
                    )
                )
                result = cursor.fetchone()
                return result['id'] if result else None
        except Exception as e:
            # Se falhar ao salvar no banco, não gerar erro para não quebrar a aplicação
            print(f"Erro ao salvar log no banco: {e}")
            return None
    
    def error(self, mensagem: str, exc_info: bool = False):
        """Registra um log de erro"""
        return self._salvar_log("ERROR", mensagem, include_traceback=exc_info)
    
    def info(self, mensagem: str):
        """Registra um log de informação"""
        return self._salvar_log("INFO", mensagem)
    
    def warning(self, mensagem: str):
        """Registra um log de aviso"""
        return self._salvar_log("WARNING", mensagem)
    
    def debug(self, mensagem: str):
        """Registra um log de debug"""
        return self._salvar_log("DEBUG", mensagem)
    
    def critical(self, mensagem: str, exc_info: bool = False):
        """Registra um log crítico"""
        return self._salvar_log("CRITICAL", mensagem, include_traceback=exc_info)

# Instância global do serviço de log
log_service = LogService()
