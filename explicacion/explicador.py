print("\n🧠 EXPLICACIÓN:")
for attr, val in historial:
    if "≠" in str(val):
        print(f"- {attr} no es {val.replace('≠ ', '')}")
    else:
        print(f"- {attr} = {val}")