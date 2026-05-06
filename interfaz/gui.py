import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from inferencia.prob import inferencia_prob
from inferencia.motor import mejor_pregunta, filtrar
from adquisicion.adquisicion import cargar_personajes


class JuegoGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Adivina el personaje - Bleach")
        self.root.geometry("520x650")
        self.root.configure(bg="#121212")

        self.personajes = cargar_personajes()
        self.restantes = self.personajes.copy()
        self.hechos = {}

        # 🔥 PREGUNTAS CORREGIDAS (alineadas con JSON)
        self.preguntas = [
            ("grupo", "¿Es shinigami?", "shinigami"),
            ("grupo", "¿Es arrancar?", "arrancar"),
            ("grupo", "¿Es humano?", "humano"),
            ("capitan", "¿Es capitán?", True),
            ("hollow", "¿Tiene poderes hollow?", True),
            ("arma_distancia", "¿Ataca a distancia?", True),
            ("tipo_poder", "¿Usa espada?", "espada"),
            ("tipo_poder", "¿Usa kido?", "kido"),
            ("genero", "¿Es hombre?", "M")
        ]

        # ---------------- UI ----------------

        self.label_pregunta = tk.Label(
            root, text="", font=("Arial", 20, "bold"),
            fg="white", bg="#121212", wraplength=450
        )
        self.label_pregunta.pack(pady=20)

        self.label_info = tk.Label(
            root, text="", font=("Arial", 12),
            fg="gray", bg="#121212"
        )
        self.label_info.pack()

        self.label_progress = tk.Label(
            root, text="", font=("Arial", 10),
            fg="lightgray", bg="#121212"
        )
        self.label_progress.pack()

        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.label_img = tk.Label(root, bg="#121212")
        self.label_img.pack(pady=20)

        self.cargar_imagen("placeholder.png")

        frame = tk.Frame(root, bg="#121212")
        frame.pack(pady=30)

        self.btn_si = tk.Button(
            frame, text="SÍ", width=12, height=2,
            bg="#4CAF50", fg="white",
            command=lambda: self.responder(True)
        )
        self.btn_si.pack(side="left", padx=20)

        self.btn_no = tk.Button(
            frame, text="NO", width=12, height=2,
            bg="#f44336", fg="white",
            command=lambda: self.responder(False)
        )
        self.btn_no.pack(side="right", padx=20)

        self.siguiente_pregunta()

    # ---------------- IMAGEN ----------------

    def cargar_imagen(self, nombre):
        try:
            base = os.path.dirname(__file__)
            ruta = os.path.join(base, "imagenes", nombre)
            img = Image.open(ruta)
        except:
            img = Image.new("RGB", (300, 300), "gray")

        img = img.resize((300, 300))
        self.img_tk = ImageTk.PhotoImage(img)
        self.label_img.config(image=self.img_tk)

    # ---------------- LOGICA ----------------

    def siguiente_pregunta(self):

        # ❌ contradicción real
        if len(self.restantes) == 0:
            self.label_pregunta.config(text="⚠️ No hay coincidencias")
            self.label_info.config(text="Respuestas inconsistentes")
            return

        # 🎯 caso ideal
        if len(self.restantes) == 1:
            nombre = self.restantes[0]["nombre"]

            self.label_pregunta.config(text=f"🎯 ¡Es {nombre}!")
            self.label_info.config(text="🧠 Inferencia completada")

            self.cargar_imagen(f"{nombre.lower()}.png")
            self.progress['value'] = 100
            return

        # 🔍 seleccionar mejor pregunta
        mejor = mejor_pregunta(self.restantes, self.preguntas, self.hechos)

        # 🤔 sin más preguntas → inferencia probabilística
        if not mejor:
            resultados = inferencia_prob(self.restantes, self.hechos)
            self.mostrar_resultados(resultados)
            return

        self.atributo, texto, self.valor = mejor

        # animación simple
        self.label_pregunta.config(text="🤖 Pensando...")
        self.root.update()
        self.root.after(300)

        self.label_pregunta.config(text=texto)
        self.label_info.config(text=f"Quedan {len(self.restantes)} posibles")
        self.label_progress.config(text=f"Preguntas: {len(self.hechos)}")

        self.progress['value'] = (len(self.hechos) / len(self.preguntas)) * 100

    def responder(self, respuesta):

        # ✅ guardar correctamente el hecho
        self.hechos[self.atributo] = (self.valor, respuesta)

        # 🔍 filtrar
        if respuesta:
            self.restantes = filtrar(self.restantes, self.atributo, self.valor)
        else:
            self.restantes = [
                p for p in self.restantes
                if p.get(self.atributo) != self.valor
            ]

        self.siguiente_pregunta()

    # ---------------- RESULTADOS ----------------

    def mostrar_resultados(self, resultados):

        self.label_pregunta.config(text="🧠 RESULTADOS")
        self.label_info.config(text="Top candidatos")

        texto = ""

        for nombre, prob in resultados[:5]:
            texto += f"{nombre}: {round(prob*100)}%\n"

        self.label_progress.config(text=texto)

        if resultados:
            mejor = resultados[0][0]
            self.cargar_imagen(f"{mejor.lower()}.png")


# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()