from transacao import Transacao



class Conta:
    def __init__(self, id_conta, titular, saldo_inicial=0.0):
        self.id = id_conta
        self.titular = titular
        self.saldo_inicial = saldo_inicial
        self.saldo = saldo_inicial
        self.transacoes = []
        self.nova_importacao = False  # Flag para novas transações

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
        self.atualizar_saldo()

    def atualizar_saldo(self):
        self.saldo = self.saldo_inicial
        self.saldo = round(self.saldo, 2)

    def calcular_saldo_atual(self):
        saldo = self.saldo_inicial
        for transacao in self.transacoes:
            saldo += transacao.valor
        return round(saldo, 2)

    def obter_saldo(self):
        return self.saldo

    def obter_extrato(self):
        return self.transacoes

    def __str__(self):
        return f"Conta de {self.titular}, Saldo atual: {self.saldo:.2f}"

class ContaCorrente(Conta):
    def __init__(self, id_conta, titular, saldo_inicial=0.0):
        super().__init__(id_conta, titular, saldo_inicial)

class ContaPoupanca(Conta):
    def __init__(self, id_conta, titular, taxa_juros, periodo_juros, saldo_inicial=0.0):
        super().__init__(id_conta, titular, saldo_inicial)
        self.taxa_juros = taxa_juros
        self.periodo_juros = periodo_juros  # 'Mensal' ou 'Anual'

class CartaoCredito(Conta):
    def __init__(self, id_conta, titular, limite_credito, saldo_inicial=0.0):
        super().__init__(id_conta, titular, saldo_inicial)
        self.limite_credito = limite_credito
        # Métodos específicos para Cartão de Crédito

class Credito(Conta):
    def __init__(self, id_conta, titular, tipo_credito, taxa_juros, saldo_inicial):
        super

    def to_dict(self):
        """Converte a conta e suas transações em um dicionário."""
        return {
            'id': self.id,
            'titular': self.titular,
            'saldo': self.saldo,
            'transacoes': [transacao.to_dict() for transacao in self.transacoes]
        }

    @staticmethod
    def from_dict(dados):
        """Cria uma instância de Conta a partir de um dicionário."""
        conta = Conta(dados['id'], dados['titular'], dados['saldo'])
        conta.transacoes = [Transacao.from_dict(t) for t in dados['transacoes']]
        return conta
