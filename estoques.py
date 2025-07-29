from lists import LinkedList

estoque = {}

def cadastrar_lote(lote):
    if lote.codigo not in estoque:
        estoque[lote.codigo] = LinkedList()
    estoque[lote.codigo].append(lote)

def atualizar_estoque(codigo, nova_quantidade):
    if codigo in estoque:
        estoque[codigo].quantidade = nova_quantidade

def listar_estoque():
    resultado = []
    for lista_lotes in estoque.values():
        atual = lista_lotes._head
        while atual:
            resultado.append(atual.get_element())
            atual = atual.get_next()
    return resultado

def remover_produto(codigo):
    if codigo in estoque:
        del estoque[codigo]

def consultar_todos_produtos():
    todos_lotes = []
    for lista_lotes in estoque.values():
        todos_lotes.extend(list_lotes_para_lista(lista_lotes))
    return todos_lotes

def list_lotes_para_lista(lista_lotes):
    resultado = []
    atual = lista_lotes._head
    while atual:
        resultado.append(atual.get_element())
        atual = atual.get_next()
    return resultado

def consultar_por_codigo(codigo):
    if codigo in estoque:
        return list_lotes_para_lista(estoque[codigo])
    return []

def consultar_por_nome(nome):
    resultados = []
    for lista_lotes in estoque.values():
        atual = lista_lotes._head
        while atual:
            lote = atual.get_element()
            if nome.lower() in lote.nome.lower():
                resultados.append(lote)
            atual = atual.get_next()
    return resultados
