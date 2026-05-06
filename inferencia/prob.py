def inferencia_prob(personajes, hechos):
    resultados = []

    for p in personajes:
        score = 0
        total = 0

        for atributo, (valor, respuesta) in hechos.items():
            if atributo not in p:
                continue

            total += 1

            if respuesta:  # respondió "sí"
                if p[atributo] == valor:
                    score += 1
            else:  # respondió "no"
                if p[atributo] != valor:
                    score += 1

        prob = (score / total) if total > 0 else 0
        resultados.append((p["nombre"], prob))

    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados