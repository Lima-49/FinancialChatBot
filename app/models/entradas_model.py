class EntradasModel:
    def __init__(self, nome_entrada=None, tipo_entrada=None, valor_entrada=None, dia_entrada=None, id_entrada=None, id_banco=None):
        self.id_entrada = id_entrada
        self.id_banco = id_banco
        self.nome_entrada = nome_entrada
        self.tipo_entrada = tipo_entrada
        self.valor_entrada = valor_entrada
        self.dia_entrada = dia_entrada

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_entrada=data.get('id_entrada'),
            id_banco=data.get('id_banco'),
            nome_entrada=data.get('nome_entrada'),
            tipo_entrada=data.get('tipo_entrada'),
            valor_entrada=data.get('valor_entrada'),
            dia_entrada=data.get('dia_entrada'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_entrada": self.id_entrada,
            "id_banco": self.id_banco, 
            "nome_entrada": self.nome_entrada,
            "tipo_entrada": self.tipo_entrada,
            "valor_entrada": self.valor_entrada,
            "dia_entrada": self.dia_entrada,
        }