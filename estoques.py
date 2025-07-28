estoque = {}

def cadastrar_produto(produto):
    estoque[produto.codigo] = produto

def atualizar_estoque(codigo, nova_quantidade):
    if codigo in estoque:
        estoque[codigo].quantidade = nova_quantidade

def listar_estoque():
    return estoque.values()

def remover_produto(codigo):
    if codigo in estoque:
        del estoque[codigo]

def consultar_todos_produtos():
    return list(estoque.values())

def consultar_por_codigo(codigo):
    return estoque.get(codigo)

def consultar_por_nome(nome):
    resultados = []
    for produto in estoque.values():
        if nome.lower() in produto.nome.lower():
            resultados.append(produto)
    return resultados
