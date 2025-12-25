class LimitesDeComprasModel:
    def __init__(self, id_limite_compra=None, id_categoria=None, limite_categoria=None):
        self.id_limite_compra = id_limite_compra
        self.id_categoria = id_categoria
        self.limite_categoria = limite_categoria

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo.."""
        return cls(
            id_limite_compra=data.get('id_limite_compra'),
            id_categoria=data.get('id_categoria'),
            limite_categoria=data.get('limite_categoria'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_limite_compra": self.id_limite_compra,
            "id_categoria": self.id_categoria,
            "limite_categoria": self.limite_categoria,
        }