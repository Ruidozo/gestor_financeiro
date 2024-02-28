import csv
from carregador_extratos import CarregadorExtratos
from conta import ContaCorrente, ContaPoupanca, CartaoCredito, Credito
from datetime import datetime
from graficos import VisualizadorGraficos



class Interface:
    def __init__(self,gestor):
        self.gestor = gestor
        self.carregador = CarregadorExtratos(self.gestor)
        self.visualizador_graficos = VisualizadorGraficos(self.gestor)

    def iniciar(self):
        while True:
            print("\nMenu Principal")
            print("1. Gerir Contas")
            print("2. Ver Resumo Financeiro")
            print("3. Importar Extratos Bancários (CSV)")
            print("4. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.mostrar_submenu_gerir_contas()
            elif escolha == "2":
                self.mostrar_submenu_resumo_financeiro()
            elif escolha == "3":
                self.importar_extratos()
            elif escolha == "4":
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

    def mostrar_submenu_gerir_contas(self):
        while True:
            print("\nGerir Contas")
            print("1. Criar Conta")
            print("2. Apagar Conta")
            print("3. Editar Conta")
            print("4. Listar Contas")
            print("5. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.criar_conta()
            elif escolha == "2":
                self.apagar_conta()
            elif escolha == "3":
                self.editar_conta()
            elif escolha == "4":
                self.listar_contas()
            elif escolha == "5":
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

    def criar_conta(self):
        print("Tipo de conta:\n1 - Corrente\n2 - Poupança\n3 - Cartão de Crédito\n4 - Crédito")
        tipo_conta = input("Escolha o tipo de conta: ")

        if tipo_conta not in ["1", "2", "3", "4"]:
            print("Tipo de conta inválido.")
            return

        nome_referencia = input("Nome para referência da conta: ")
        id_conta = self.gestor.gerar_id_conta()  # Método para gerar um ID único para a conta

        if tipo_conta in ["1", "2", "4"]:  # Corrente, Poupança e Crédito
            valor_inicial = float(input("Valor inicial: "))

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
        print("Conta criada com sucesso!")

    def apagar_conta(self):
        conta_id_str = input("Insira o ID da conta a ser apagada: ")

        try:
            conta_id = int(conta_id_str)
        except ValueError:
            print("ID inválido: Por favor, insira um número.")
            return

        conta = self.gestor.encontrar_conta_por_id(conta_id)

        if conta is None:
            print("Conta não encontrada.")
            return

        saldo_conta = conta.obter_saldo()
        if saldo_conta < 0:
            self._tratar_conta_devedora(conta_id, saldo_conta)
        elif saldo_conta > 0:
            self._tratar_conta_credora(conta_id, saldo_conta)

        confirmacao = input("Tem certeza que deseja apagar esta conta? (sim/não): ")
        if confirmacao.lower() == 'sim':
            self.gestor.remover_conta(conta_id)
            print("Conta apagada com sucesso.")
        else:
            print("Operação cancelada.")

    def _tratar_conta_credora(self, conta_id, saldo_conta):
        print(f"A conta {conta_id} tem crédito. Saldo: {saldo_conta:.2f}")
        while True:
            id_conta_destino_str = input(
                "ID da conta para transferir o crédito (ou 'novo' para criar uma nova conta): ")
            if id_conta_destino_str.lower() == 'novo':
                self.criar_conta()
                continue

            try:
                id_conta_destino = int(id_conta_destino_str)
            except ValueError:
                print("ID inválido: Por favor, insira um número.")
                continue

            conta_destino = self.gestor.encontrar_conta_por_id(id_conta_destino)
            if conta_destino:
                self.gestor.transferir_fundos(conta_id, id_conta_destino, saldo_conta)
                break
            else:
                print("Conta de destino inválida.")
                resposta = input("Deseja tentar novamente? (sim/não): ")
                if resposta.lower() != 'sim':
                    break

    def editar_conta(self):
        conta_id_str = input("Insira o ID da conta que deseja editar: ")

        try:
            conta_id = int(conta_id_str)
        except ValueError:
            print("ID inválido. Por favor, insira um número.")
            return

        conta = self.gestor.encontrar_conta_por_id(conta_id)

        if conta is None:
            print("Conta não encontrada.")
            return

        print(f"Editando a conta: {conta_id}")
        print(f"Nome atual: {conta.titular}")
        print(f"Saldo inicial atual: {conta.saldo_inicial}")

        novo_titular = input("Insira o novo nome do titular (ou pressione Enter para manter o atual): ")
        novo_saldo_str = input("Insira o novo saldo inicial (ou pressione Enter para manter o atual): ")

        if novo_titular:
            conta.titular = novo_titular

        if novo_saldo_str:
            try:
                novo_saldo = float(novo_saldo_str)
                conta.saldo_inicial = novo_saldo
                conta.atualizar_saldo()  # Atualiza o saldo com base no novo saldo inicial
            except ValueError:
                print("Saldo inválido. Por favor, insira um número.")

        print("Conta atualizada com sucesso.")

    def listar_contas(self):
        if not self.gestor.contas:
            print("Não há contas na memória.")
            return

        print("\nLista de Contas:")
        for id_conta, conta in self.gestor.contas.items():
            saldo_atual = conta.calcular_saldo_atual()  # Calcula o saldo atual
            print(f"ID: {id_conta}, Titular: {conta.titular}, Saldo: {saldo_atual:.2f}")

    def mostrar_submenu_resumo_financeiro(self):
        while True:
            print("\nResumo Financeiro")
            print("1. Listar Saldos de Todas as Contas")
            print("2. Listagem de Movimentos")
            print("3. Visualização de Gráficos")
            print("4. Exportação de Dados")
            print("5. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.listar_saldos_contas()
            elif escolha == "2":
                self.mostrar_submenu_listagem_movimentos()
            elif escolha == "3":
                self.mostrar_submenu_graficos()
            elif escolha == "4":
                self.exportar_dados()
            elif escolha == "5":
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

    def listar_saldos_contas(self):
        if not self.gestor.contas:
            print("Não há contas em memória.")
            return

        print("\nSaldos de Todas as Contas:")
        for id_conta, conta in self.gestor.contas.items():
            saldo_atual = conta.calcular_saldo_atual()  # Calcula o saldo atual
            print(f"ID: {id_conta}, Titular: {conta.titular}, Saldo: {saldo_atual:.2f}")

    def mostrar_submenu_listagem_movimentos(self):
        print("\nListagem de Movimentos")
        print("1. Listar Movimentos por Data")
        print("2. Listar Movimentos por Categoria")
        print("3. Listar Todos os Movimentos da Conta")
        print("4. Voltar")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            self.listar_movimentos_por_data()
        elif escolha == "2":
            self.listar_movimentos_por_categoria()
        elif escolha == "3":
            self.listar_todos_movimentos()
        elif escolha == "4":
            return
        else:
            print("Opção inválida. Por favor, tente novamente.")

    def listar_movimentos_por_data(self):
        # Listar as contas disponíveis
        print("Contas disponíveis:")
        for id_conta in self.gestor.contas:
            print(f"ID da Conta: {id_conta}")

        # Pedir ao usuário para escolher uma conta e converter para inteiro
        id_escolhido_str = input("Insira o ID da conta para listar os movimentos: ")
        try:
            id_escolhido = int(id_escolhido_str)
        except ValueError:
            print("ID inválido.")
            return

        if id_escolhido not in self.gestor.contas:
            print("Conta não encontrada.")
            return

        # Solicitar a data
        data_escolhida_str = input("Insira a data para listar os movimentos (formato YYYY-MM-DD): ")
        try:
            # Converter a entrada do usuário para o formato de data das transações
            data_escolhida = datetime.strptime(data_escolhida_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            print("Formato de data inválido.")
            return

        # Filtrar as transações pela data na conta escolhida
        transacoes = self.gestor.listar_transacoes_por_data(id_escolhido, data_escolhida)

        # Verificar se transações foram encontradas e exibir
        if transacoes:
            for transacao in transacoes:
                print(f"{transacao.get_data()} - {transacao.get_descricao()} - {transacao.get_valor():.2f} - {transacao.get_categoria()}")
        else:
            print("Nenhuma transação encontrada para esta data nesta conta.")

    def listar_movimentos_por_categoria(self):
        categoria_escolhida = input("Insira a categoria para listar os movimentos: ")

        # Debugging: imprimir todas as categorias disponíveis
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
            print("Nenhuma transação encontrada para esta categoria.")

    def listar_todos_movimentos(self):
        id_conta = input("Insira o ID da conta para listar os movimentos: ")

        try:
            id_conta_int = int(id_conta)
        except ValueError:
            print(f"ID inválido: {id_conta} não é um número.")
            return

        conta = self.gestor.encontrar_conta_por_id(id_conta_int)
        if not conta:
            print(f"Conta com ID {id_conta} não encontrada.")
            return

        transacoes = conta.obter_extrato()
        if transacoes:
            print(f"\nMovimentos para a conta {id_conta}:")
            self.imprimir_transacoes(transacoes)
        else:
            print("Não há movimentos para esta conta.")

    def imprimir_transacoes(self, transacoes):
        print("{:<10} {:<15} {:<20} {:<30}".format('Data', 'Valor', 'Categoria', 'Descrição'))
        for transacao in transacoes:
            print("{:<10} {:<15} {:<20} {:<30}".format(
                transacao.get_data(),
                f"{transacao.get_valor():.2f}",
                transacao.get_categoria(),
                transacao.get_descricao()
            ))

    def mostrar_submenu_graficos(self):
        while True:
            print("\nSubmenu de Gráficos")
            print("1. Visualizar Gastos por Descrição")
            print("2. Visualizar Gastos por Categoria")
            print("3. Visualizar Salários por Mês")
            print("4. Visualizar Saldo de uma conta ao Longo do Tempo")
            print("5. Voltar")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.visualizador_graficos.visualizar_gastos_por_descricao()
            elif escolha == "2":
                self.visualizador_graficos.visualizar_gastos_por_categoria()
            elif escolha == "3":
                self.visualizador_graficos.visualizar_salarios_por_mes()
            elif escolha == "4":
                self.visualizador_graficos.visualizar_saldo_conta()
            elif escolha == "5":
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

    def exportar_dados(self):
        # Pede ao usuário o nome do arquivo para salvar os dados
        nome_arquivo = input("Insira o nome do arquivo para exportar os dados (ex: dados.csv): ")
        caminho_arquivo = f"./{nome_arquivo}"

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

        print(f"Dados exportados com sucesso para {caminho_arquivo}")

    def importar_extratos(self):
        caminho_arquivo = input("Digite o caminho do arquivo CSV de extratos bancários: ")
        self.carregador.carregar_extratos(caminho_arquivo)
        print("Extratos bancários importados com sucesso!")

