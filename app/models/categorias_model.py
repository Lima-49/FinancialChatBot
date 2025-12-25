class CategoriasModel:
    def __init__(self, id_categoria=None, nome_categoria=None):
        self.id_categoria = id_categoria
        self.nome_categoria = nome_categoria

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_categoria=data.get('id_categoria'),
            nome_categoria=data.get('nome_categoria'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_categoria": self.id_categoria,
            "nome_categoria": self.nome_categoria,
        }