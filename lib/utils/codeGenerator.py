import random

def get_password():
    liste = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefjhigklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    longueur = 10
    code = ""
    cpt = 0

    while cpt < longueur:
        char = liste[random.randint(0, len(liste) - 1)]
        code += char
        cpt += 1

    return code
