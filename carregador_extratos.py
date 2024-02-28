import os
import csv
from transacao import Transacao
from tkinter import Tk, filedialog, simpledialog, messagebox


class CarregadorExtratos:
    def __init__(self, gestor):
        self.gestor = gestor

    def carregar_extratos(self):

        root = Tk()
        root.withdraw()
        caminho_do_arquivo = filedialog.askopenfilename()

        id_conta = simpledialog.askstring("ID da Conta", "Digite o ID da conta para importar o extrato:")

        # Check if id_conta is None
        if id_conta is None:
            root.destroy()
            return

        # Converte o ID da conta para um inteiro
        try:
            id_conta_int = int(id_conta)
        except ValueError:
            messagebox.showerror("Erro", f"ID inválido: {id_conta} não é um número.")
            root.destroy()
            return

        # Validação do ID da conta
        if not self.gestor.encontrar_conta_por_id(id_conta_int):
            messagebox.showerror("Erro", f"Conta com ID {id_conta} não encontrada.")
            root.destroy()
            return

        conta = self.gestor.encontrar_conta_por_id(id_conta_int)

        # Verificação da existência do ficheiro
        if not os.path.isfile(caminho_do_arquivo):
            messagebox.showerror("Erro", "Ficheiro não encontrado.")
            root.destroy()
            return

        try:
            with open(caminho_do_arquivo, 'r') as arquivo:
                leitor_csv = csv.reader(arquivo)
                next(leitor_csv)  # Pular cabeçalho
                for linha in leitor_csv:
                    data, valor, descricao, categoria = linha
                    transacao = Transacao(data, float(valor), descricao, categoria)
                    conta.adicionar_transacao(transacao)

            messagebox.showinfo("Sucesso", f"Extrato importado com sucesso para a conta {id_conta_int}.")
            root.destroy()
            
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar extrato: {e}")
            root.destroy()
            return
        


        # Verificar a flag antes de carregar as transações
        if conta.nova_importacao:
            return

        # Atualizar a flag após importar com sucesso
        conta.nova_importacao = True
        id_conta = simpledialog.askstring("ID da Conta", "Digite o ID da conta para importar o extrato:")
