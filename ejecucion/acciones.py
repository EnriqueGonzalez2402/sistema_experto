def mostrar_resultados(resultados):
    print("\n🏆 RESULTADOS:")
    for nombre, prob in resultados[:5]:
        print(f"{nombre} -> {round(prob*100,2)}%")