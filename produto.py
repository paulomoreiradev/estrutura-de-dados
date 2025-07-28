from datetime import date

class Produto:
    def __init__(self, codigo, nome, quantidade, preco, validade=None):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.validade = validade  # datetime.date ou None

    def is_vencido(self):
        if self.validade:
            return date.today() > self.validade
        return False
