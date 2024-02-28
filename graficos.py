import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from datetime import datetime
from tkinter import messagebox, simpledialog, scrolledtext
from tkinter import simpledialog, messagebox
from tkinter.messagebox import showinfo
import tkinter.ttk as ttk


class VisualizadorGraficos:
    def __init__(self, gestor_financeiro):
        self.gestor = gestor_financeiro

    def visualizar_saldo_conta(self):

        id_escolhido = simpledialog.askinteger("Saldo da Conta", "Insira o ID da conta para visualizar grafico:")
        try:
            id_escolhido = int(id_escolhido)
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return

        conta = self.gestor.contas.get(id_escolhido)
        if not conta:
            messagebox.showerror("Erro", "Conta não encontrada.")
            return

        transacoes_ordenadas = sorted(conta.transacoes, key=lambda x: datetime.strptime(x.get_data(), "%d/%m/%Y"))

        # Inicializa o saldo e o mês atual
        saldo_atual = conta.saldo_inicial
        saldos_mensais = {}
        ultimo_dia_processado = None

        for transacao in transacoes_ordenadas:
            data_transacao = datetime.strptime(transacao.get_data(), "%d/%m/%Y")
            saldo_atual += transacao.get_valor()

            # Verifica se a transação é do próximo mês ou é a última transação
            if ultimo_dia_processado is None or data_transacao.month != ultimo_dia_processado.month:
                if ultimo_dia_processado is not None:
                    # Salva o saldo no último dia do mês anterior
                    saldos_mensais[ultimo_dia_processado] = saldo_atual

                # Atualiza o último dia processado
                ultimo_dia_do_mes = (data_transacao.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(
                    days=1)
                ultimo_dia_processado = ultimo_dia_do_mes

        # Certifique-se de capturar o saldo do último mês
        if ultimo_dia_processado not in saldos_mensais:
            saldos_mensais[ultimo_dia_processado] = saldo_atual

        # Gera o gráfico
        plt.figure(figsize=(10, 6))
        datas = list(saldos_mensais.keys())
        saldos = list(saldos_mensais.values())
        plt.plot(datas, saldos, marker='o')
        plt.title(f"Saldo no Final de Cada Mês para a Conta {id_escolhido}")
        plt.xlabel("Data")
        plt.ylabel("Saldo")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def visualizar_gastos_por_categoria(self):
        categorias = {}
        for conta in self.gestor.contas.values():
            for transacao in conta.transacoes:
                if transacao.get_valor() < 0:  # Apenas gastos
                    categoria = transacao.get_categoria()
                    categorias[categoria] = categorias.get(categoria, 0) + abs(transacao.get_valor())

        plt.figure(figsize=(10, 6))
        plt.bar(categorias.keys(), categorias.values(), color='skyblue')
        plt.title("Gastos por Categoria")
        plt.xlabel("Categoria")
        plt.ylabel("Gastos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def visualizar_gastos_por_descricao(self):
        descricoes = {}
        for conta in self.gestor.contas.values():
            for transacao in conta.transacoes:
                if transacao.get_valor() < 0:  # Considera apenas gastos
                    descricao = transacao.get_descricao()
                    descricoes[descricao] = descricoes.get(descricao, 0) + abs(transacao.get_valor())

        plt.figure(figsize=(10, 6))
        nomes_descricoes = list(descricoes.keys())
        valores_descricoes = list(descricoes.values())

        plt.bar(nomes_descricoes, valores_descricoes, color='skyblue')
        plt.title("Gastos por Descrição")
        plt.xlabel("Descrição")
        plt.ylabel("Gastos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def visualizar_salarios_por_mes(self):
        salarios = {}
        for conta in self.gestor.contas.values():
            for transacao in conta.transacoes:
                if transacao.get_categoria().lower() == "salário" and transacao.get_valor() > 0:
                    mes = datetime.strptime(transacao.get_data(), "%d/%m/%Y").strftime("%Y-%m")
                    salarios[mes] = salarios.get(mes, 0) + transacao.get_valor()

        plt.figure(figsize=(10, 6))
        plt.bar(salarios.keys(), salarios.values())
        plt.title("Salários por Mês")
        plt.xlabel("Mês")
        plt.ylabel("Salário Recebido")
        plt.xticks(rotation=45)
        plt.show()
