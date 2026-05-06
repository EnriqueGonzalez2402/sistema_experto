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

            # BASE
            ("grupo", "¿Es shinigami?", "shinigami"),
            ("grupo", "¿Es arrancar?", "arrancar"),
            ("grupo", "¿Es humano?", "humano"),

            ("capitan", "¿Es capitán?", True),
            ("hollow", "¿Tiene poderes hollow?", True),

            ("arma_distancia", "¿Ataca a distancia?", True),
            ("tipo_poder", "¿Usa espada?", "espada"),
            ("tipo_poder", "¿Usa kido?", "kido"),

            ("genero", "¿Es hombre?", "M"),

            # 🔥 NUEVAS
            ("elemento", "¿Usa hielo?", "hielo"),
            ("elemento", "¿Usa pétalos?", "petalos"),
            ("elemento", "¿Usa fuego?", "fuego"),

            ("arma_tipo", "¿Tiene doble espada?", "doble"),
            ("arma_tipo", "¿Usa guadaña?", "guadana"),

            ("estatus", "¿Es noble?", True),

            ("fisico", "¿Es joven?", "joven"),
            ("fisico", "¿Es robusto?", "robusto"),
            ("fisico", "¿Está enfermo?", "enfermo"),

            ("animal", "¿Tiene temática animal?", True),

            ("estilo", "¿Es más rápido que fuerte?", True),
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
            self.label_info.config(text="Enséñame el personaje")

            self.mostrar_aprendizaje()
   
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
        
        
        
    def mostrar_aprendizaje(self):

        self.btn_si.pack_forget()
        self.btn_no.pack_forget()

        if hasattr(self, "frame_aprender"):
            self.frame_aprender.destroy()

        self.frame_aprender = tk.Frame(self.root, bg="#121212")
        self.frame_aprender.pack(pady=10)

        tk.Label(self.frame_aprender, text="🧠 Nuevo personaje",
                fg="white", bg="#121212").pack()

        tk.Label(self.frame_aprender, text="Nombre:",
                fg="white", bg="#121212").pack()

        self.entry_nombre = tk.Entry(self.frame_aprender)
        self.entry_nombre.pack(pady=5)

        self.vars = {}

        campos = {
            "grupo": ["shinigami", "arrancar", "humano", "vizard"],
            "capitan": [True, False],
            "hollow": [True, False],
            "arma_distancia": [True, False],
            "tipo_poder": ["espada", "kido", "fuerza", "velocidad", "arma"],
            "genero": ["M", "F"]
        }

        for attr, opciones in campos.items():

            if attr in self.hechos:
                continue

            tk.Label(self.frame_aprender, text=attr,
                    fg="white", bg="#121212").pack()

            var = tk.StringVar()
            var.set(str(opciones[0]))
            self.vars[attr] = var

            tk.OptionMenu(
                self.frame_aprender, var,
                *[str(o) for o in opciones]
            ).pack()

        tk.Button(
            self.frame_aprender,
            text="💾 Guardar",
            bg="#4CAF50",
            fg="white",
            command=self.guardar_nuevo_personaje
        ).pack(pady=10)   
    
    def guardar_nuevo_personaje(self):

        nombre = self.entry_nombre.get().strip()

        if not nombre:
            self.label_info.config(text="⚠️ Ingresa nombre")
            return

        # evitar duplicados
        for p in self.personajes:
            if p["nombre"].lower() == nombre.lower():
                self.label_info.config(text="⚠️ Ya existe")
                return

        nuevo = {"nombre": nombre}

        # usar respuestas previas
        for attr, val in self.hechos.items():

            valor, respuesta = val

            if respuesta:
                nuevo[attr] = valor
            else:
                if isinstance(valor, bool):
                    nuevo[attr] = not valor
                else:
                    nuevo[attr] = "otro"

        # completar lo faltante
        for attr, var in self.vars.items():

            valor = var.get()

            if valor == "True":
                valor = True
            elif valor == "False":
                valor = False

            nuevo[attr] = valor

        # estructura base
        base = {
            "grupo": "otro",
            "capitan": False,
            "hollow": False,
            "arma_distancia": False,
            "tipo_poder": "otro",
            "genero": "M"
        }

        for k, v in base.items():
            if k not in nuevo:
                nuevo[k] = v

        from adquisicion.adquisicion import guardar_personaje
        guardar_personaje(nuevo)

        # recargar personajes
        self.personajes = cargar_personajes()

        self.label_pregunta.config(text="✅ Aprendido")
        self.label_info.config(text=nombre)

        self.mostrar_final()
    
# ---------------- MAIN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()