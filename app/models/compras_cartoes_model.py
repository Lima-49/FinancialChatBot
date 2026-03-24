class ComprasCartoesModel:
    def __init__(self, data_compra=None, estabelecimento=None, id_categoria=None, valor_compra=None, observacoes=None, id_compra_cartao=None, id_cartao=None, id_banco=None, numero_parcelas=1, parcela_atual=1, created_at=None):
        self.id_compra_cartao = id_compra_cartao
        self.id_cartao = id_cartao
        self.id_banco = id_banco
        self.data_compra = data_compra
        self.estabelecimento = estabelecimento
        self.numero_parcelas = numero_parcelas
        self.parcela_atual = parcela_atual
        self.id_categoria = id_categoria
        self.valor_compra = valor_compra
        self.observacoes = observacoes
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_compra_cartao=data.get('id_compra_cartao'),
            id_cartao=data.get('id_cartao'),
            id_banco=data.get('id_banco'),
            data_compra=data.get('data_compra'),
            estabelecimento=data.get('estabelecimento'),
            numero_parcelas=data.get('numero_parcelas', data.get('parcelas', 1)),
            parcela_atual=data.get('parcela_atual', 1),
            id_categoria=data.get('id_categoria'),
            valor_compra=data.get('valor_compra'),
            observacoes=data.get('observacoes'),
            created_at=data.get('created_at') or data.get('created_at')
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_compra_cartao": self.id_compra_cartao,
            "id_cartao": self.id_cartao,
            "id_banco": self.id_banco,
            "data_compra": self.data_compra,
            "estabelecimento": self.estabelecimento,
            "numero_parcelas": self.numero_parcelas,
            "parcela_atual": self.parcela_atual,
            "id_categoria": self.id_categoria,
            "valor_compra": self.valor_compra,
            "observacoes": self.observacoes,
            "created_at": self.created_at,
        }