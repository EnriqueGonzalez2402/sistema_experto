import math

# ---------------------------
# ENTROPÍA (para preguntas)
# ---------------------------
def entropia(valores):
    total = len(valores)
    if total == 0:
        return 0

    p = sum(valores) / total
    if p == 0 or p == 1:
        return 0

    return -p*math.log2(p) - (1-p)*math.log2(1-p)


def mejor_pregunta(personajes, preguntas, hechos):
    mejor = None
    mejor_gain = -1

    for atributo in preguntas:
        if atributo in hechos:
            continue

        valores = [1 if p[atributo] else 0 for p in personajes]

        h = entropia(valores)

        if h > mejor_gain:
            mejor_gain = h
            mejor = atributo

    return mejor


# ---------------------------
# FILTRADO (reglas)
# ---------------------------
def filtrar(personajes, atributo, valor):
    return [p for p in personajes if p[atributo] == valor]


# ---------------------------
# PROBABILIDAD (ranking)
# ---------------------------
def inferencia_prob(personajes, hechos):

    pesos = {
        "espada": 0.2,
        "capitan": 0.3,
        "hollow": 0.3,
        "genero": 0.2
    }

    resultados = []

    for p in personajes:
        score = 0
        total = 0

        for k, v in hechos.items():
            if k in pesos:
                total += pesos[k]
                if p[k] == v:
                    score += pesos[k]

        prob = score / total if total > 0 else 0.01
        resultados.append((p["nombre"], prob))

    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados