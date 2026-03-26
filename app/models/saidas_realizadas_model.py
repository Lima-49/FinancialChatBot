class SaidasRealizadasModel:
    def __init__(
        self,
        id_banco=None,
        data_saida=None,
        valor=None,
        id_categoria=None,
        id_saida=None,
        descricao=None,
        created_at=None,
    ):
        self.id_saida = id_saida
        self.id_categoria = id_categoria
        self.id_banco = id_banco
        self.data_saida = data_saida
        self.valor = valor
        self.descricao = descricao
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_saida=data.get("id_saida"),
            id_categoria=data.get("id_categoria"),
            id_banco=data.get("id_banco"),
            data_saida=data.get("data_saida"),
            valor=data.get("valor"),
            descricao=data.get("descricao"),
            created_at=data.get("created_at"),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_saida": self.id_saida,
            "id_categoria": self.id_categoria,
            "id_banco": self.id_banco,
            "data_saida": self.data_saida,
            "valor": self.valor,
            "descricao": self.descricao,
            "created_at": self.created_at,
        }
