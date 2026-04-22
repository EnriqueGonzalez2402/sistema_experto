import json

RUTA = "conocimiento/personajes.json"

def cargar_personajes():
    with open(RUTA, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_personaje(nuevo):
    personajes = cargar_personajes()

    # evitar duplicados
    if any(p["nombre"].lower() == nuevo["nombre"].lower() for p in personajes):
        print("⚠️ Ya conozco ese personaje")
        return

    personajes.append(nuevo)

    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(personajes, f, indent=4, ensure_ascii=False)

    print("\n🧠 Aprendido correctamente!")