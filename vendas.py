from datetime import datetime
from estoques import estoque
from lists import LinkedList

vendas = LinkedList()



def realizar_venda(codigo, quantidade):
    if codigo not in estoque:
        print("Produto não encontrado.")
        return False

    lotes = estoque[codigo]
    atual = lotes._head
    quantidade_restante = quantidade
    venda_total = 0
    venda_registro = []
    nome_produto = None

    while atual and quantidade_restante > 0:
        lote = atual.get_element()

        if lote.quantidade == 0 or lote.is_vencido():
            atual = atual.get_next()
            continue

        nome_produto = lote.nome

        if lote.quantidade >= quantidade_restante:
            venda_total += quantidade_restante * lote.preco
            venda_registro.append((lote.validade, quantidade_restante, lote.preco))
            lote.quantidade -= quantidade_restante
            quantidade_restante = 0
        else:
            venda_total += lote.quantidade * lote.preco
            venda_registro.append((lote.validade, lote.quantidade, lote.preco))
            quantidade_restante -= lote.quantidade
            lote.quantidade = 0

        atual = atual.get_next()

    if quantidade_restante > 0:
        print("Estoque insuficiente para realizar a venda.")
        return False

    registro = {
        "data": datetime.now(),
        "codigo": codigo,
        "itens": [(nome_produto, q, p) for (_, q, p) in venda_registro],
        "valor_total": venda_total
    }
    vendas.append(registro)

    # 🔽 Mini relatório
    print("\n=== Venda realizada com sucesso ===")
    print(f"Data: {registro['data'].strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Produto: {nome_produto} (código: {codigo})")
    print("Lotes utilizados:")
    for validade, qtd, preco in venda_registro:
        print(f"  - Validade: {validade}, Qtd: {qtd}, Preço: R${preco:.2f}")
    print(f"Valor total da venda: R${venda_total:.2f}")
    print("====================================\n")

    return True

def gerar_relatorio():
    relatorio = []
    atual = vendas._head
    while atual:
        relatorio.append(atual.get_element())
        atual = atual.get_next()
    return relatorio
