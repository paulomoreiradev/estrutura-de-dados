from datetime import date, datetime

class ValidacaoError(Exception):
    """Classe base para erros de validação"""
    pass

class CodigoInvalidoError(ValidacaoError):
    pass

class PrecoInvalidoError(ValidacaoError):
    pass

class QuantidadeInvalidaError(ValidacaoError):
    pass

class DataInvalidaError(ValidacaoError):
    pass

class ProdutoNaoEncontradoError(ValidacaoError):
    pass

class NomeVazioError(ValidacaoError):
    pass

def validar_codigo(codigo: str) -> str:
    """Valida o código do produto"""
    if not codigo or not codigo.strip():
        raise CodigoInvalidoError("Código não pode ser vazio")
    if len(codigo) > 20:
        raise CodigoInvalidoError("Código muito longo (máx 20 caracteres)")
    if not codigo.isalnum():
        raise CodigoInvalidoError("Código deve conter apenas letras e números")
    return codigo.strip().upper()

def validar_preco(preco: float) -> float:
    """Valida o preço do produto"""
    try:
        preco = float(preco)
    except (ValueError, TypeError):
        raise PrecoInvalidoError("Preço deve ser um número válido")

    if preco <= 0:
        raise PrecoInvalidoError("Preço deve ser positivo")
    return round(preco, 2)

def validar_quantidade(quantidade: int) -> int:
    """Valida a quantidade em estoque"""
    try:
        quantidade = int(quantidade)
    except (ValueError, TypeError):
        raise QuantidadeInvalidaError("Quantidade deve ser um número inteiro")

    if quantidade < 0:
        raise QuantidadeInvalidaError("Quantidade não pode ser negativa")
    return quantidade

def validar_data_validade(data_str: str) -> date:
    """Valida a data de validade"""
    if not data_str:
        return None

    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        raise DataInvalidaError("Formato de data inválido. Use YYYY-MM-DD")

    return data

def input_com_retry(mensagem, funcao_validacao, tipo=str, mensagem_erro="Valor inválido, tente novamente:"):
    """
    Solicita input do usuário com possibilidade de correção em caso de erro

    Args:
        mensagem (str): Mensagem a ser exibida para o usuário
        funcao_validacao (function): Função que valida o input
        tipo (type): Tipo esperado do input (str, int, float, etc)
        mensagem_erro (str): Mensagem a ser exibida em caso de erro

    Returns:
        Valor validado conforme o tipo especificado
    """
    while True:
        try:
            valor = input(mensagem).strip()
            if tipo != str:  # Para tipos não-string, fazemos a conversão
                valor = tipo(valor)
            return funcao_validacao(valor)
        except ValidacaoError as e:
            print(f"\n{mensagem_erro} {e}")
        except (ValueError, TypeError):
            print(f"\n{mensagem_erro} Deve ser do tipo {tipo.__name__}")

def validar_nome(nome: str) -> str:
    """Valida o nome do produto"""
    nome = nome.strip()
    if not nome:
        raise NomeVazioError("O nome do produto não pode ser vazio")
    if len(nome) > 100:
        raise NomeVazioError("O nome do produto é muito longo (máx 100 caracteres)")
    return nome
