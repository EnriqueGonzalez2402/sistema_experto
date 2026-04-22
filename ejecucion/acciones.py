def mostrar_resultados(resultados):
    print("\n🏆 RESULTADOS:")
    for nombre, prob in resultados:
        print(f"{nombre} -> {round(prob*100,2)}%")