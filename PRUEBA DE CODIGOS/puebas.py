import tkinter as tk
from tkinter import messagebox
import sqlite3

class Curso:
    def __init__(self, nombre, codigo, cupo):
        self.nombre = nombre
        self.codigo = codigo
        self.cupo = cupo

class RegistroCursosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cursos")

        # Inicializar base de datos
        self.conn = sqlite3.connect('registro_cursos.db')
        self.c = self.conn.cursor()
        self.create_table()

        # Crear widgets
        self.label_nombre = tk.Label(root, text="Nombre del Curso:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        self.label_codigo = tk.Label(root, text="Código del Curso:")
        self.label_codigo.grid(row=1, column=0, padx=10, pady=5)
        self.entry_codigo = tk.Entry(root)
        self.entry_codigo.grid(row=1, column=1, padx=10, pady=5)

        self.label_cupo = tk.Label(root, text="Cupo del Curso:")
        self.label_cupo.grid(row=2, column=0, padx=10, pady=5)
        self.entry_cupo = tk.Entry(root)
        self.entry_cupo.grid(row=2, column=1, padx=10, pady=5)

        self.btn_agregar = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
        self.btn_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.label_buscar_codigo = tk.Label(root, text="Buscar Curso por Código:")
        self.label_buscar_codigo.grid(row=4, column=0, padx=10, pady=5)
        self.entry_buscar_codigo = tk.Entry(root)
        self.entry_buscar_codigo.grid(row=4, column=1, padx=10, pady=5)

        self.btn_buscar = tk.Button(root, text="Buscar", command=self.buscar_curso)
        self.btn_buscar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.resultado_text = tk.Text(root, height=5, width=50, wrap="word")
        self.resultado_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS cursos (
                            codigo TEXT PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            cupo INTEGER NOT NULL
                            )''')
        self.conn.commit()

    def agregar_curso(self):
        nombre = self.entry_nombre.get()
        codigo = self.entry_codigo.get()
        cupo = self.entry_cupo.get()

        if nombre and codigo and cupo:
            try:
                curso = Curso(nombre, codigo, int(cupo))
                self.c.execute("INSERT INTO cursos (codigo, nombre, cupo) VALUES (?, ?, ?)",
                               (curso.codigo, curso.nombre, curso.cupo))
                self.conn.commit()
                messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")
                self.entry_nombre.delete(0, tk.END)
                self.entry_codigo.delete(0, tk.END)
                self.entry_cupo.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "El cupo debe ser un número entero.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def buscar_curso(self):
        cupo = self.entry_buscar_codigo.get()

        if cupo:
            self.c.execute("SELECT * FROM cursos WHERE codigo=?", (cupo,))
            curso = self.c.fetchone()
            if curso:
                resultado = f"Curso encontrado:\nNombre: {curso[1]}\nCódigo: {curso[0]}\nCupo: {curso[2]}"
            else:
                resultado = f"No se encontró ningún curso con el código {cupo}."
            self.resultado_text.delete(1.0, tk.END)  # Limpiar resultados anteriores
            self.resultado_text.insert(tk.END, resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un código de curso.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroCursosGUI(root)
    root.mainloop()
