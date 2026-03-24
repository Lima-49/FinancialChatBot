class EntradasRealizadasModel:
    def __init__(self, data_entrada=None, valor=None, descricao=None, id_categoria=None, id_entrada=None, id_banco=None, created_at=None):
        self.id_entrada = id_entrada
        self.id_banco = id_banco
        self.id_categoria = id_categoria
        self.data_entrada = data_entrada
        self.valor = valor
        self.descricao = descricao
        self.created_at = created_at


    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_entrada=data.get('id_entrada'),
            id_banco=data.get('id_banco'),
            data_entrada=data.get('data_entrada'),
            valor=data.get('valor'),
            descricao=data.get('descricao'),
            id_categoria=data.get('id_categoria'),
            created_at=data.get('created_at'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_entrada": self.id_entrada,
            "id_banco": self.id_banco,
            "data_entrada": self.data_entrada,
            "valor": self.valor,
            "descricao": self.descricao,
            "id_categoria": self.id_categoria,
            "created_at": self.created_at,
        }