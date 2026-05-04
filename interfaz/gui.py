import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from inferencia.motor import mejor_pregunta, filtrar
from adquisicion.adquisicion import cargar_personajes


class JuegoGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Adivina el personaje - Bleach")
        self.root.geometry("500x600")

        self.personajes = cargar_personajes()
        self.restantes = self.personajes.copy()
        self.hechos = {}

        self.preguntas = [
            ("grupo", "¿Es shinigami?", "shinigami"),
            ("grupo", "¿Es arrancar?", "arrancar"),
            ("grupo", "¿Es humano?", "humano"),
            ("capitan", "¿Es capitán?", True),
            ("hollow", "¿Tiene poderes hollow?", True),
            ("distancia", "¿Ataca a distancia?", True),
            ("poder", "¿Usa espada?", "espada"),
            ("poder", "¿Usa kido?", "kido"),
            ("genero", "¿Es hombre?", "M")
        ]

        # UI
        self.label_pregunta = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
        self.label_pregunta.pack(pady=20)

        self.label_info = tk.Label(root, text="", font=("Arial", 12))
        self.label_info.pack(pady=10)

        # Imagen (placeholder)
        self.img = Image.open("interfaz/placeholder.png")
        self.img = self.img.resize((200, 200))
        self.img_tk = ImageTk.PhotoImage(self.img)

        self.label_img = tk.Label(root, image=self.img_tk)
        self.label_img.pack(pady=10)

        # Botones
        self.btn_si = tk.Button(root, text="Sí", width=10, command=lambda: self.responder(True))
        self.btn_si.pack(side="left", padx=40, pady=20)

        self.btn_no = tk.Button(root, text="No", width=10, command=lambda: self.responder(False))
        self.btn_no.pack(side="right", padx=40, pady=20)

        self.siguiente_pregunta()

    def siguiente_pregunta(self):

        if len(self.restantes) == 0:
            messagebox.showinfo("Error", "No hay coincidencias 😵")
            self.root.quit()
            return

        if len(self.restantes) == 1:
            nombre = self.restantes[0]["nombre"]
            self.label_pregunta.config(text=f"🎯 Es: {nombre}")
            self.label_info.config(text="¡Adiviné!")
            return

        mejor = mejor_pregunta(self.restantes, self.preguntas, self.hechos)

        if not mejor:
            self.label_pregunta.config(text="🤔 No estoy seguro")
            return

        self.atributo, texto, self.valor = mejor

        self.label_pregunta.config(text=texto)
        self.label_info.config(text=f"Quedan {len(self.restantes)} posibles")

    def responder(self, respuesta):

        # marcar como preguntado
        self.hechos[self.atributo] = self.valor if respuesta else f"!= {self.valor}"

        if respuesta:
            self.restantes = filtrar(self.restantes, self.atributo, self.valor)
        else:
            self.restantes = [p for p in self.restantes if p.get(self.atributo) != self.valor]

        self.siguiente_pregunta()


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()