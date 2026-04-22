from inferencia.motor import mejor_pregunta, filtrar, inferencia_prob
from ejecucion.acciones import mostrar_resultados

def iniciar_juego(personajes):
    hechos = {}
    restantes = personajes.copy()

    preguntas = {
        "espada": "¿Tiene espada? (s/n): ",
        "capitan": "¿Es capitán? (s/n): ",
        "hollow": "¿Tiene poderes hollow? (s/n): ",
        "genero": "¿Es hombre? (s/n): "
    }

    print("🎮 Piensa en un personaje de Bleach...\n")

    while len(restantes) > 1:
        pregunta = mejor_pregunta(restantes, preguntas, hechos)

        if not pregunta:
            break

        resp = input(preguntas[pregunta])

        if pregunta == "genero":
            valor = "M" if resp.lower() == "s" else "F"
        else:
            valor = True if resp.lower() == "s" else False

        hechos[pregunta] = valor
        restantes = filtrar(restantes, pregunta, valor)

        print(f"🔎 Quedan {len(restantes)} posibles...")

    
    print("DEBUG len inicial:", len(restantes))
    resultados = inferencia_prob(restantes, hechos)
    mostrar_resultados(resultados)