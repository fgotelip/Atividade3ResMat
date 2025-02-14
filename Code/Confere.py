import re
import sympy as sp
## Funções para garantir que as inserções do usuário estão corretas
def eh_numero(valor,igual_a_zero=False,menor_que_zero=False): ## Função para verificar se um número é maior que 0
    try:
        valor = float(valor)
        if igual_a_zero:
            if valor < 0: ## Caso o número seja negativo
                print("O valor digitado não é um número positivo.")
                return False
        elif menor_que_zero: ## Caso o número seja zero
            if valor == 0:
                print("O valor digitado não é um número diferente de 0.")
                return False
        elif valor <= 0: ## Caso o número seja zero ou negativo
            print("O valor digitado não é um número positivo diferente de 0.")
            return False
        return True
    except ValueError: ## Caso não seja um número
        print("O valor digitado não é um número.")
        return False

def confere_coordenadas(entrada): ## Função para verificar se uma coordenda foi inserida corretamente
    if not re.fullmatch(r"\s*(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s*",entrada):
        print("As coordenadas digitadas não estão no formato correto.")
        return False
    return True

def eh_sim_nao(valor): ## Função para verificar se o valor é um número
    if valor.lower() in ['s','n']:
        return True
    print("Digite 's' ou 'n'.")
    return False

def eh_123(valor): ## Função para verificar se o valor está no intervalo 1 a 3
    if valor in ['1','2','3']:
        return True
    print("Digite 1, 2 ou 3.")
    return False

def eh_funcao(funcao): ## Função para verificar se a inserção é uma função válida
    try:
        sp.sympify(funcao)
        return True
    except:
        print("A função inserida não é válida")
        return False