import tkinter as tk
from tkinter import messagebox
import sqlite3

class Curso:
    def __init__(self, nombre, grado):
        self.nombre = nombre
        self.grado = grado

class Matricula:
    def __init__(self, nombres, apellidos, grado_curso):
        self.nombres = nombres
        self.apellidos = apellidos
        self.grado_curso = grado_curso

class RegistroCursosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cursos y Matrícula")

        # Inicializar base de datos de cursos
        self.conn_cursos = sqlite3.connect('registro_cursos.db')
        self.c_cursos = self.conn_cursos.cursor()
        self.create_table_cursos()

        # Inicializar base de datos de matrícula
        self.conn_matricula = sqlite3.connect('matricula.db')
        self.c_matricula = self.conn_matricula.cursor()
        self.create_table_matricula()

        # Crear widgets
        self.label_nombre = tk.Label(root, text="Nombre del Curso:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        self.label_grado = tk.Label(root, text="Grado del Curso:")
        self.label_grado.grid(row=1, column=0, padx=10, pady=5)
        self.entry_grado = tk.Entry(root)
        self.entry_grado.grid(row=1, column=1, padx=10, pady=5)

        self.btn_agregar_curso = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
        self.btn_agregar_curso.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.label_buscar_grado = tk.Label(root, text="Buscar Estudiantes por Grado:")
        self.label_buscar_grado.grid(row=3, column=0, padx=10, pady=5)
        self.entry_buscar_grado = tk.Entry(root)
        self.entry_buscar_grado.grid(row=3, column=1, padx=10, pady=5)

        self.btn_buscar_estudiantes = tk.Button(root, text="Buscar Estudiantes", command=self.buscar_estudiantes_por_grado)
        self.btn_buscar_estudiantes.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
        self.resultado_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_table_cursos(self):
        self.c_cursos.execute('''CREATE TABLE IF NOT EXISTS cursos (
                            codigo TEXT PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            grado TEXT NOT NULL
                            )''')
        self.conn_cursos.commit()

    def create_table_matricula(self):
        self.c_matricula.execute('''CREATE TABLE IF NOT EXISTS matricula (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombres TEXT NOT NULL,
                            apellidos TEXT NOT NULL,
                            grado_curso TEXT NOT NULL,
                            FOREIGN KEY (grado_curso) REFERENCES cursos (grado)
                            )''')
        self.conn_matricula.commit()

    def agregar_curso(self):
        nombre = self.entry_nombre.get()
        grado = self.entry_grado.get()

        if nombre and grado:
            codigo = f"{nombre[:3]}-{grado}"  # Generar código basado en nombre y grado
            curso = Curso(nombre, grado)
            try:
                self.c_cursos.execute("INSERT INTO cursos (codigo, nombre, grado) VALUES (?, ?, ?)",
                                    (codigo, curso.nombre, curso.grado))
                self.conn_cursos.commit()
                messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")
                self.entry_nombre.delete(0, tk.END)
                self.entry_grado.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Ya existe un curso con el mismo código.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def buscar_estudiantes_por_grado(self):
        grado = self.entry_buscar_grado.get()

        if grado:
            self.c_matricula.execute("SELECT nombres, apellidos FROM matricula WHERE grado_curso=?", (grado,))
            estudiantes = self.c_matricula.fetchall()
            if estudiantes:
                resultado = f"Estudiantes matriculados en el grado {grado}:\n"
                for estudiante in estudiantes:
                    resultado += f"Nombres: {estudiante[0]}, Apellidos: {estudiante[1]}\n"
            else:
                resultado = f"No se encontraron estudiantes matriculados en el grado {grado}."
            self.mostrar_resultado(resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un grado para buscar estudiantes.")

    def mostrar_resultado(self, resultado):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, resultado)

    def __del__(self):
        self.conn_cursos.close()
        self.conn_matricula.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroCursosGUI(root)
    root.mainloop()
