from carregador_extratos import CarregadorExtratos
from conta import ContaCorrente, ContaPoupanca, CartaoCredito, Credito
from datetime import datetime
from graficos import VisualizadorGraficos
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import tkinter.ttk as ttk
import csv
from datetime import datetime
from tkinter import simpledialog


class InterfaceGrafica:
    def __init__(self, gestor):
        self.gestor = gestor  # This is correct
        self.janela = tk.Tk()
        self.janela.title("Gestor Financeiro vs. 2.0")

        self.frame_menu_principal = tk.Frame(self.janela)
        self.frame_menu_principal.pack(fill=tk.BOTH, expand=True)

        self.label_titulo = tk.Label(self.frame_menu_principal, text="Menu Principal")
        self.label_titulo.pack()

        self.button_gerir_contas = ttk.Button(self.frame_menu_principal, text="Gerir Contas", command=self.mostrar_submenu_gerir_contas)
        self.button_gerir_contas.pack(pady=10)

        self.button_resumo_financeiro = ttk.Button(self.frame_menu_principal, text="Ver Resumo Financeiro", command=self.mostrar_submenu_resumo_financeiro)
        self.button_resumo_financeiro.pack(pady=10)

        self.button_importar_extratos = ttk.Button(self.frame_menu_principal, text="Importar Extratos Bancários (CSV)", command=lambda: self.carregar_extratos())
        self.button_importar_extratos.pack(pady=10)

        self.button_sair = ttk.Button(self.frame_menu_principal, text="Sair", command=self.janela.quit)
        self.button_sair.pack(pady=10)

    def iniciar(self):
        self.janela.mainloop()

    def mostrar_erro(self, mensagem):
        erro_window = tk.Toplevel(self.janela)
        erro_window.title("Erro")
        erro_window.geometry("300x150")  # Set the window size

        label_erro = tk.Label(erro_window, text=mensagem, font=("Arial", 14))  # Customize the font
        label_erro.pack(pady=20)

        button_ok = tk.Button(erro_window, text="OK", command=erro_window.destroy, width=10)  # Adjust the button width
        button_ok.pack(pady=10)

    def mostrar_sucesso(self, janela_a_fechar):
        def mostrar_sucesso(self, janela_a_fechar):
            sucesso_window = tk.Toplevel(self.janela)
            sucesso_window.title("Sucesso")

            style = ttk.Style()
            style.configure("TLabel", font=("Arial", 14))
            style.configure("TButton", font=("Arial", 12))

            label_sucesso = ttk.Label(sucesso_window, text="Operação realizada com sucesso!")
            label_sucesso.pack(pady=20)

            button_voltar = ttk.Button(sucesso_window, text="Voltar", command=lambda: [sucesso_window.destroy(), janela_a_fechar.destroy()])
            button_voltar.pack(pady=10)

            sucesso_window.geometry("300x150")

    def mostrar_submenu_gerir_contas(self):

        submenu_gerir_contas = tk.Toplevel(self.janela)
        submenu_gerir_contas.title("Gerir Contas")

        label_titulo = ttk.Label(submenu_gerir_contas, text="Gerir Contas")
        label_titulo.pack()

        button_criar_conta = ttk.Button(submenu_gerir_contas, text="Criar Conta", command=self.criar_conta)
        button_criar_conta.pack()

        button_apagar_conta = ttk.Button(submenu_gerir_contas, text="Apagar Conta", command=self.apagar_conta)
        button_apagar_conta.pack()

        button_editar_conta = ttk.Button(submenu_gerir_contas, text="Editar Conta", command=self.editar_conta)
        button_editar_conta.pack()

        button_listar_contas = ttk.Button(submenu_gerir_contas, text="Listar Contas", command=self.listar_contas)
        button_listar_contas.pack()

        button_voltar = ttk.Button(submenu_gerir_contas, text="Voltar ao Menu Principal",
                                  command=submenu_gerir_contas.destroy)
        button_voltar.pack()

    def criar_conta(self):
        submenu_criar_conta = tk.Toplevel(self.janela)
        submenu_criar_conta.title("Criar Conta")

        label_titulo = tk.Label(submenu_criar_conta, text="Criar Conta")
        label_titulo.pack()

        label_tipo_conta = tk.Label(submenu_criar_conta, text="Tipo de conta:")
        label_tipo_conta.pack()

        tipo_conta_var = tk.StringVar()
        tipo_conta_var.set("1")  # Padrão para Conta Corrente

        radio_conta_corrente = tk.Radiobutton(submenu_criar_conta, text="Conta Corrente", variable=tipo_conta_var, value="1")
        radio_conta_poupanca = tk.Radiobutton(submenu_criar_conta, text="Conta Poupança", variable=tipo_conta_var, value="2")
        radio_cartao_credito = tk.Radiobutton(submenu_criar_conta, text="Cartão de Crédito", variable=tipo_conta_var, value="3")
        radio_credito = tk.Radiobutton(submenu_criar_conta, text="Crédito", variable=tipo_conta_var, value="4")

        radio_conta_corrente.pack()
        radio_conta_poupanca.pack()
        radio_cartao_credito.pack()
        radio_credito.pack()

        label_nome_referencia = tk.Label(submenu_criar_conta, text="Nome para referência da conta:")
        label_nome_referencia.pack()
        nome_referencia_var = tk.StringVar()
        entry_nome_referencia = tk.Entry(submenu_criar_conta, textvariable=nome_referencia_var)
        def validate_float_input(input):
            try:
                float(input)
                return True
            except ValueError:
                messagebox.showerror("Erro", "Numero invalido.")
                return False

        entry_nome_referencia.pack()

        label_valor_inicial = tk.Label(submenu_criar_conta, text="Valor inicial:")
        label_valor_inicial.pack()
        valor_inicial_var = tk.StringVar()
        entry_valor_inicial = tk.Entry(submenu_criar_conta, textvariable=valor_inicial_var)
        entry_valor_inicial.pack()

        entry_valor_inicial.config(validate="key", validatecommand=(submenu_criar_conta.register(validate_float_input), "%P"))

        button_criar = tk.Button(submenu_criar_conta, text="Criar", command=lambda: self.criar_conta_logic(tipo_conta_var.get(), nome_referencia_var.get(), valor_inicial_var.get()))
        button_criar.pack()

        button_voltar = tk.Button(submenu_criar_conta, text="Voltar", command=submenu_criar_conta.destroy)
        button_voltar.pack()

    def criar_conta_logic(self, tipo_conta, nome_referencia, valor_inicial):
        if tipo_conta not in ["1", "2", "3", "4"]:
            print("Tipo de conta inválido.")
            return

        id_conta = self.gestor.gerar_id_conta()  # Método para gerar um ID único para a conta

        if tipo_conta in ["1", "2", "4"]:  # Corrente, Poupança e Crédito
            valor_inicial = float(valor_inicial)

        if tipo_conta == "1":
            # Criação de Conta Corrente
            conta = ContaCorrente(id_conta, nome_referencia, valor_inicial)
        elif tipo_conta == "2":
            # Criação de Conta Poupança
            taxa_juros = float(input("Taxa de Juros: "))
            periodo_juros = input("Aplicar juros: 1 - Mensalmente, 2 - Anualmente: ")
            conta = ContaPoupanca(id_conta, nome_referencia, taxa_juros, periodo_juros, valor_inicial)
        elif tipo_conta == "3":
            # Criação de Cartão de Crédito
            limite_credito = float(input("Valor disponível para uso: "))
            conta = CartaoCredito(id_conta, nome_referencia, limite_credito)
        elif tipo_conta == "4":
            # Criação de Crédito
            tipo_credito = input("Tipo de crédito (pessoal, habitação, outro): ")
            taxa_juros = float(input("Taxa de Juros: "))
            # Lógica adicional para Crédito de Habitação e Euribor...
            conta = Credito(id_conta, nome_referencia, tipo_credito, taxa_juros, valor_inicial)

        self.gestor.adicionar_conta(conta)
         
    def apagar_conta(self):
        submenu_apagar_conta = tk.Toplevel(self.janela)
        submenu_apagar_conta.title("Apagar Conta")

        label_titulo = tk.Label(submenu_apagar_conta, text="Apagar Conta")
        label_titulo.pack()

        label_id_conta = tk.Label(submenu_apagar_conta, text="ID da conta:")
        label_id_conta.pack()
        id_conta_var = tk.StringVar()
        entry_id_conta = tk.Entry(submenu_apagar_conta, textvariable=id_conta_var)
        entry_id_conta.pack()

        button_apagar = tk.Button(submenu_apagar_conta, text="Apagar", command=lambda: self.apagar_conta_logic(id_conta_var.get(), submenu_apagar_conta))
        button_apagar.pack()

        button_voltar = tk.Button(submenu_apagar_conta, text="Voltar", command=submenu_apagar_conta.destroy)
        button_voltar.pack()

    def apagar_conta_logic(self, id_conta_str, janela_a_fechar):
        try:
            self.gestor.remover_conta(id_conta_str)
            self.mostrar_sucesso(janela_a_fechar)
        except ValueError as erro:
            self.mostrar_erro(str(erro))
    
    def editar_conta(self):

        conta_id_str = simpledialog.askstring("Editar Conta", "Insira o ID da conta que deseja editar:")
        if conta_id_str is None:
            return
        
        try:
            conta_id = int(conta_id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID inválido. Por favor, insira um número.")
            return

        conta = self.gestor.encontrar_conta_por_id(conta_id)

        if conta is None:
            messagebox.showerror("Erro", f"Conta com ID {conta_id} não encontrada.")
            return
        
    
        novo_titular = simpledialog.askstring("Editar Conta", "Insira o novo nome do titular (ou pressione Enter para manter o atual): ")
        novo_saldo_str = simpledialog.askstring("Editar Conta", "Insira o novo saldo inicial (ou pressione Enter para manter o atual): ")

        if novo_titular:
            conta.titular = novo_titular

        if novo_saldo_str:
            try:
                novo_saldo = float(novo_saldo_str)
                conta.saldo_inicial = novo_saldo
                conta.atualizar_saldo()  # Atualiza o saldo com base no novo saldo inicial
            except ValueError:
                messagebox.showerror("Erro", "Saldo inválido. Por favor, insira um número.")

                messagebox.showinfo("Sucesso", "Conta editada com sucesso.")   
       


    def listar_contas(self):

        submenu_listar_contas = tk.Toplevel(self.janela)
        submenu_listar_contas.title("Listar Contas")
        lista_contas_frame = tk.Frame(submenu_listar_contas)
        lista_contas_frame.pack(fill=tk.BOTH, expand=True)
        lista_contas_frame.pack_propagate(False)  # Resize the frame to fit its contents

        label_titulo = tk.Label(submenu_listar_contas, text="Listar Contas")
        label_titulo.pack()

        lista_contas = ttk.Treeview(submenu_listar_contas, columns=("ID", "Titular", "Saldo"), show="headings")
        lista_contas.heading("ID", text="ID")
        lista_contas.heading("Titular", text="Titular")
        lista_contas.heading("Saldo", text="Saldo")

        for id_conta, conta in self.gestor.contas.items():
            saldo_atual = conta.calcular_saldo_atual()  # Calcula o saldo atual
            lista_contas.insert("", tk.END, values=(id_conta, conta.titular, f"{saldo_atual:.2f}"))

        lista_contas.pack()

        button_voltar = tk.Button(submenu_listar_contas, text="Voltar", command=submenu_listar_contas.destroy)
        button_voltar.pack()

    def mostrar_submenu_resumo_financeiro(self):

        submenu_resumo_financeiro = tk.Toplevel(self.janela)
        button_listar_saldos = tk.Button(submenu_resumo_financeiro, text="Listar Saldos de todas as contas", command=self.listar_saldos)
        button_listar_saldos.pack()

        button_listar_movimentos = tk.Button(submenu_resumo_financeiro, text="Listagem de Movimentos", command=self.listar_movimentos)
        button_listar_movimentos.pack()

        button_visualizar_graficos = tk.Button(submenu_resumo_financeiro, text="Visualizar Gráficos", command=self.mostrar_submenu_graficos)
        button_visualizar_graficos.pack()

        button_exportar_dados = tk.Button(submenu_resumo_financeiro, text="Exportar Dados", command=self.exportar_dados)
        button_exportar_dados.pack()

        button_voltar = tk.Button(submenu_resumo_financeiro, text="Voltar ao Menu Principal", command=submenu_resumo_financeiro.destroy)
        button_voltar.pack()
       
    def listar_saldos(self):
        submenu_listar_contas = tk.Toplevel(self.janela)
        submenu_listar_contas.title("Listar Saldos de Contas")
        lista_contas_frame = tk.Frame(submenu_listar_contas)
        lista_contas_frame.pack(fill=tk.BOTH, expand=True)
        lista_contas_frame.pack_propagate(False)  # Resize the frame to fit its contents

        label_titulo = tk.Label(submenu_listar_contas, text="Listar Contas")
        label_titulo.pack()

        lista_contas = ttk.Treeview(submenu_listar_contas, columns=("ID", "Titular", "Saldo"), show="headings")
        lista_contas.heading("ID", text="ID")
        lista_contas.heading("Titular", text="Titular")
        lista_contas.heading("Saldo", text="Saldo")

        for id_conta, conta in self.gestor.contas.items():
            saldo_atual = conta.calcular_saldo_atual()  # Calcula o saldo atual
            lista_contas.insert("", tk.END, values=(id_conta, conta.titular, f"{saldo_atual:.2f}"))

        lista_contas.pack()

        button_voltar = tk.Button(submenu_listar_contas, text="Voltar", command=submenu_listar_contas.destroy)
        button_voltar.pack()

    def listar_movimentos(self):

        self.janela.title("Listagem Movimentos")
        submenu_resumo_financeiro = tk.Toplevel(self.janela)
        button_listar_saldos = tk.Button(submenu_resumo_financeiro, text="Listar Movimentos por Data", command=self.listar_movimentos_por_data)
        button_listar_saldos.pack()

        button_listar_movimentos = tk.Button(submenu_resumo_financeiro, text="Listar Movimentos por categoria", command=self.listar_movimentos_por_categoria)
        button_listar_movimentos.pack()

        button_voltar = tk.Button(submenu_resumo_financeiro, text="Voltar ao Menu Principal", command=submenu_resumo_financeiro.destroy)
        button_voltar.pack()

    
    def listar_movimentos_por_data(self):

        self.janela.title("Listagem Movimentos por Data")
        submenu_listar_contas = tk.Toplevel(self.janela)
        submenu_listar_contas.title("Contas disponiveis para listar movimentos por data")

        lista_contas_frame = tk.Frame(submenu_listar_contas)
        lista_contas_frame.pack(fill=tk.BOTH, expand=True)
        lista_contas_frame.pack_propagate(False)

        # Listar as contas disponíveis
        lista_contas = ttk.Treeview(submenu_listar_contas, columns=("ID", "Titular", "Saldo"), show="headings")
        lista_contas.heading("ID", text="ID")
        lista_contas.heading("Titular", text="Titular")
        lista_contas.heading("Saldo", text="Saldo")
        
        # Pedir ao usuário para escolher uma conta e converter para inteiro
        id_conta = simpledialog.askstring("ID da Conta", "Digite o ID da conta para listar os movimentos:")
        if id_conta is None:  # Check if the user cancels the dialog prompt
            return
        try:
            id_conta_int = int(id_conta)
        except ValueError:
            messagebox.showerror("Erro", f"ID inválido: {id_conta} não é um número.")
            return
                
        # Verificar se a conta existe
        if not self.gestor.encontrar_conta_por_id(id_conta_int):
            messagebox.showerror("Erro", f"Conta com ID {id_conta} não encontrada.")
            return
        
        # Pedir ao usuário para escolher uma data
        data = simpledialog.askstring("Data", "Insira a data para listar os movimentos (formato YYYY-MM-DD):")
        try:
            data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", f"Data inválida: {data} não está no formato correto.")
            return
        
        # Logica para listar os movimentos por data
        conta = self.gestor.encontrar_conta_por_id(id_conta_int)
        transacoes = self.gestor.listar_transacoes_por_data(id_conta_int, data)

        # Create a window for listing movements only once, before iterating over transactions
        submenu_listar_contas = tk.Toplevel(self.janela)
        submenu_listar_contas.title("Listar Movimentos por data")

        lista_movimentos_frame = tk.Frame(submenu_listar_contas)
        lista_movimentos_frame.pack(fill=tk.BOTH, expand=True)

        lista_movimentos = tk.Text(lista_movimentos_frame)
        lista_movimentos.pack()

        if transacoes:  # Check if there are any transactions to display
            for transacao in transacoes:
                lista_movimentos.insert(tk.END, f"{transacao.get_data()} - {transacao.get_descricao()} - {transacao.get_valor():.2f} - {transacao.get_categoria()}\n")
        else:
            lista_movimentos.insert(tk.END, "Nenhuma transação encontrada para esta data nesta conta.")

    def listar_movimentos_por_categoria(self):
        
        self.janela.title("Listagem Movimentos por Categoria")
        categoria_escolhida = simpledialog.askstring("Categoria", "Insira a categoria para listar os movimentos:")
        
        if not categoria_escolhida:  # User clicked cancel or closed the dialog
            return
        
        categorias_disponiveis = set()
        for conta in self.gestor.contas.values():
            for transacao in conta.transacoes:
                categorias_disponiveis.add(transacao.get_categoria())
        
        transacoes_categoria = []

        for conta in self.gestor.contas.values():
            transacoes_categoria.extend(
                [t for t in conta.transacoes if t.get_categoria().lower() == categoria_escolhida.lower()])
        
        if transacoes_categoria:
            self.imprimir_transacoes(transacoes_categoria)
        else:
            messagebox.showinfo("Resultado", "Nenhuma transação encontrada para esta categoria.")

    def imprimir_transacoes(self, transacoes):

        transacoes_window = tk.Toplevel()
        transacoes_window.title("Transações por Categoria")

        text_widget = scrolledtext.ScrolledText(transacoes_window)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for transacao in transacoes:
            transacao_info = f"Data: {transacao.get_data()}, Valor: {transacao.get_valor()}, Descrição: {transacao.get_descricao()}, Categoria: {transacao.get_categoria()}\n"
            text_widget.insert(tk.END, transacao_info)

        text_widget.config(state=tk.DISABLED)

    def listar_todos_movimentos(self):
        pass
    
    def mostrar_submenu_graficos(self):
        visualizador_graficos = VisualizadorGraficos(self.gestor)
        submenu_window = tk.Toplevel()
        submenu_window.title("Submenu de Gráficos")

        frame = ttk.Frame(submenu_window)
        frame.pack()

        ttk.Button(frame, text="Visualizar Gastos por Descrição", command=visualizador_graficos.visualizar_gastos_por_descricao).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(frame, text="Visualizar Gastos por Categoria", command=visualizador_graficos.visualizar_gastos_por_categoria).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(frame, text="Visualizar Salários por Mês", command=visualizador_graficos.visualizar_salarios_por_mes).grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(frame, text="Visualizar Saldo de uma conta ao Longo do Tempo", command=visualizador_graficos.visualizar_saldo_conta).grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(frame, text="Voltar", command=submenu_window.destroy).grid(row=3, columnspan=2, padx=10, pady=5)
        submenu_window.mainloop()

    def exportar_dados(self):

        # Pede ao usuário o nome do arquivo para salvar os dados
        nome_arquivo = simpledialog.askstring("Exportar Dados", "Insira o nome do arquivo para salvar os dados:")
        if nome_arquivo is None:  # Verifica se o usuário cancelou a operação
            return
        else:
            caminho_arquivo = f"./{nome_arquivo}.csv"

        # Abre o arquivo para escrita
        with open(caminho_arquivo, mode='w', newline='') as arquivo:
            escritor_csv = csv.writer(arquivo)

            # Escreve o cabeçalho do CSV
            escritor_csv.writerow(['ID Conta', 'Titular', 'Saldo Inicial', 'Saldo Atual', 'Transações'])

            # Itera sobre todas as contas e suas transações para escrever os dados
            for id_conta, conta in self.gestor.contas.items():
                # Prepara as transações como uma string
                transacoes_str = '; '.join([str(transacao) for transacao in conta.transacoes])

                # Escreve uma linha para cada conta
                escritor_csv.writerow(
                    [id_conta, conta.titular, conta.saldo_inicial, conta.obter_saldo(), transacoes_str])

        messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para {caminho_arquivo}")

    def carregar_extratos(self):
        carregador = CarregadorExtratos(self.gestor)
        carregador.carregar_extratos()
        


