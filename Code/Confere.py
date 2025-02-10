import re
def eh_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        print("O valor digitado não é um número.")
        return False

def eh_inteiro(valor):
    try:
        int(valor)
        if int(valor) <= 0:
            print("O valor digitado não é um número inteiro positivo.")
            return False
        return True
    except ValueError:
        print("O valor digitado não é um número inteiro.")
        return False
    
def confere_coordenadas(entrada):
    if not re.fullmatch(r"\s*(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s*",entrada):
        print("As coordenadas digitadas não estão no formato correto.")
        return False
    return True

def eh_sim_nao(valor):
    if valor.lower() in ['s','n']:
        return True
    print("Digite 's' ou 'n'.")
    return False