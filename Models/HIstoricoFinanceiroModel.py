class HistoricoFinanceiroModel:
    def __init__(self, date=None, category=None, description=None, bank=None, method=None, value=None):
        self.date = date
        self.category = category
        self.description = description
        self.bank = bank
        self.method = method
        self.value = value

    @classmethod
    def from_dict(cls, data):
        return cls(
            date = data.get("Data"),
            category = data.get("Categoria"),
            description = data.get("Descricao"),
            bank = data.get("Banco"),
            metodo = data.get("Metodo"),
            value = data.get("Valor")
        )