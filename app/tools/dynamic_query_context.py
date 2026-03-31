from typing import Dict, Any

class DynamicQueryContext:
    """Classe para gerenciar o contexto das queries dinâmicas."""

    def __init__(self):
        self.phone_number = ""
        self.pending_queries: Dict[str, Dict[str, Any]] = {}

    def set_phone_number(self, phone: str):
        self.phone_number = phone

    def get_phone_number(self) -> str:
        return self.phone_number or "default"

    def get_pending(self, phone: str) -> Dict[str, Any]:
        return self.pending_queries.get(phone, {})

    def set_pending(self, phone: str, data: Dict[str, Any]):
        self.pending_queries[phone] = data

    def pop_pending(self, phone: str) -> Dict[str, Any]:
        return self.pending_queries.pop(phone, {})