class BancosModel:
    """Modelo de dados para bancos."""
    def __init__(self, nome_banco=None,
                    valor_em_conta=None, valor_investido=None, id_banco=None):
        self.id_banco = id_banco
        self.nome_banco = nome_banco
        self.valor_em_conta = valor_em_conta
        self.valor_investido = valor_investido

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_banco=data.get('id_banco'),
            nome_banco=data.get('nome_banco'),
            valor_em_conta=data.get('valor_em_conta'),
            valor_investido=data.get('valor_investido')
        )

    def to_dict(self):
        """Converte objeto do modelo em dicionário."""
        return {
            "id_banco": self.id_banco,
            "nome_banco": self.nome_banco,
            "valor_em_conta": self.valor_em_conta,
            "valor_investido": self.valor_investido
        }
