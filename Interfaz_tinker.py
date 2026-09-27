import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk

import Datos
from Entidades import Candidato


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, icon, command, bg_color="#1f6feb", hover_color="#0d5ad7", width=250, height=64):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.command = command

        self.round_rect = self.create_rectangle(
            6, 6, width - 6, height - 6,
            fill=bg_color,
            outline="",
            tags="button"
        )

        self.icon_bg = self.create_oval(
            18, 18, 54, 54,
            fill="white",
            outline="white"
        )

        self.create_text(
            36,
            36,
            text=icon,
            font=("Segoe UI Emoji", 18),
            fill=bg_color,
            anchor="center"
        )

        self.create_text(
            72,
            36,
            text=text,
            font=("Arial", 11, "bold"),
            fill="white",
            anchor="w"
        )

        self.bind("<Button-1>", lambda event: self.command())
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.itemconfig(self.round_rect, fill=self.hover_color)
        self.itemconfig(self.icon_bg, fill="#f8fbff")

    def on_leave(self, event):
        self.itemconfig(self.round_rect, fill=self.bg_color)
        self.itemconfig(self.icon_bg, fill="white")


class WorkerLocationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Worker Location")
        self.geometry("700x760")
        self.configure(bg="#edf3ff")
        self.resizable(False, False)

        self._crear_encabezado()
        self._crear_logo()
        self._crear_menu()

    def _crear_encabezado(self):
        header = tk.Frame(self, bg="#edf3ff")
        header.pack(pady=(18, 4))

        tk.Label(
            header,
            text="Worker Location",
            font=("Arial", 24, "bold"),
            bg="#edf3ff",
            fg="#123d6b"
        ).pack()

        tk.Label(
            header,
            text="Sistema de gestión de candidatos",
            font=("Arial", 10),
            bg="#edf3ff",
            fg="#5a6c83"
        ).pack(pady=(2, 0))

    def _crear_logo(self):
        try:
            imagen = Image.open("logo.png")
            imagen = imagen.resize((150, 150))
            self.logo = ImageTk.PhotoImage(imagen)
            tk.Label(
                self,
                image=self.logo,
                bg="#edf3ff"
            ).pack(pady=(8, 12))
        except FileNotFoundError:
            tk.Label(
                self,
                text="WORKER LOCATION",
                font=("Arial", 22, "bold"),
                bg="#edf3ff",
                fg="#0d3b66"
            ).pack(pady=(8, 12))

    def _crear_menu(self):
        frame = tk.Frame(self, bg="#edf3ff")
        frame.pack(fill="x", padx=18, pady=8)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        botones = [
            ("Registrar", "＋", self.abrir_formulario_registro, "#1f6feb"),
            ("Buscar", "⌕", self.buscar_gui, "#2e8b57"),
            ("Actualizar", "✎", self.actualizar_gui, "#f39c12"),
            ("Eliminar", "🗑", self.eliminar_gui, "#e74c3c"),
            ("Mejor candidato", "★", self.buscar_mejor_candidato_gui, "#8e44ad"),
            ("Salir", "⎋", self.cerrar, "#d9534f"),
        ]

        for index, (texto, icono, comando, color) in enumerate(botones):
            fila = index // 2
            columna = index % 2
            hover = {
                "#1f6feb": "#0d5ad7",
                "#2e8b57": "#1f6a46",
                "#f39c12": "#d58500",
                "#e74c3c": "#c0392b",
                "#8e44ad": "#6d3e93",
                "#d9534f": "#be3a2d",
            }[color]

            boton = RoundedButton(
                frame,
                text=texto,
                icon=icono,
                command=comando,
                bg_color=color,
                hover_color=hover,
                width=250,
                height=64,
            )
            boton.grid(row=fila, column=columna, padx=8, pady=8, sticky="nsew")

    def abrir_formulario_registro(self):
        ventana_form = tk.Toplevel(self)
        ventana_form.title("Registrar candidato")
        ventana_form.geometry("420x420")
        ventana_form.config(bg="#f4f8ff")
        ventana_form.resizable(False, False)

        tk.Label(ventana_form, text="Registrar candidato", font=("Arial", 18, "bold"), bg="#f4f8ff", fg="#153d6b").pack(pady=(18, 10))

        campos = [
            ("ID del candidato", "id"),
            ("Nombre", "nombre"),
            ("Profesión", "profesion"),
            ("Años de experiencia", "experiencia"),
            ("Habilidades", "habilidades"),
        ]

        entradas = {}
        for texto, clave in campos:
            frame = tk.Frame(ventana_form, bg="#f4f8ff")
            frame.pack(fill="x", padx=25, pady=6)
            tk.Label(frame, text=texto, font=("Arial", 10, "bold"), bg="#f4f8ff", anchor="w").pack(anchor="w")
            entry = tk.Entry(frame, font=("Arial", 10))
            entry.pack(fill="x")
            entradas[clave] = entry

        def guardar():
            try:
                id_cand = int(entradas["id"].get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.", parent=ventana_form)
                return

            nombre = entradas["nombre"].get().strip()
            profesion = entradas["profesion"].get().strip()
            experiencia = entradas["experiencia"].get().strip()
            habilidades = entradas["habilidades"].get().strip()

            if not nombre or not profesion or not experiencia or not habilidades:
                messagebox.showerror("Error", "Complete todos los campos.", parent=ventana_form)
                return

            try:
                experiencia_int = int(experiencia)
            except ValueError:
                messagebox.showerror("Error", "La experiencia debe ser un número entero.", parent=ventana_form)
                return

            for candidato in Datos.lista_candidatos:
                if candidato.id_candidato == id_cand:
                    messagebox.showerror("Error", "Ya existe un candidato con ese ID.", parent=ventana_form)
                    return

            nuevo_candidato = Candidato(id_cand, nombre, profesion, experiencia_int, habilidades)
            Datos.lista_candidatos.append(nuevo_candidato)
            messagebox.showinfo("Éxito", "¡Candidato guardado exitosamente!", parent=ventana_form)
            ventana_form.destroy()

        tk.Button(
            ventana_form,
            text="Guardar candidato",
            command=guardar,
            bg="#1f6feb",
            fg="white",
            font=("Arial", 10, "bold"),
            width=24,
            pady=8,
            bd=0,
            cursor="hand2"
        ).pack(pady=(18, 10))

    def registrar_gui(self):
        self.abrir_formulario_registro()

    def buscar_gui(self):
        if not Datos.lista_candidatos:
            messagebox.showwarning("Advertencia", "No hay candidatos registrados.")
            return

        ventana_buscar = tk.Toplevel(self)
        ventana_buscar.title("Buscar candidato")
        ventana_buscar.geometry("360x180")
        ventana_buscar.config(bg="#f4f8ff")

        tk.Label(ventana_buscar, text="Buscar candidato por ID", font=("Arial", 16, "bold"), bg="#f4f8ff", fg="#153d6b").pack(pady=(18, 10))

        frame = tk.Frame(ventana_buscar, bg="#f4f8ff")
        frame.pack(fill="x", padx=25)
        tk.Label(frame, text="ID del candidato:", bg="#f4f8ff", font=("Arial", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, font=("Arial", 10))
        entry.pack(fill="x", pady=(4, 12))

        def consultar():
            try:
                id_buscar = int(entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.", parent=ventana_buscar)
                return

            for candidato in Datos.lista_candidatos:
                if candidato.id_candidato == id_buscar:
                    info = (
                        f"ID: {candidato.id_candidato}\n"
                        f"Nombre: {candidato.nombre}\n"
                        f"Profesión: {candidato.profesion}\n"
                        f"Experiencia: {candidato.experiencia} años\n"
                        f"Habilidades: {candidato.habilidades}"
                    )
                    messagebox.showinfo("Candidato encontrado", info, parent=ventana_buscar)
                    ventana_buscar.destroy()
                    return

            messagebox.showerror("Error", "Candidato no encontrado.", parent=ventana_buscar)

        tk.Button(
            ventana_buscar,
            text="Buscar",
            command=consultar,
            bg="#2e8b57",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            pady=7,
            bd=0,
            cursor="hand2"
        ).pack(pady=8)

    def actualizar_gui(self):
        if not Datos.lista_candidatos:
            messagebox.showwarning("Advertencia", "No hay candidatos registrados.")
            return

        ventana_actualizar = tk.Toplevel(self)
        ventana_actualizar.title("Actualizar candidato")
        ventana_actualizar.geometry("420x420")
        ventana_actualizar.config(bg="#f4f8ff")

        tk.Label(ventana_actualizar, text="Actualizar candidato", font=("Arial", 18, "bold"), bg="#f4f8ff", fg="#153d6b").pack(pady=(18, 10))

        frame = tk.Frame(ventana_actualizar, bg="#f4f8ff")
        frame.pack(fill="x", padx=25, pady=6)
        tk.Label(frame, text="ID del candidato a actualizar:", font=("Arial", 10, "bold"), bg="#f4f8ff").pack(anchor="w")
        entry_id = tk.Entry(frame, font=("Arial", 10))
        entry_id.pack(fill="x")

        def cargar_formulario():
            try:
                id_buscar = int(entry_id.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.", parent=ventana_actualizar)
                return

            candidato = None
            for item in Datos.lista_candidatos:
                if item.id_candidato == id_buscar:
                    candidato = item
                    break

            if candidato is None:
                messagebox.showerror("Error", "Candidato no encontrado.", parent=ventana_actualizar)
                return

            ventana_form = tk.Toplevel(ventana_actualizar)
            ventana_form.title("Editar datos")
            ventana_form.geometry("420x420")
            ventana_form.config(bg="#f4f8ff")

            campos = [
                ("Nombre", candidato.nombre),
                ("Profesión", candidato.profesion),
                ("Años de experiencia", str(candidato.experiencia)),
                ("Habilidades", candidato.habilidades),
            ]
            entradas = {}

            for texto, valor in campos:
                sub = tk.Frame(ventana_form, bg="#f4f8ff")
                sub.pack(fill="x", padx=25, pady=6)
                tk.Label(sub, text=texto, font=("Arial", 10, "bold"), bg="#f4f8ff").pack(anchor="w")
                entry = tk.Entry(sub, font=("Arial", 10))
                entry.insert(0, valor)
                entry.pack(fill="x")
                entradas[texto] = entry

            def guardar_campos():
                nombre = entradas["Nombre"].get().strip()
                profesion = entradas["Profesión"].get().strip()
                experiencia_texto = entradas["Años de experiencia"].get().strip()
                habilidades = entradas["Habilidades"].get().strip()

                if not nombre or not profesion or not experiencia_texto or not habilidades:
                    messagebox.showerror("Error", "Complete todos los campos.", parent=ventana_form)
                    return

                try:
                    experiencia_int = int(experiencia_texto)
                except ValueError:
                    messagebox.showerror("Error", "La experiencia debe ser un número entero.", parent=ventana_form)
                    return

                candidato.nombre = nombre
                candidato.profesion = profesion
                candidato.experiencia = experiencia_int
                candidato.habilidades = habilidades
                messagebox.showinfo("Éxito", "¡Candidato actualizado exitosamente!", parent=ventana_form)
                ventana_form.destroy()
                ventana_actualizar.destroy()

            tk.Button(
                ventana_form,
                text="Guardar cambios",
                command=guardar_campos,
                bg="#f39c12",
                fg="white",
                font=("Arial", 10, "bold"),
                width=22,
                pady=8,
                bd=0,
                cursor="hand2"
            ).pack(pady=(18, 10))

        tk.Button(
            ventana_actualizar,
            text="Continuar",
            command=cargar_formulario,
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            pady=7,
            bd=0,
            cursor="hand2"
        ).pack(pady=10)

    def eliminar_gui(self):
        if not Datos.lista_candidatos:
            messagebox.showwarning("Advertencia", "No hay candidatos registrados.")
            return

        ventana_eliminar = tk.Toplevel(self)
        ventana_eliminar.title("Eliminar candidato")
        ventana_eliminar.geometry("360x180")
        ventana_eliminar.config(bg="#f4f8ff")

        tk.Label(ventana_eliminar, text="Eliminar candidato", font=("Arial", 16, "bold"), bg="#f4f8ff", fg="#153d6b").pack(pady=(18, 10))

        frame = tk.Frame(ventana_eliminar, bg="#f4f8ff")
        frame.pack(fill="x", padx=25)
        tk.Label(frame, text="ID del candidato:", bg="#f4f8ff", font=("Arial", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, font=("Arial", 10))
        entry.pack(fill="x", pady=(4, 10))

        def borrar():
            try:
                id_eliminar = int(entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.", parent=ventana_eliminar)
                return

            for i, candidato in enumerate(Datos.lista_candidatos):
                if candidato.id_candidato == id_eliminar:
                    if messagebox.askyesno("Confirmar", f"¿Desea eliminar a {candidato.nombre}?"):
                        eliminado = Datos.lista_candidatos.pop(i)
                        messagebox.showinfo("Éxito", f"El candidato {eliminado.nombre} ha sido eliminado.", parent=ventana_eliminar)
                        ventana_eliminar.destroy()
                    return

            messagebox.showerror("Error", "Candidato no encontrado.", parent=ventana_eliminar)

        tk.Button(
            ventana_eliminar,
            text="Eliminar",
            command=borrar,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            pady=7,
            bd=0,
            cursor="hand2"
        ).pack(pady=8)

    def buscar_mejor_candidato_gui(self):
        if not Datos.lista_candidatos:
            messagebox.showwarning("Advertencia", "No hay candidatos registrados.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Mejor candidato")
        ventana.geometry("420x360")
        ventana.config(bg="#f4f8ff")

        tk.Label(ventana, text="Buscar mejor candidato", font=("Arial", 18, "bold"), bg="#f4f8ff", fg="#153d6b").pack(pady=(18, 12))

        campos = [
            ("Profesión requerida", "profesion"),
            ("Experiencia mínima", "experiencia"),
            ("Habilidades requeridas", "habilidades"),
        ]

        entradas = {}
        for texto, clave in campos:
            frame = tk.Frame(ventana, bg="#f4f8ff")
            frame.pack(fill="x", padx=25, pady=6)
            tk.Label(frame, text=texto, bg="#f4f8ff", font=("Arial", 10, "bold")).pack(anchor="w")
            entry = tk.Entry(frame, font=("Arial", 10))
            entry.pack(fill="x")
            entradas[clave] = entry

        def buscar():
            profesion_requerida = entradas["profesion"].get().strip()
            experiencia_texto = entradas["experiencia"].get().strip()
            habilidades_requeridas = entradas["habilidades"].get().strip()

            if not profesion_requerida or not experiencia_texto or not habilidades_requeridas:
                messagebox.showerror("Error", "Complete todos los campos.", parent=ventana)
                return

            try:
                experiencia_minima = int(experiencia_texto)
            except ValueError:
                messagebox.showerror("Error", "La experiencia debe ser un número entero.", parent=ventana)
                return

            habilidades_requeridas = [
                habilidad.strip().lower()
                for habilidad in habilidades_requeridas.split(",")
            ]

            resultados = []
            for candidato in Datos.lista_candidatos:
                puntos = 0

                if candidato.profesion.lower() == profesion_requerida.lower():
                    puntos += 50

                if candidato.experiencia >= experiencia_minima:
                    puntos += 30

                habilidades_candidato = [
                    habilidad.strip().lower()
                    for habilidad in candidato.habilidades.split(",")
                ]

                coincidencias = 0
                for habilidad in habilidades_requeridas:
                    if habilidad in habilidades_candidato:
                        coincidencias += 1

                puntos += coincidencias * 10

                if puntos > 0:
                    resultados.append((puntos, candidato))

            resultados.sort(key=lambda resultado: resultado[0], reverse=True)

            if not resultados:
                messagebox.showinfo("Resultado", "No se encontraron candidatos compatibles.", parent=ventana)
                return

            mensaje = "Top candidatos:\n\n"
            for puntos, candidato in resultados[:3]:
                mensaje += (
                    f"{candidato.nombre} - {candidato.profesion} - "
                    f"{candidato.experiencia} años - {puntos} puntos\n"
                )

            messagebox.showinfo("Resultado", mensaje, parent=ventana)

        tk.Button(
            ventana,
            text="Buscar mejor candidato",
            command=buscar,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            pady=8,
            bd=0,
            cursor="hand2"
        ).pack(pady=(16, 10))

    def ver_candidatos_gui(self):
        ventana = tk.Toplevel(self)
        ventana.title("Lista de candidatos")
        ventana.geometry("780x420")
        ventana.config(bg="#f4f8ff")

        columns = ("ID", "Nombre", "Profesión", "Experiencia", "Habilidades")
        tree = ttk.Treeview(ventana, columns=columns, show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Profesión", text="Profesión")
        tree.heading("Experiencia", text="Experiencia")
        tree.heading("Habilidades", text="Habilidades")

        for col in columns:
            tree.column(col, width=120, anchor="center")

        for candidato in Datos.lista_candidatos:
            tree.insert(
                "",
                "end",
                values=(
                    candidato.id_candidato,
                    candidato.nombre,
                    candidato.profesion,
                    candidato.experiencia,
                    candidato.habilidades,
                )
            )

        tree.pack(fill="both", expand=True, padx=12, pady=12)

    def mostrar_total_gui(self):
        total = len(Datos.lista_candidatos)
        messagebox.showinfo(
            "Total de candidatos",
            f"Actualmente hay {total} candidato(s) registrado(s) en el sistema."
        )

    def cerrar(self):
        self.destroy()


if __name__ == "__main__":
    app = WorkerLocationApp()
    app.mainloop()