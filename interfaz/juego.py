from inferencia.motor import mejor_pregunta, filtrar, inferencia_prob
from ejecucion.acciones import mostrar_resultados
from adquisicion.adquisicion import guardar_personaje

def iniciar_juego(personajes):

    hechos = {}
    restantes = personajes.copy()
    historial = []

    preguntas = [
        ("grupo", "¿Es shinigami? (s/n): ", "shinigami"),
        ("grupo", "¿Es arrancar? (s/n): ", "arrancar"),
        ("grupo", "¿Es humano? (s/n): ", "humano"),
        ("capitan", "¿Es capitán? (s/n): ", True),
        ("hollow", "¿Tiene poderes hollow? (s/n): ", True),
        ("distancia", "¿Ataca a distancia? (s/n): ", True),
        ("poder", "¿Usa espada? (s/n): ", "espada"),
        ("poder", "¿Usa kido? (s/n): ", "kido"),
        ("genero", "¿Es hombre? (s/n): ", "M")
    ]

    print("🎮 Piensa en un personaje de Bleach...\n")

    while len(restantes) > 1:

        mejor = mejor_pregunta(restantes, preguntas, hechos)

        if not mejor:
            break

        atributo, texto, valor = mejor

        resp = input(texto)
        r = resp.lower() == "s"

        # guardar SI o NO
# 🔥 marcar SIEMPRE como preguntado
        hechos[atributo] = valor if r else f"!= {valor}"

        if r:
            historial.append((atributo, valor))
            restantes = filtrar(restantes, atributo, valor)
        else:
            historial.append((atributo, f"≠ {valor}"))
            restantes = [p for p in restantes if p.get(atributo) != valor]

        print(f"🔎 Quedan {len(restantes)} posibles...")

        # 🚨 contradicción
        if len(restantes) == 0:
            print("\n⚠️ No hay coincidencias.")

            aprender = input("¿Quieres enseñarme el personaje? (s/n): ")

            if aprender.lower() == "s":
                nombre = input("Nombre del personaje: ")

                nuevo = {"nombre": nombre}

                for atributo, texto, valor in preguntas:
                    resp = input(texto)
                    r = resp.lower() == "s"

                    if r:
                        nuevo[atributo] = valor
                    else:
                        if isinstance(valor, bool):
                            nuevo[atributo] = not valor
                        elif atributo == "genero":
                            nuevo[atributo] = "F" if valor == "M" else "M"
                        else:
                            nuevo[atributo] = "otro"

                guardar_personaje(nuevo)

            return

    # 🎯 resultado exacto
    if len(restantes) == 1:
        personaje = restantes[0]["nombre"]

        print(f"\n🎯 El personaje es: {personaje}")

        print("\n🧠 EXPLICACIÓN:")
        for h in historial:
            print(f"- {h[0]} = {h[1]}")

        return

    # fallback probabilístico
    resultados = inferencia_prob(restantes, hechos)
    mostrar_resultados(resultados)