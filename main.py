from gestor_financeiro import GestorFinanceiro
from interface import Interface
from interface_grafica import InterfaceGrafica

def main():
    gestor = GestorFinanceiro()
    gestor.carregar_contas_csv()
    gestor.carregar_transacoes_csv()

    #interface_usuario = Interface(gestor) # Cria uma instancia da classe Interface (nao gráfica)
    #interface_usuario.iniciar()

    interface_grafica = InterfaceGrafica(gestor)  # Cria uma instância da classe InterfaceGrafica
    interface_grafica.iniciar()

    gestor.salvar_contas_csv()
    gestor.salvar_transacoes_csv()

if __name__ == "__main__":
    main()
