from produto import LoteProduto
from estoques import *
from vendas import *

def menu():
    while True:
        print("\n--- SISTEMA DE ESTOQUE ---")
        print("1. Cadastrar produto")
        print("2. Atualizar estoque")
        print("3. Vender produto")
        print("4. Relatório de vendas")
        print("5. Produtos vencidos")
        print("6. Consultar produtos")
        print("0. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            codigo = input("Código: ")
            nome = input("Nome: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            validade_input = input("Validade (YYYY-MM-DD) ou Enter: ")
            validade = None
            if validade_input:
                from datetime import datetime
                validade = datetime.strptime(validade_input, "%Y-%m-%d").date()
            produto = LoteProduto(codigo, nome, quantidade, preco, validade)
            cadastrar_lote(produto)
            print("Produto cadastrado!")

        elif opcao == "2":
            codigo = input("Código do produto: ")
            nova_qtd = int(input("Nova quantidade: "))
            atualizar_estoque(codigo, nova_qtd)

        elif opcao == "3":
            codigo = input("Código do produto: ")
            qtd = int(input("Quantidade: "))
            if realizar_venda(codigo, qtd):
                print("Venda realizada!")
            else:
                print("Venda falhou!")

        elif opcao == "4":
            for v in gerar_relatorio():
                print(v)

        elif opcao == "5":
            for produto in listar_estoque():
                if produto.is_vencido():
                    print(f"{produto.nome} está vencido!")

        elif opcao == "6":
            print("1. Consultar todos")
            print("2. Consultar por código")
            print("3. Consultar por nome")
            tipo = input("Escolha o tipo de consulta: ")

            if tipo == "1":
                for p in consultar_todos_produtos():
                    print(vars(p))
            elif tipo == "2":
                codigo = input("Digite o código: ")
                produto = consultar_por_codigo(codigo)
                if produto:
                    print(vars(produto))
                else:
                    print("Produto não encontrado.")
            elif tipo == "3":
                nome = input("Digite o nome ou parte do nome: ")
                resultados = consultar_por_nome(nome)
                if resultados:
                    for p in resultados:
                        print(vars(p))
                else:
                    print("Nenhum produto encontrado.")

        elif opcao == "0":
            break

if __name__ == "__main__":
    menu()
