import os
import csv
from transacao import Transacao
from datetime import datetime
from tkinter import messagebox

diretorio_programa = os.path.dirname(os.path.abspath(__file__))

from conta import Conta, ContaCorrente, ContaPoupanca, CartaoCredito, Credito

class GestorFinanceiro:
    def __init__(self):
        self.contas = {}

    def salvar_contas_csv(self, arquivo_contas='contas.csv'):
        with open(arquivo_contas, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID Conta', 'Titular', 'Saldo'])
            if not self.contas:
                print("Nenhuma conta para salvar.")
            for id_conta, conta in self.contas.items():
                writer.writerow([id_conta, conta.titular, conta.obter_saldo()])
        print("Contas salvas no ficheiro.")
    def salvar_transacoes_csv(self, arquivo_transacoes='transacoes.csv'):
        with open(arquivo_transacoes, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID Conta', 'Data', 'Valor', 'Descrição', 'Categoria'])
            for conta in self.contas.values():
                for transacao in conta.transacoes:
                    writer.writerow([conta.id, transacao.get_data(), transacao.get_valor(), transacao.get_descricao(), transacao.get_categoria()])
    def carregar_contas_csv(self, arquivo_contas='contas.csv'):
        try:
            with open(arquivo_contas, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    id_conta = int(row['ID Conta'])  # Convertendo o ID para inteiro
                    titular = row['Titular']
                    saldo = float(row['Saldo'])
                    conta = Conta(id_conta, titular, saldo)
                    self.contas[id_conta] = conta
        except FileNotFoundError:
            print(f"Arquivo {arquivo_contas} não encontrado.")  # Corrigido para 'arquivo_contas'
    def carregar_transacoes_csv(self, arquivo_transacoes='transacoes.csv'):
        try:
            with open(arquivo_transacoes, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    id_conta = int(row['ID Conta'])  # Convertendo o ID da conta para inteiro
                    data = row['Data']
                    valor = float(row['Valor'])
                    categoria = row['Categoria']
                    descricao = row['Descrição']
                    transacao = Transacao(data, valor, categoria, descricao)
                    if id_conta in self.contas:
                        self.contas[id_conta].adicionar_transacao(transacao)

                        # Atualizar o saldo da conta após cada transação
                        self.contas[id_conta].atualizar_saldo()
                    else:
                        print(f"Conta com ID {id_conta} não encontrada. A transação não foi adicionada.")
        except FileNotFoundError:
            print(f"Arquivo {arquivo_transacoes} não encontrado.")
    def gerar_id_conta(self):
        novo_id = len(self.contas) + 1
        while novo_id in self.contas:
            novo_id += 1
        return novo_id
    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise ValueError("O objeto fornecido não é uma conta válida.")
        if conta.id in self.contas:
            raise ValueError(f"Uma conta com o ID {conta.id} já existe.")
        self.contas[conta.id] = conta

        # cria janela de aviso usando o tkinter com butao ok
        messagebox.showinfo("Aviso", "Conta criada com sucesso")

    def remover_conta(self, conta_id_str):
        print("IDs de contas existentes:", self.contas.keys())  # Debugging para listar IDs de contas existentes

        try:
            conta_id = int(conta_id_str)
        except ValueError:
            raise ValueError(f"ID inválido: {conta_id_str} não é um número.")

        print("Tentando remover a conta com ID:", conta_id)  # Debugging para mostrar o ID da conta sendo removido

        if conta_id not in self.contas:
            raise ValueError(f"Não existe conta com o ID {conta_id}.")

        del self.contas[conta_id]
        print(f"Conta removida: ID {conta_id}")

    def obter_resumo_financeiro(self):
        return {conta.id: conta.obter_saldo() for conta in self.contas.values()}
    def encontrar_conta_por_id(self, conta_id):
        return self.contas.get(conta_id, None)
    def listar_transacoes_por_conta(self, conta_id):
        conta = self.encontrar_conta_por_id(conta_id)
        if conta:
            return conta.obter_extrato()
        else:
            return "Conta não encontrada."
    def listar_transacoes_por_categoria(self, categoria):
        transacoes_categoria = []
        for conta in self.contas.values():
            for transacao in conta.transacoes:
                if transacao.categoria == categoria:
                    transacoes_categoria.append(transacao)
        return transacoes_categoria

    def listar_transacoes_por_data(self, id_conta, data_escolhida):
        conta = self.encontrar_conta_por_id(id_conta)
        if conta:
            return [t for t in conta.transacoes if t.get_data() == data_escolhida]
        else:
            return []

    def transferir_fundos(self, id_origem, id_destino, valor):
        conta_origem = self.encontrar_conta_por_id(id_origem)
        conta_destino = self.encontrar_conta_por_id(id_destino)

        if conta_origem and conta_destino and conta_origem.obter_saldo() >= valor:
            # Obter a data atual no formato desejado (por exemplo, DD/MM/YYYY)
            data_atual = datetime.now().strftime("%d/%m/%Y")

            # Criar transações para débito e crédito
            transacao_debito = Transacao(data_atual, -valor, "Transferência", "Débito")
            transacao_credito = Transacao(data_atual, valor, "Transferência", "Crédito")

            conta_origem.adicionar_transacao(transacao_debito)
            conta_destino.adicionar_transacao(transacao_credito)
            print("Transferência realizada com sucesso.")
        else:
            print("Transferência não realizada. Verifique as contas e os saldos.")
    def validar_transacao(self, id_conta, valor):
        conta = self.encontrar_conta_por_id(id_conta)
        if not conta:
            return False, "Conta não encontrada."
        if conta.obter_saldo() < valor:
            return False, "Saldo insuficiente."
        return True, "Validação bem-sucedida."
    def atualizar_saldos_se_necessario(self):
        for conta in self.contas.values():
            if conta.nova_importacao:
                conta.atualizar_saldo()
                conta.nova_importacao = False

