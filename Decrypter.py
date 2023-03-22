# Made with Python 3.10.3 for VSCode Version: 1.76.2 (user setup)

import numpy as np
from colored import fg, attr


# Función que calcula el fitness score de cada quadgram
def calc_score(text, quadgrams):
    text = "".join(text)
    score = 0
    quads = quadgrams.__getitem__
    for i in range(len(text) - 3):
        if text[i : i + 4] in quadgrams:
            score += quads(text[i : i + 4])
        else:
            score += floor
    return round(score, 3)


# Se crea diccionario con cada uno de los quadgrams en el inglés y su respectiva frecuencia
quadgrams = {}
for line in open("english_quadgrams.txt"):
    quad, num = line.split(" ")
    quadgrams[quad] = int(num)

# Se calcula la probabilidad logarítmica de cada quadgram
n = len(quadgrams.values())
for quad in quadgrams.keys():
    quadgrams[quad] = np.log10(quadgrams[quad] / n)
floor = np.log10(0.01 / n)

# Se le pide al usuario la frase a desencriptar
original_text = input("Enter crypted text:\n")
text = original_text.upper()
print("\x1B[s")

# Se crea lista con el alfabeto en inglés y la primera clave
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
initial_key = alphabet[:]

# Se explora el texto para encontrar caracteres especiales, estos se extraen y
# se guardan en una lista con su respectivo index
special_chars = []
count = 0
for char in text:
    if char not in alphabet:
        special_chars.append((char, text.index(char) + count))
        text = text.replace(char, "", 1)
        count += 1

# Se asignan los valores iniciales del puntaje del texto encriptado,
# el puntaje de validación y se le da un valor muy pequeño al
# valor final para hacer una validación adecuada con los puntajes
# obtenidos en cada iteración
initial_score, valid_score, final_score = calc_score(list(text), quadgrams), None, -99e9

# Valores iniciales del padre para el algoritmo genético
np.random.shuffle(initial_key)
parent_key, parent_guess = initial_key[:], []

reset = fg(15) + attr(0)
no_changes = 0
current_gen = 0

# Inicializamos el algoritmo genético
while 1:
    current_gen += 1

    # Se obtiene la clave del padre y el fitness score de su predicción
    for char in text:
        idx = alphabet.index(char)
        parent_guess.append(parent_key[idx])
    parent_score = calc_score(parent_guess, quadgrams)

    # Inicializamos el ciclo para calcular los valores de los hijos
    count = 0
    while count < 310:
        a = np.random.randint(0, len(alphabet))
        b = np.random.randint(0, len(alphabet))

        # Se obtiene la clave del hijo y el fitness score de su predicción
        child_key, child_guess = parent_key[:], []
        child_key[a], child_key[b] = child_key[b], child_key[a]

        for char in text:
            idx = alphabet.index(char)
            child_guess.append(child_key[idx])
        child_score = calc_score(child_guess, quadgrams)

        # Se evalúa si el puntaje del hijo es mayor al del padre. En caso
        # de ser así, se establece el hijo como nuevo padre el cual empieza
        # una nueva genereación de hijos
        if child_score > parent_score:
            parent_score, parent_key, parent_guess = (
                child_score,
                child_key[:],
                child_guess[:],
            )
            count = 0
            current_gen += 1

            # Se evalúa si el puntaje del nuevo padre es mayor al valor final. Si esto se
            # cumple, se establecen los valores del nuevo padre como los mejores valores
            if parent_score > final_score:
                best_gen, final_score, best_key, best_guess = (
                    current_gen,
                    parent_score,
                    parent_key[:],
                    parent_guess[:],
                )

            # Se imprimen los resultados de cada generación del nuevo padre
            print(
                f"\x1B[0JCurrent generation: {fg(4)}{attr(1)}{current_gen}{reset} - Score: {fg(1)}{attr(1)}{final_score}{reset}\nGuessed text: {fg(243)}{attr(1)}{''.join(best_guess)}{reset}\x1B[u"
            )
        else:
            count += 1

    # Se evalúa si el puntaje del padre es mayor al valor final. Si esto se
    # cumple, se establecen los valores del padre como los mejores valores
    if parent_score > final_score:
        best_gen, final_score, best_key, best_guess = (
            current_gen,
            parent_score,
            parent_key[:],
            parent_guess[:],
        )

    # Se evalúa si el puntaje final es igual al puntaje de validación. En caso
    # de que se cumpla, se acumula la iteración ya que se define que cuando el
    # puntaje no haya cambiado durante 113 veces seguidas, el mensaje fue
    # desencriptado satisfactoriamente y se rompe el ciclo
    if final_score == valid_score:
        no_changes += 1
        if no_changes == 113:
            break
    else:
        no_changes = 0

    valid_score = final_score

    # Se imprimen los resultados de cada generación
    print(
        f"\x1B[0JCurrent generation: {fg(4)}{attr(1)}{current_gen}{reset} - Score: {fg(1)}{attr(1)}{final_score}{reset}\nGuessed text: {fg(243)}{attr(1)}{''.join(best_guess)}{reset}\x1B[u"
    )

# Se agregan los caracteres especiales que fueron retirados del mensaje
for char in special_chars:
    special_char, idx = char
    best_guess.insert(idx, special_char)

# Se agregan las mayúsculas en las posiciones adecuadas
for i in range(len(original_text)):
    if not original_text[i].isupper():
        best_guess[i] = best_guess[i].lower()

best_guess = "".join(best_guess)
max_score = final_score - initial_score

# Se imprimen los resultados finales
print(
    f"""\x1B[3E\nDecrypted in Generation {fg(2)}{attr(1)}{best_gen}{reset} with a Fitness Score increase of {fg(2)}{attr(1)}{max_score}{reset} points
    Initial Score: {fg(208)}{initial_score}{reset} - Final Score: {fg(3)}{final_score}{reset}
    Key: {fg(4)}{''.join(alphabet)}{reset}
         ˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅
         {fg(6)}{attr(1)}{''.join(best_key)}{reset}
    Crypted text: {fg(1)}{original_text}{reset}
  Decrypted text: {fg(2)}{best_guess}{reset}""",
)
