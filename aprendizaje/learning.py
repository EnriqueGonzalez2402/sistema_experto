import json

def guardar_partida(hechos, resultado):
    data = {"hechos": hechos, "resultado": resultado}

    try:
        with open("aprendizaje/datos.json", "r") as f:
            historial = json.load(f)
    except:
        historial = []

    historial.append(data)

    with open("aprendizaje/datos.json", "w") as f:
        json.dump(historial, f, indent=4)