from datetime import date
from validacoes import validar_codigo, validar_preco, validar_quantidade, validar_data_validade, validar_nome

class LoteProduto:
    def __init__(self, codigo, nome, quantidade, preco, validade):
        self.codigo = validar_codigo(codigo)
        self.nome = validar_nome(nome)
        self.quantidade = validar_quantidade(quantidade)
        self.preco = validar_preco(preco)
        self.validade = validade  # Já deve vir validado

    def is_vencido(self):
        """Verifica se o produto está vencido"""
        if self.validade is None:
            return False
        return date.today() > self.validade

    def __str__(self):
        validade_str = self.validade.strftime('%d/%m/%Y') if self.validade else "N/A"
        return f"{self.nome} - qtd: {self.quantidade}, validade: {validade_str}, preço: R${self.preco:.2f}"
