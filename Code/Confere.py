import re
import sympy as sp
def eh_numero_pos(valor,igual_a_zero=False):
    try:
        valor = float(valor)
        if igual_a_zero:
            if valor < 0:
                print("O valor digitado não é um número positivo.")
                return False
        elif valor <= 0:
            print("O valor digitado não é um número positivo diferente de 0.")
            return False
        return True
    except ValueError:
        print("O valor digitado não é um número.")
        return False
    
def confere_coordenadas(entrada):
    if not re.fullmatch(r"\s*(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s*",entrada):
        print("As coordenadas digitadas não estão no formato correto.")
        return False
    return True

def eh_sim_nao(valor):
    if valor.lower() in ['s','n']:
        return True
    print("Digite 's' ou 'n'.")
    return False

def eh_123(valor):
    if valor in ['1','2','3']:
        return True
    print("Digite 1, 2 ou 3.")
    return False

def eh_funcao(funcao):
    try:
        sp.sympify(funcao)
        return True
    except:
        print("A função inserida não é válida.")
        return False
