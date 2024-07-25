import tkinter as tk
from tkinter import messagebox
import sqlite3

class Curso:
    def __init__(self, nombre, codigo, grado):
        self.nombre = nombre
        self.codigo = codigo
        self.grado = grado

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

        self.label_grado = tk.Label(root, text="Grado del Curso:")
        self.label_grado.grid(row=2, column=0, padx=10, pady=5)
        self.entry_grado = tk.Entry(root)
        self.entry_grado.grid(row=2, column=1, padx=10, pady=5)

        self.btn_agregar = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
        self.btn_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.label_buscar_grado = tk.Label(root, text="Buscar Cursos por Grado:")
        self.label_buscar_grado.grid(row=4, column=0, padx=10, pady=5)
        self.entry_buscar_grado = tk.Entry(root)
        self.entry_buscar_grado.grid(row=4, column=1, padx=10, pady=5)

        self.btn_buscar = tk.Button(root, text="Buscar", command=self.buscar_cursos_por_grado)
        self.btn_buscar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
        self.resultado_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS cursos (
                            codigo TEXT PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            grado TEXT NOT NULL
                            )''')
        self.conn.commit()

    def agregar_curso(self):
        nombre = self.entry_nombre.get()
        codigo = self.entry_codigo.get()
        grado = self.entry_grado.get()

        if nombre and codigo and grado:
            try:
                curso = Curso(nombre, codigo, grado)
                self.c.execute("INSERT INTO cursos (codigo, nombre, grado) VALUES (?, ?, ?)",
                               (curso.codigo, curso.nombre, curso.grado))
                self.conn.commit()
                messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")
                self.entry_nombre.delete(0, tk.END)
                self.entry_codigo.delete(0, tk.END)
                self.entry_grado.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe un curso con el mismo código.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def buscar_cursos_por_grado(self):
        grado = self.entry_buscar_grado.get()

        if grado:
            self.c.execute("SELECT nombre, codigo FROM cursos WHERE grado=?", (grado,))
            cursos = self.c.fetchall()
            if cursos:
                resultado = "Cursos encontrados:\n"
                for curso in cursos:
                    resultado += f"Nombre: {curso[0]}, Código: {curso[1]}\n"
            else:
                resultado = f"No se encontraron cursos para el grado {grado}."
            self.resultado_text.delete(1.0, tk.END)  # Limpiar resultados anteriores
            self.resultado_text.insert(tk.END, resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un grado para buscar cursos.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroCursosGUI(root)
    root.mainloop()
