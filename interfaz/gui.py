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

        # ❌ sin coincidencias
        if len(self.restantes) == 0:
            self.label_pregunta.config(text="⚠️ No hay coincidencias")
            self.label_info.config(text="Respuestas inconsistentes")
            self.mostrar_final()
            return

        # 🎯 éxito
        if len(self.restantes) == 1:
            nombre = self.restantes[0]["nombre"]

            self.label_pregunta.config(text=f"🎯 ¡Es {nombre}!")
            self.label_info.config(text="🧠 Inferencia completada")

            self.cargar_imagen(f"{nombre.lower()}.png")
            self.progress['value'] = 100

            self.mostrar_final()
            return

        mejor = mejor_pregunta(self.restantes, self.preguntas, self.hechos)

        # 🤔 inferencia
        if not mejor:
            resultados = inferencia_prob(self.restantes, self.hechos)
            self.mostrar_resultados(resultados)
            return

        self.atributo, texto, self.valor = mejor

        self.label_pregunta.config(text="🤖 Pensando...")
        self.root.update()
        self.root.after(300)

        self.label_pregunta.config(text=texto)
        self.label_info.config(text=f"Quedan {len(self.restantes)} posibles")
        self.label_progress.config(text=f"Preguntas: {len(self.hechos)}")

        self.progress['value'] = (len(self.hechos) / len(self.preguntas)) * 100

    def responder(self, respuesta):

        self.hechos[self.atributo] = (self.valor, respuesta)

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

        self.mostrar_final()

    # ---------------- FINAL ----------------

    def mostrar_final(self):

        # desactivar botones
        self.btn_si.pack_forget()
        self.btn_no.pack_forget()

        # limpiar espacio inferior si ya existe
        if hasattr(self, "frame_final"):
            self.frame_final.destroy()

        # contenedor final
        self.frame_final = tk.Frame(self.root, bg="#121212")
        self.frame_final.pack(side="bottom", pady=30)

        # título opcional
        label = tk.Label(
            self.frame_final,
            text="¿Qué quieres hacer?",
            font=("Arial", 12),
            fg="white",
            bg="#121212"
        )
        label.pack(pady=10)

        # botones
        btn_reset = tk.Button(
            self.frame_final,
            text="🔄 Jugar otra vez",
            width=18,
            height=2,
            bg="#2196F3",
            fg="white",
            command=self.reiniciar
        )
        btn_reset.pack(pady=5)

        btn_exit = tk.Button(
            self.frame_final,
            text="❌ Salir",
            width=18,
            height=2,
            bg="#555",
            fg="white",
            command=self.root.quit
        )
        btn_exit.pack(pady=5)
    def reiniciar(self):

        # reset lógico
        self.restantes = self.personajes.copy()
        self.hechos = {}

        # limpiar toda la interfaz
        for widget in self.root.winfo_children():
            widget.destroy()

        # reconstruir todo
        self.__init__(self.root)
# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()