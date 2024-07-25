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
    
        # Inicializar base de datos de asistencia
        self.conn_asistencia = sqlite3.connect('asistencia.db')
        self.c_asistencia = self.conn_asistencia.cursor()
        self.create_table_asistencia()

        # Crear widgets
        self.label_grado = tk.Label(root, text="Seleccionar Grado:")
        self.label_grado.grid(row=0, column=0, padx=10, pady=5)
        self.combo_grado = ttk.Combobox(root, values=self.obtener_grados())
        self.combo_grado.grid(row=0, column=1, padx=10, pady=5)

        self.label_fecha = tk.Label(root, text="Fecha (YYYY-MM-DD):")
        self.label_fecha.grid(row=1, column=0, padx=10, pady=5)
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.grid(row=1, column=1, padx=10, pady=5)

        self.btn_consultar_asistencia = tk.Button(root, text="Consultar Asistencia", command=self.consultar_asistencia)
        self.btn_consultar_asistencia.grid(row=1, column=2, padx=10, pady=5)

        # Crear las columnas para los días de la semana en el Treeview
        self.treeview_estudiantes = ttk.Treeview(root, columns=("Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"))
        self.treeview_estudiantes.heading("#0", text="ID")
        self.treeview_estudiantes.heading("Nombres", text="Nombres")
        self.treeview_estudiantes.heading("Apellidos", text="Apellidos")
        self.treeview_estudiantes.heading("Grado", text="Grado")
        self.treeview_estudiantes.heading("Lunes", text="Lunes")
        self.treeview_estudiantes.heading("Martes", text="Martes")
        self.treeview_estudiantes.heading("Miércoles", text="Miércoles")
        self.treeview_estudiantes.heading("Jueves", text="Jueves")
        self.treeview_estudiantes.heading("Viernes", text="Viernes")
        self.treeview_estudiantes.column("#0", width=50)
        self.treeview_estudiantes.column("Nombres", width=150)
        self.treeview_estudiantes.column("Apellidos", width=150)
        self.treeview_estudiantes.column("Grado", width=100)
        self.treeview_estudiantes.column("Lunes", width=75)
        self.treeview_estudiantes.column("Martes", width=75)
        self.treeview_estudiantes.column("Miércoles", width=75)
        self.treeview_estudiantes.column("Jueves", width=75)
        self.treeview_estudiantes.column("Viernes", width=75)
        self.treeview_estudiantes.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.cargar_estudiantes()

        # Botón para guardar la asistencia
        self.btn_guardar_asistencia = tk.Button(root, text="Guardar Asistencia", command=self.guardar_asistencia)
        self.btn_guardar_asistencia.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        # Asignar evento de clic para marcar asistencia
        self.treeview_estudiantes.bind("<Button-1>", self.marcar_asistencia)

    def create_table_asistencia(self):
        self.c_asistencia.execute('''CREATE TABLE IF NOT EXISTS asistencia (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_estudiante INTEGER,
                            fecha TEXT,
                            lunes BOOLEAN,
                            martes BOOLEAN,
                            miércoles BOOLEAN,
                            jueves BOOLEAN,
                            viernes BOOLEAN,
                            FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
                            )''')
        self.conn_asistencia.commit()

    def marcar_asistencia(self, event):
        item_id = self.treeview_estudiantes.focus()
        column_id = self.treeview_estudiantes.identify_column(event.x)
        
        # Verificar si se hizo clic en una columna válida
        if column_id in ["#4", "#5", "#6", "#7", "#8"]:  # Columnas correspondientes a Lunes, Martes, Miércoles, Jueves, Viernes
            # Obtener el día de la semana correspondiente
            day = self.treeview_estudiantes.heading(column_id)["text"]
            # Obtener el índice de la columna en el Treeview
            column_index = self.treeview_estudiantes["columns"].index(day)
            # Obtener los valores del ítem seleccionado en el Treeview
            item_values = self.treeview_estudiantes.item(item_id)["values"]
            
            # Verificar si el ítem tiene valores y si el índice de columna es válido
            if item_values and len(item_values) > column_index:
                current_value = item_values[column_index]
                # Cambiar el valor actual
                new_value = "✔" if current_value == "" else ""
                # Actualizar el valor en el Treeview
                self.treeview_estudiantes.set(item_id, column_id, new_value)
            else:
                messagebox.showerror("Error", "No se pudo obtener los valores del estudiante seleccionado.")

    def guardar_asistencia(self):
        fecha = self.entry_fecha.get().strip()
        if not fecha:
            messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
            return
        
        # Iterar sobre todos los estudiantes en el Treeview
        for item_id in self.treeview_estudiantes.get_children():
            estudiante_id = self.treeview_estudiantes.item(item_id)["text"]
            # Obtener los valores de asistencia de cada día
            lunes = "✔" if self.treeview_estudiantes.set(item_id, "#4") else ""
            martes = "✔" if self.treeview_estudiantes.set(item_id, "#5") else ""
            miercoles = "✔" if self.treeview_estudiantes.set(item_id, "#6") else ""
            jueves = "✔" if self.treeview_estudiantes.set(item_id, "#7") else ""
            viernes = "✔" if self.treeview_estudiantes.set(item_id, "#8") else ""
            
            try:
                self.c_asistencia.execute("INSERT INTO asistencia (id_estudiante, fecha, lunes, martes, miércoles, jueves, viernes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                          (estudiante_id, fecha, lunes, martes, miercoles, jueves, viernes))
                self.conn_asistencia.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al guardar asistencia: {e}")
                return
        
        messagebox.showinfo("Asistencia Guardada", f"Asistencia para la fecha {fecha} guardada exitosamente.")

    def consultar_asistencia(self):
        grado = self.combo_grado.get()
        fecha = self.entry_fecha.get().strip()

        if not fecha:
            messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
            return

        # Limpiar el Treeview antes de cargar nuevos datos
        self.treeview_estudiantes.delete(*self.treeview_estudiantes.get_children())

        # Consultar la base de datos para obtener los estudiantes y su asistencia
        self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
        estudiantes = self.c_matricula.fetchall()

        for estudiante in estudiantes:
            estudiante_id = estudiante[0]
            nombre = estudiante[1]
            apellido = estudiante[2]

            # Obtener la asistencia del estudiante para la fecha especificada
            self.c_asistencia.execute("SELECT lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ? AND fecha = ?",
                                      (estudiante_id, fecha))
            registro_asistencia = self.c_asistencia.fetchone()

            # Preparar los valores de asistencia para mostrar en el Treeview
            if registro_asistencia:
                lunes = "✔" if registro_asistencia[0] else ""
                martes = "✔" if registro_asistencia[1] else ""
                miercoles = "✔" if registro_asistencia[2] else ""
                jueves = "✔" if registro_asistencia[3] else ""
                viernes = "✔" if registro_asistencia[4] else ""
            else:
                lunes = ""
                martes = ""
                miercoles = ""
                jueves = ""
                viernes = ""

            # Insertar en el Treeview
            self.treeview_estudiantes.insert("", "end", text=estudiante_id, values=(nombre, apellido, grado, lunes, martes, miercoles, jueves, viernes))

    def obtener_grados(self):
        self.c_matricula.execute("SELECT DISTINCT grado_curso FROM matricula")
        grados = [row[0] for row in self.c_matricula.fetchall()]
        return grados

    def cargar_estudiantes(self):
        # Limpiar el Treeview antes de cargar nuevos datos
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
