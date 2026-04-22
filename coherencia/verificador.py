def verificar(personajes):
    errores = []

    for p in personajes:
        if p["genero"] not in ["M", "F"]:
            errores.append(p["nombre"])

    return errores