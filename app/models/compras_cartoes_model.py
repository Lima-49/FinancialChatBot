class ComprasCartoesModel:
    def __init__(self, data_compra=None, estabelecimento=None, parcelas=None, id_categoria=None, valor_compra=None, observacoes=None, id_compra_cartao=None, id_cartao=None, id_banco=None):
        self.id_compra_cartao = id_compra_cartao
        self.id_cartao = id_cartao
        self.id_banco = id_banco
        self.data_compra = data_compra
        self.estabelecimento = estabelecimento
        self.parcelas = parcelas
        self.id_categoria = id_categoria
        self.valor_compra = valor_compra
        self.observacoes = observacoes

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_compra_cartao=data.get('id_compra_cartao'),
            id_cartao=data.get('id_cartao'),
            id_banco=data.get('id_banco'),
            data_compra=data.get('data_compra'),
            estabelecimento=data.get('estabelecimento'),
            parcelas=data.get('parcelas'),
            id_categoria=data.get('id_categoria'),
            valor_compra=data.get('valor_compra'),
            observacoes=data.get('observacoes'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_compra_cartao": self.id_compra_cartao,
            "id_cartao": self.id_cartao,
            "id_banco": self.id_banco,
            "data_compra": self.data_compra,
            "estabelecimento": self.estabelecimento,
            "parcelas": self.parcelas,
            "id_categoria": self.id_categoria,
            "valor_compra": self.valor_compra,
            "observacoes": self.observacoes,
        }