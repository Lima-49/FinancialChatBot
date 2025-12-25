class FaturasCartoesDeCreditoModel:
    def __init__(self, id_fatura_cartao_credito=None, id_cartao=None, id_banco=None, 
                 mes_fatura=None, ano_fatura=None, valor_fatura=None, paga=None):
        self.id_fatura_cartao_credito = id_fatura_cartao_credito
        self.id_cartao = id_cartao
        self.id_banco = id_banco
        self.mes_fatura = mes_fatura
        self.ano_fatura = ano_fatura
        self.valor_fatura = valor_fatura
        self.paga = paga

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_fatura_cartao_credito=data.get('id_fatura_cartao_credito'),
            id_cartao=data.get('id_cartao'),
            id_banco=data.get('id_banco'),
            mes_fatura=data.get('mes_fatura'),
            ano_fatura=data.get('ano_fatura'),
            valor_fatura=data.get('valor_fatura'),
            paga=data.get('paga'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_fatura_cartao_credito": self.id_fatura_cartao_credito,
            "id_cartao": self.id_cartao,
            "id_banco": self.id_banco,
            "mes_fatura": self.mes_fatura,
            "ano_fatura": self.ano_fatura,
            "valor_fatura": self.valor_fatura,
            "paga": self.paga,
        }