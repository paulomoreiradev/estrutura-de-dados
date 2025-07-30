import json
from datetime import datetime
from produto import LoteProduto
from lists import LinkedList
from validacoes import ProdutoNaoEncontradoError, QuantidadeInvalidaError


estoque = {}

def carregar_dados_iniciais():
    """Carrega dados iniciais de um arquivo JSON"""
    try:
        with open('estoque_inicial.json', 'r') as f:
            dados = json.load(f)

            # Carrega o estoque
            for codigo, lotes in dados['estoque'].items():
                estoque[codigo] = LinkedList()
                for lote_data in lotes:
                    validade = datetime.strptime(lote_data['validade'], '%Y-%m-%d').date() if lote_data['validade'] else None
                    lote = LoteProduto(
                        codigo=lote_data['codigo'],
                        nome=lote_data['nome'],
                        quantidade=lote_data['quantidade'],
                        preco=lote_data['preco'],
                        validade=validade
                    )
                    estoque[codigo].append(lote)

            # Carrega as vendas (se necessário)
            # ...

        print("Dados iniciais carregados com sucesso!")
    except FileNotFoundError:
        print("Arquivo de dados iniciais não encontrado. Iniciando com estoque vazio.")
    except Exception as e:
        print(f"Erro ao carregar dados iniciais: {e}")

# Carrega os dados quando o módulo é importado
carregar_dados_iniciais()

def cadastrar_lote(lote):
    if lote.codigo not in estoque:
        estoque[lote.codigo] = LinkedList()
    estoque[lote.codigo].append(lote)

def atualizar_estoque(codigo, nova_quantidade):
    """
    Atualiza a quantidade em estoque de um produto

    Args:
        codigo (str): Código do produto
        nova_quantidade (int): Nova quantidade em estoque

    Raises:
        ProdutoNaoEncontradoError: Se o produto não existir
        QuantidadeInvalidaError: Se a quantidade for inválida
    """
    if codigo not in estoque:
        raise ProdutoNaoEncontradoError(f"Produto com código {codigo} não encontrado")

    if not isinstance(nova_quantidade, int) or nova_quantidade < 0:
        raise QuantidadeInvalidaError("Quantidade deve ser um inteiro positivo")

    # Atualiza o primeiro lote encontrado (podemos modificar para atualizar todos se necessário)
    lista_lotes = estoque[codigo]
    if lista_lotes._head:  # Verifica se há lotes
        lote = lista_lotes._head.get_element()
        lote.quantidade = nova_quantidade
    else:
        raise ProdutoNaoEncontradoError(f"Nenhum lote encontrado para o produto {codigo}")

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

def remover_produtos_vencidos():
    """
    Remove todos os lotes de produtos vencidos do estoque

    Returns:
        tuple: (quantidade_lotes_removidos, quantidade_itens_removidos)
    """
    lotes_removidos = 0
    itens_removidos = 0

    # Lista temporária para armazenar códigos que ficarão sem lotes
    codigos_para_remover = []

    for codigo, lista_lotes in estoque.items():
        atual = lista_lotes._head
        anterior = None

        while atual:
            lote = atual.get_element()

            if lote.is_vencido():
                # Atualiza contadores
                lotes_removidos += 1
                itens_removidos += lote.quantidade

                # Remove o nó da lista
                if anterior is None:
                    lista_lotes._head = atual.get_next()
                else:
                    anterior.set_next(atual.get_next())

                # Se era o último nó, atualiza a tail
                if atual == lista_lotes._tail:
                    lista_lotes._tail = anterior

                lista_lotes._length -= 1
                atual = atual.get_next() if anterior is None else anterior.get_next()
            else:
                anterior = atual
                atual = atual.get_next()

        # Verifica se a lista de lotes ficou vazia
        if lista_lotes._head is None:
            codigos_para_remover.append(codigo)

    # Remove os códigos que ficaram sem lotes
    for codigo in codigos_para_remover:
        del estoque[codigo]

    return (lotes_removidos, itens_removidos)
