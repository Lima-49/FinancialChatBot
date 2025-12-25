class SaidasFrequentesModel:
    def __init__(self, nome_saida=None, tipo_saida=None, valor_saida=None, dia_saida=None, id_saida_frequente=None, id_banco=None):
        self.id_saida_frequente = id_saida_frequente
        self.id_banco = id_banco
        self.nome_saida = nome_saida
        self.tipo_saida = tipo_saida
        self.valor_saida = valor_saida
        self.dia_saida = dia_saida

    @classmethod
    def from_dict(cls, data):
        """Converte dicionário do banco de dados em objeto do modelo."""
        return cls(
            id_saida_frequente=data.get('id_saida_frequente'),
            id_banco=data.get('id_banco'),
            nome_saida=data.get('nome_saida'),
            tipo_saida=data.get('tipo_saida'),
            valor_saida=data.get('valor_saida'),
            dia_saida=data.get('dia_saida'),
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_saida_frequente": self.id_saida_frequente,
            "id_banco": self.id_banco, 
            "nome_saida": self.nome_saida,
            "tipo_saida": self.tipo_saida,
            "valor_saida": self.valor_saida,
            "dia_saida": self.dia_saida,
        }