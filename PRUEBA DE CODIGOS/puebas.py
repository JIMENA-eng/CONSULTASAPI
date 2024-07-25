import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Matricula:
    def __init__(self, nombres, apellidos, grado_curso):
        self.nombres = nombres
        self.apellidos = apellidos
        self.grado_curso = grado_curso

class AsistenciaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Asistencia por Grado")

        # Inicializar base de datos de matrícula
        self.conn_matricula = sqlite3.connect('matricula.db')
        self.c_matricula = self.conn_matricula.cursor()
        self.create_table_matricula()

        # Inicializar base de datos de asistencia
        self.conn_asistencia = sqlite3.connect('asistencia.db')
        self.c_asistencia = self.conn_asistencia.cursor()
        self.create_table_asistencia()

        # Crear widgets
        self.label_grado = tk.Label(root, text="Seleccionar Grado:")
        self.label_grado.grid(row=0, column=0, padx=10, pady=5)
        self.combo_grado = ttk.Combobox(root, values=self.obtener_grados())
        self.combo_grado.grid(row=0, column=1, padx=10, pady=5)

        self.btn_matricular = tk.Button(root, text="Matricular", command=self.matricular_estudiante)
        self.btn_matricular.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.btn_registrar_asistencia = tk.Button(root, text="Registrar Asistencia", command=self.registrar_asistencia)
        self.btn_registrar_asistencia.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.treeview_estudiantes = ttk.Treeview(root, columns=("Nombres", "Apellidos", "Grado"))
        self.treeview_estudiantes.heading("#0", text="ID")
        self.treeview_estudiantes.heading("Nombres", text="Nombres")
        self.treeview_estudiantes.heading("Apellidos", text="Apellidos")
        self.treeview_estudiantes.heading("Grado", text="Grado")
        self.treeview_estudiantes.column("#0", width=50)
        self.treeview_estudiantes.column("Nombres", width=150)
        self.treeview_estudiantes.column("Apellidos", width=150)
        self.treeview_estudiantes.column("Grado", width=100)
        self.treeview_estudiantes.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.cargar_estudiantes()

    def create_table_matricula(self):
        self.c_matricula.execute('''CREATE TABLE IF NOT EXISTS matricula (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombres TEXT NOT NULL,
                            apellidos TEXT NOT NULL,
                            grado_curso TEXT NOT NULL
                            )''')
        self.conn_matricula.commit()

    def create_table_asistencia(self):
        self.c_asistencia.execute('''CREATE TABLE IF NOT EXISTS asistencia (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_estudiante INTEGER,
                            fecha TEXT,
                            presente BOOLEAN,
                            FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
                            )''')
        self.conn_asistencia.commit()

    def matricular_estudiante(self):
        nombres = tk.simpledialog.askstring("Matrícula", "Ingrese los nombres del estudiante:")
        apellidos = tk.simpledialog.askstring("Matrícula", "Ingrese los apellidos del estudiante:")
        grado = self.combo_grado.get()

        if nombres and apellidos and grado:
            estudiante = Matricula(nombres, apellidos, grado)
            try:
                self.c_matricula.execute("INSERT INTO matricula (nombres, apellidos, grado_curso) VALUES (?, ?, ?)",
                                        (estudiante.nombres, estudiante.apellidos, estudiante.grado_curso))
                self.conn_matricula.commit()
                messagebox.showinfo("Matrícula", f"Estudiante {estudiante.nombres} {estudiante.apellidos} matriculado en {estudiante.grado_curso}.")
                self.cargar_estudiantes()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al matricular estudiante: {e}")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def registrar_asistencia(self):
        seleccion = self.treeview_estudiantes.selection()
        if seleccion:
            estudiante_id = self.treeview_estudiantes.item(seleccion)["text"]
            fecha = "2024-07-26"  # Ejemplo de fecha (se puede obtener dinámicamente)
            presente = True  # Ejemplo de asistencia (se puede obtener dinámicamente)

            try:
                self.c_asistencia.execute("INSERT INTO asistencia (id_estudiante, fecha, presente) VALUES (?, ?, ?)",
                                        (estudiante_id, fecha, presente))
                self.conn_asistencia.commit()
                messagebox.showinfo("Registro de Asistencia", f"Asistencia registrada para estudiante ID {estudiante_id}.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al registrar asistencia: {e}")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un estudiante.")

    def obtener_grados(self):
        self.c_matricula.execute("SELECT DISTINCT grado_curso FROM matricula")
        grados = [row[0] for row in self.c_matricula.fetchall()]
        return grados

    def cargar_estudiantes(self):
        self.treeview_estudiantes.delete(*self.treeview_estudiantes.get_children())
        self.c_matricula.execute("SELECT id, nombres, apellidos, grado_curso FROM matricula")
        estudiantes = self.c_matricula.fetchall()
        for estudiante in estudiantes:
            self.treeview_estudiantes.insert("", "end", text=estudiante[0], values=(estudiante[1], estudiante[2], estudiante[3]))

    def __del__(self):
        self.conn_matricula.close()
        self.conn_asistencia.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenciaGUI(root)
    root.mainloop()
