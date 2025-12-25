from enum import Enum

class CardType(Enum):
    DEBITO = 0
    CREDITO = 1
    CREDITO_E_DEBITO = 2
    
class CartoesCreditoModel:
    """Modelo de dados para cartões de crédito."""    
    def __init__(self, nome_cartao=None, tipo_cartao=None, dia_vencimento=None, id_cartao=None, id_banco=None):
        self.id_cartao = id_cartao
        self.id_banco = id_banco
        self.nome_cartao = nome_cartao
        self.tipo_cartao = tipo_cartao
        self.dia_vencimento = dia_vencimento

    @classmethod
    def from_dict(cls, data):
        tipo_cartao_value = data.get('tipo_cartao')
        return cls(
            id_cartao=data.get('id_cartao'),
            id_banco=data.get('id_banco'),
            nome_cartao=data.get('nome_cartao'),
            tipo_cartao=CardType(tipo_cartao_value) if tipo_cartao_value is not None else CardType.CREDITO,
            dia_vencimento=data.get('dia_vencimento'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_cartao": self.id_cartao,
            "id_banco": self.id_banco,
            "nome_cartao": self.nome_cartao,
            "tipo_cartao": self.tipo_cartao.value if self.tipo_cartao else None,
            "dia_vencimento": self.dia_vencimento,
        }