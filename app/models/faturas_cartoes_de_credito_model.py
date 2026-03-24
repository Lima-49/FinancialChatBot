class FaturasCartoesDeCreditoModel:
    def __init__(self, id_fatura_cartao_credito=None, id_cartao=None,
                 valor_fatura=None, paga=None, data_fatura=None, data_vencimento=None):
        self.id_fatura_cartao_credito = id_fatura_cartao_credito
        self.id_cartao = id_cartao
        self.valor_fatura = valor_fatura
        self.paga = paga
        self.data_fatura = data_fatura
        self.data_vencimento = data_vencimento

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_fatura_cartao_credito=data.get('id_fatura_cartao_credito'),
            id_cartao=data.get('id_cartao'),
            valor_fatura=data.get('valor_fatura'),
            paga=data.get('paga'),
            data_fatura=data.get('data_fatura'),
            data_vencimento=data.get('data_vencimento')
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_fatura_cartao_credito": self.id_fatura_cartao_credito,
            "id_cartao": self.id_cartao,
            "valor_fatura": self.valor_fatura,
            "paga": self.paga,
            "data_fatura": self.data_fatura,
            "data_vencimento": self.data_vencimento,
        }