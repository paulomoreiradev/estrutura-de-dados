from datetime import datetime
from estoques import estoque

vendas = []

def realizar_venda(codigo, quantidade):
    if codigo in estoque and estoque[codigo].quantidade >= quantidade:
        estoque[codigo].quantidade -= quantidade
        vendas.append({
            "data": datetime.now(),
            "produto": estoque[codigo].nome,
            "quantidade": quantidade,
            "valor_total": quantidade * estoque[codigo].preco
        })
        return True
    return False

def gerar_relatorio():
    return vendas
