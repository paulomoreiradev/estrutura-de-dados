from datetime import datetime
from estoques import estoque
from lists import LinkedList
from validacoes import ProdutoNaoEncontradoError, validar_codigo, validar_quantidade

vendas = LinkedList()



def realizar_venda(codigo, quantidade):
    """
    Realiza a venda de um produto, verificando estoque e validades.
    """
    try:
        # Validações iniciais
        codigo = validar_codigo(codigo)
        quantidade = validar_quantidade(quantidade)

        if codigo not in estoque:
            raise ProdutoNaoEncontradoError(f"Produto com código {codigo} não encontrado")

        lotes = estoque[codigo]
        atual = lotes._head
        quantidade_restante = quantidade
        venda_total = 0.0
        venda_registro = []
        nome_produto = None
        lotes_disponiveis = False

        # Processa os lotes disponíveis
        while atual and quantidade_restante > 0:
            lote = atual.get_element()

            # Verifica se o lote está disponível para venda
            if lote.quantidade == 0 or lote.is_vencido():
                atual = atual.get_next()
                continue

            lotes_disponiveis = True
            nome_produto = lote.nome

            # Calcula quanto pode ser vendido deste lote
            quantidade_vendida = min(lote.quantidade, quantidade_restante)
            valor_parcial = quantidade_vendida * lote.preco

            venda_total += valor_parcial
            venda_registro.append((lote.validade, quantidade_vendida, lote.preco))

            # Atualiza estoque
            lote.quantidade -= quantidade_vendida
            quantidade_restante -= quantidade_vendida

            atual = atual.get_next()

        # Verifica se a venda foi completada
        if quantidade_restante > 0:
            if not lotes_disponiveis:
                raise ValueError("Produto não possui lotes válidos (todos vencidos ou sem estoque)")
            else:
                raise ValueError(f"Estoque insuficiente. Faltam {quantidade_restante} unidades")

        # Registra a venda
        registro = {
            "data": datetime.now(),
            "codigo": codigo,
            "itens": [(nome_produto, q, p) for (_, q, p) in venda_registro],
            "valor_total": venda_total
        }
        vendas.append(registro)

        # Gera relatório da venda
        print("\n=== Venda realizada com sucesso ===")
        print(f"Data: {registro['data'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Produto: {nome_produto} (código: {codigo})")
        print(f"Quantidade total: {quantidade}")
        print("Lotes utilizados:")
        for validade, qtd, preco in venda_registro:
            val_str = validade.strftime('%d/%m/%Y') if validade else "N/A"
            print(f"  - Validade: {val_str}, Qtd: {qtd}, Preço unitário: R${preco:.2f}")
        print(f"Valor total da venda: R${venda_total:.2f}")
        print("====================================")

        return True

    except Exception as e:
        print(f"\nErro ao realizar venda: {e}")
        return False

def gerar_relatorio():
    """
    Gera um relatório completo de vendas com faturamento total

    Returns:
        dict: Dicionário contendo:
            - 'vendas': lista de todas as vendas registradas
            - 'faturamento_total': soma de todos os valores de venda
            - 'quantidade_vendas': número total de vendas realizadas
    """
    vendas_lista = []
    faturamento_total = 0.0
    quantidade_vendas = 0

    # Percorre todas as vendas
    atual = vendas._head
    while atual:
        venda = atual.get_element()
        vendas_lista.append(venda)
        faturamento_total += venda['valor_total']
        quantidade_vendas += 1
        atual = atual.get_next()

    return {
        'vendas': vendas_lista,
        'faturamento_total': faturamento_total,
        'quantidade_vendas': quantidade_vendas
    }

