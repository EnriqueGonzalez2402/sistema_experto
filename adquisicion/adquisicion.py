import json

def cargar_personajes():
    with open("conocimiento/personajes.json", "r", encoding="utf-8") as f:
        return json.load(f)