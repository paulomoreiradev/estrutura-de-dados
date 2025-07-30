from produto import LoteProduto
from estoques import *
from vendas import *
from validacoes import *
import sys

def menu():
    if not estoque:
        print("\nAVISO: O estoque está vazio. Considere cadastrar produtos.")

    while True:
        print("\n--- SISTEMA DE ESTOQUE ---")
        print("1. Cadastrar produto")
        print("2. Atualizar estoque")
        print("3. Vender produto")
        print("4. Relatório de vendas")
        print("5. Listar produtos vencidos")  # Renomeado para maior clareza
        print("6. Remover produtos vencidos")  # Nova opção
        print("7. Consultar produtos")
        print("0. Sair")
        try:
            opcao = input("Escolha: ").strip()

            if opcao == "1":
                cadastrar_produto()
            elif opcao == "2":
                atualizar_estoque_menu()
            elif opcao == "3":
                vender_produto_menu()
            elif opcao == "4":
                relatorio_vendas()
            elif opcao == "5":
                listar_produtos_vencidos()
            elif opcao == "6":
                remover_produtos_vencidos_menu()
            elif opcao == "7":
                consultar_produtos_menu()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

        except ValidacaoError as e:
            print(f"\nErro de validação: {e}")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")

def cadastrar_produto():
    """Submenu para cadastro de produtos com validações"""
    print("\n--- CADASTRO DE PRODUTO ---")

    codigo = input_com_retry(
        "Código: ",
        validar_codigo,
        str,
        "Código inválido:"
    )

    nome = input_com_retry(
        "Nome: ",
        validar_nome,  # Usando a nova função de validação
        str,
        "Nome inválido:"
    )

    quantidade = input_com_retry(
        "Quantidade: ",
        validar_quantidade,
        int,
        "Quantidade inválida:"
    )

    preco = input_com_retry(
        "Preço: ",
        validar_preco,
        float,
        "Preço inválido:"
    )

    validade = None
    while True:
        validade_input = input("Validade (YYYY-MM-DD) ou Enter para sem validade: ").strip()
        if not validade_input:
            break
        try:
            validade = validar_data_validade(validade_input)
            break
        except DataInvalidaError as e:
            print(f"\nData inválida: {e}")

    produto = LoteProduto(codigo, nome, quantidade, preco, validade)
    cadastrar_lote(produto)
    print("\nProduto cadastrado com sucesso!")

def atualizar_estoque_menu():
    """Submenu para atualização de estoque com retry"""
    print("\n--- ATUALIZAR ESTOQUE ---")

    try:
        codigo = input_com_retry(
            "Código do produto: ",
            validar_codigo,
            str,
            "Código inválido:"
        )

        # Verifica se o produto existe mostrando os dados atuais
        produtos = consultar_por_codigo(codigo)
        if not produtos:
            print("\nProduto não encontrado.")
            if input("Deseja tentar outro código? (S/N): ").upper() == 'S':
                return atualizar_estoque_menu()
            return

        print("\nProduto encontrado:")
        for i, p in enumerate(produtos, 1):
            print(f"{i}. {p.nome} - Qtd atual: {p.quantidade}")

        nova_qtd = input_com_retry(
            "Nova quantidade: ",
            validar_quantidade,
            int,
            "Quantidade inválida:"
        )

        # Confirmação antes de atualizar
        print(f"\nConfirmar atualização?")
        print(f"Quantidade atual: {produtos[0].quantidade} → Nova quantidade: {nova_qtd}")
        if input("(S/N): ").upper() != 'S':
            print("Atualização cancelada.")
            return

        atualizar_estoque(codigo, nova_qtd)
        print("\nEstoque atualizado com sucesso!")

        # Mostra os dados atualizados
        produtos_atualizados = consultar_por_codigo(codigo)
        print("\nDados atualizados:")
        for i, p in enumerate(produtos_atualizados, 1):
            print(f"{i}. {p.nome} - Qtd atual: {p.quantidade}")

    except Exception as e:
        print(f"\nErro ao atualizar estoque: {e}")

def vender_produto_menu():
    """Submenu para venda de produtos com validações"""
    print("\n--- VENDER PRODUTO ---")
    codigo = validar_codigo(input("Código do produto: "))
    qtd = validar_quantidade(input("Quantidade: "))

    if realizar_venda(codigo, qtd):
        print("\nVenda realizada com sucesso!")
    else:
        print("\nFalha ao realizar venda!")

def relatorio_vendas():
    """Exibe relatório de vendas completo com faturamento"""
    print("\n--- RELATÓRIO DE VENDAS ---")

    relatorio = gerar_relatorio()

    if relatorio['quantidade_vendas'] == 0:
        print("Nenhuma venda registrada.")
        return

    # Exibe o resumo do faturamento
    print(f"\nRESUMO:")
    print(f"Total de vendas realizadas: {relatorio['quantidade_vendas']}")
    print(f"Faturamento total: R${relatorio['faturamento_total']:.2f}")
    print("-" * 40)

    # Exibe os detalhes de cada venda
    print("\nDETALHES DAS VENDAS:")
    for i, venda in enumerate(relatorio['vendas'], 1):
        print(f"\nVenda #{i}")
        print(f"Data: {venda['data'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Código: {venda['codigo']}")
        print("Itens:")
        for item in venda['itens']:
            print(f"  - {item[0]} (Qtd: {item[1]}, Preço: R${item[2]:.2f})")
        print(f"Valor da venda: R${venda['valor_total']:.2f}")
        print("-" * 40)

def listar_produtos_vencidos():
    """Lista produtos vencidos formatado"""
    print("\n--- PRODUTOS VENCIDOS ---")
    vencidos = [p for p in listar_estoque() if p.is_vencido()]

    if not vencidos:
        print("Nenhum produto vencido encontrado.")
        return

    total_itens = sum(p.quantidade for p in vencidos)

    for i, produto in enumerate(vencidos, 1):
        print(f"{i}. {produto.nome} (Cód: {produto.codigo}) - Qtd: {produto.quantidade}, Vencido em: {produto.validade}")

    print(f"\nTotal de lotes vencidos: {len(vencidos)}")
    print(f"Total de itens vencidos: {total_itens}")

def consultar_produtos_menu():
    """Submenu para consulta de produtos"""
    print("\n--- CONSULTAR PRODUTOS ---")
    print("1. Consultar todos")
    print("2. Consultar por código")
    print("3. Consultar por nome")
    print("0. Voltar")

    opcao = input("Escolha: ").strip()

    if opcao == "1":
        exibir_todos_produtos()
    elif opcao == "2":
        consultar_por_codigo_menu()
    elif opcao == "3":
        consultar_por_nome_menu()
    elif opcao == "0":
        return
    else:
        print("Opção inválida!")

def remover_produtos_vencidos_menu():
    """Submenu para remoção de produtos vencidos"""
    print("\n--- REMOVER PRODUTOS VENCIDOS ---")

    # Primeiro mostra o que será removido
    vencidos = [p for p in listar_estoque() if p.is_vencido()]

    if not vencidos:
        print("Nenhum produto vencido encontrado.")
        return

    print("\nProdutos vencidos que serão removidos:")
    for i, p in enumerate(vencidos, 1):
        print(f"{i}. {p.nome} (Cód: {p.codigo}) - Qtd: {p.quantidade}, Vencido em: {p.validade}")

    # Pede confirmação
    confirmacao = input("\nDeseja realmente remover todos os produtos vencidos listados acima? (S/N): ").upper()

    if confirmacao == 'S':
        lotes_removidos, itens_removidos = remover_produtos_vencidos()
        print(f"\nRemoção concluída:")
        print(f"- Lotes removidos: {lotes_removidos}")
        print(f"- Itens descartados: {itens_removidos}")
    else:
        print("Operação cancelada.")

def exibir_todos_produtos():  # Mudei o nome da função
    """Lista todos os produtos formatado"""
    print("\n--- TODOS OS PRODUTOS ---")
    produtos = consultar_todos_produtos()  # Agora chama a função do estoques.py

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for i, p in enumerate(produtos, 1):
        print(f"{i}. {p.nome} (Cód: {p.codigo}) - Qtd: {p.quantidade}, Preço: R${p.preco:.2f}, Validade: {p.validade or 'N/A'}")

def consultar_por_codigo_menu():
    """Consulta produto por código com validação"""
    codigo = validar_codigo(input("\nDigite o código: "))
    produtos = consultar_por_codigo(codigo)

    if not produtos:
        print("Produto não encontrado.")
        return

    for p in produtos:
        print("\nDetalhes do Produto:")
        print(f"Código: {p.codigo}")
        print(f"Nome: {p.nome}")
        print(f"Quantidade: {p.quantidade}")
        print(f"Preço: R${p.preco:.2f}")
        print(f"Validade: {p.validade or 'N/A'}")

def consultar_por_nome_menu():
    """Consulta produto por nome"""
    nome = input("\nDigite o nome ou parte do nome: ").strip()
    if not nome:
        print("Termo de busca não pode ser vazio.")
        return

    resultados = consultar_por_nome(nome)

    if not resultados:
        print("Nenhum produto encontrado.")
        return

    print(f"\nResultados para '{nome}':")
    for i, p in enumerate(resultados, 1):
        print(f"{i}. {p.nome} (Cód: {p.codigo}) - Qtd: {p.quantidade}, Preço: R${p.preco:.2f}")

if __name__ == "__main__":
    menu()
