import math

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
    mejor_entropia = -1

    for atributo, texto, valor in preguntas:

        if atributo in hechos:
            continue

        valores = [1 if p.get(atributo) == valor else 0 for p in personajes]

        h = entropia(valores)

        if h > mejor_entropia:
            mejor_entropia = h
            mejor = (atributo, texto, valor)

    return mejor


def filtrar(personajes, atributo, valor):
    return [p for p in personajes if p.get(atributo) == valor]


def inferencia_prob(personajes, hechos):

    resultados = []

    for p in personajes:
        score = 0
        total = len(hechos)

        for k, v in hechos.items():
            if p.get(k) == v:
                score += 1

        prob = score / total if total > 0 else 0
        resultados.append((p["nombre"], prob))

    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados