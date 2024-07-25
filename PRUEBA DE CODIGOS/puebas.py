import tkinter as tk
from tkinter import messagebox
import sqlite3

class Curso:
    def __init__(self, nombre, codigo, grado):
        self.nombre = nombre
        self.codigo = codigo
        self.grado = grado

class Matricula:
    def __init__(self, nombres, apellidos, codigo_curso):
        self.nombres = nombres
        self.apellidos = apellidos
        self.codigo_curso = codigo_curso

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

        # Inicializar base de datos de empleados
        self.conn_empleados = sqlite3.connect('asistencia.db')
        self.c_empleados = self.conn_empleados.cursor()

        # Crear widgets
        self.label_dni = tk.Label(root, text="Ingrese DNI del Empleado:")
        self.label_dni.grid(row=0, column=0, padx=10, pady=5)
        self.entry_dni = tk.Entry(root)
        self.entry_dni.grid(row=0, column=1, padx=10, pady=5)

        self.btn_buscar = tk.Button(root, text="Buscar Empleado", command=self.buscar_empleado)
        self.btn_buscar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.label_nombre = tk.Label(root, text="Nombre del Curso:")
        self.label_nombre.grid(row=2, column=0, padx=10, pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=5)

        self.label_codigo = tk.Label(root, text="Código del Curso:")
        self.label_codigo.grid(row=3, column=0, padx=10, pady=5)
        self.entry_codigo = tk.Entry(root)
        self.entry_codigo.grid(row=3, column=1, padx=10, pady=5)

        self.label_grado = tk.Label(root, text="Grado del Curso:")
        self.label_grado.grid(row=4, column=0, padx=10, pady=5)
        self.entry_grado = tk.Entry(root)
        self.entry_grado.grid(row=4, column=1, padx=10, pady=5)

        self.btn_agregar_curso = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
        self.btn_agregar_curso.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.label_buscar_grado = tk.Label(root, text="Buscar Cursos por Grado:")
        self.label_buscar_grado.grid(row=6, column=0, padx=10, pady=5)
        self.entry_buscar_grado = tk.Entry(root)
        self.entry_buscar_grado.grid(row=6, column=1, padx=10, pady=5)

        self.btn_buscar_grado = tk.Button(root, text="Buscar", command=self.buscar_cursos_por_grado)
        self.btn_buscar_grado.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
        self.resultado_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

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
                            codigo_curso TEXT NOT NULL,
                            FOREIGN KEY (codigo_curso) REFERENCES cursos (codigo)
                            )''')
        self.conn_matricula.commit()

    def buscar_empleado(self):
        dni = self.entry_dni.get()

        if dni:
            self.c_empleados.execute("SELECT NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO FROM empleados WHERE DNI=?", (dni,))
            empleado = self.c_empleados.fetchone()
            if empleado:
                nombres, apellido_paterno, apellido_materno = empleado
                self.mostrar_resultado(f"Empleado encontrado:\n{apellido_paterno} {apellido_materno}, {nombres}")
            else:
                self.mostrar_resultado("No se encontró ningún empleado con el DNI especificado.")
        else:
            messagebox.showerror("Error", "Por favor, ingrese el DNI del empleado.")

    def agregar_curso(self):
        nombre = self.entry_nombre.get()
        codigo = self.entry_codigo.get()
        grado = self.entry_grado.get()

        if nombre and codigo and grado:
            curso = Curso(nombre, codigo, grado)
            try:
                self.c_cursos.execute("INSERT INTO cursos (codigo, nombre, grado) VALUES (?, ?, ?)",
                                    (curso.codigo, curso.nombre, curso.grado))
                self.conn_cursos.commit()
                messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")

                # Obtener nombres y apellidos del empleado por DNI
                dni = self.entry_dni.get()
                self.c_empleados.execute("SELECT NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO FROM empleados WHERE DNI=?", (dni,))
                empleado = self.c_empleados.fetchone()
                if empleado:
                    nombres, apellido_paterno, apellido_materno = empleado
                    matricula = Matricula(nombres, f"{apellido_paterno} {apellido_materno}", curso.codigo)
                    self.c_matricula.execute("INSERT INTO matricula (nombres, apellidos, codigo_curso) VALUES (?, ?, ?)",
                                            (matricula.nombres, matricula.apellidos, matricula.codigo_curso))
                    self.conn_matricula.commit()
                    messagebox.showinfo("Matrícula", f"Empleado matriculado en el curso {curso.nombre}.")
                else:
                    messagebox.showerror("Error", "No se encontró un empleado con el DNI especificado.")

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
            self.c_cursos.execute("SELECT nombre, codigo FROM cursos WHERE grado=?", (grado,))
            cursos = self.c_cursos.fetchall()
            if cursos:
                resultado = "Cursos encontrados:\n"
                for curso in cursos:
                    resultado += f"Nombre: {curso[0]}, Código: {curso[1]}\n"
            else:
                resultado = f"No se encontraron cursos para el grado {grado}."
            self.mostrar_resultado(resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un grado para buscar cursos.")

    def mostrar_resultado(self, resultado):
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, resultado)

    def __del__(self):
        self.conn_cursos.close()
        self.conn_matricula.close()
        self.conn_empleados.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroCursosGUI(root)
    root.mainloop()
