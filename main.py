from adquisicion.adquisicion import cargar_personajes
from coherencia.verificador import verificar
from interfaz.juego import iniciar_juego

def main():
    personajes = cargar_personajes()

    errores = verificar(personajes)

    if errores:
        print("❌ Error en base de conocimiento:", errores)
    else:
        iniciar_juego(personajes)

if __name__ == "__main__":
    main()