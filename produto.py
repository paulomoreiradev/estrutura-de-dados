from datetime import date

class LoteProduto:
    def __init__(self, codigo, nome, quantidade, preco, validade):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.validade = validade  # datetime.date

    def is_vencido(self):
        return date.today() > self.validade

    def __str__(self):
        return f"{self.nome} - qtd: {self.quantidade}, validade: {self.validade}, preço: R${self.preco:.2f}"
