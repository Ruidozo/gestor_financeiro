from datetime import datetime

class Transacao:
    def __init__(self, data, valor, descricao, categoria):
        self.data = data
        self.valor = valor
        self.descricao = descricao
        self.categoria = categoria


    def get_data(self):
        return self.data
    
    def get_valor(self):
        return self.valor

    def get_categoria(self):
        return self.categoria

    def get_descricao(self):
        return self.descricao

    def set_data(self, data):
        """Atualiza a data da transação."""
        self.data = data

    def set_valor(self, valor):
        """Atualiza o valor da transação."""
        self.valor = round(valor, 2)

    def set_categoria(self, categoria):
        """Atualiza a categoria da transação."""
        self.categoria = categoria

    def set_descricao(self, descricao):
        """Atualiza a descrição da transação."""
        self.descricao = descricao

    def __str__(self):
        """Representação em string da transação."""
        return f"Transação: {self.descricao}, Data: {self.data}, Valor: {self.valor:.2f}, Categoria: {self.categoria}"

    def to_dict(self):
        """Converte a transação em um dicionário."""
        return {
            'data': self.data.strftime("%Y-%m-%d"),  # assumindo que self.data é um objeto datetime
            'valor': self.valor,
            'categoria': self.categoria,
            'categoria': self.categoria,
            'descricao': self.descricao
        }

    @staticmethod
    def from_dict(dados):
        """Cria uma instância de Transacao a partir de um dicionário."""
        data = datetime.strptime(dados['data'], "%Y-%m-%d")  # convertendo a string de volta para datetime
        return Transacao(data, dados['valor'], dados['descricao'],dados['categoria'])
