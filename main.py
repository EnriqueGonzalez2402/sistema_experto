from adquisicion.adquisicion import cargar_personajes
from interfaz.juego import iniciar_juego

def main():
    personajes = cargar_personajes()
    iniciar_juego(personajes)

if __name__ == "__main__":
    main()