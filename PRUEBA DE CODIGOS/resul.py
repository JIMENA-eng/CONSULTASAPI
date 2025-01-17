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
        self.combo_grado.bind("<<ComboboxSelected>>", self.cargar_estudiantes_por_grado)

        self.label_fecha = tk.Label(root, text="Fecha (YYYY-MM-DD):")
        self.label_fecha.grid(row=1, column=0, padx=10, pady=5)
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.grid(row=1, column=1, padx=10, pady=5)

        self.btn_ver_asistencias = tk.Button(root, text="Ver Asistencias", command=self.ver_asistencias)
        self.btn_ver_asistencias.grid(row=1, column=2, padx=10, pady=5)

        self.treeview_estudiantes = ttk.Treeview(root, columns=("Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"), show='headings')
        self.treeview_estudiantes.heading("Nombres", text="Nombres")
        self.treeview_estudiantes.heading("Apellidos", text="Apellidos")
        self.treeview_estudiantes.heading("Grado", text="Grado")
        self.treeview_estudiantes.heading("Lunes", text="Lunes")
        self.treeview_estudiantes.heading("Martes", text="Martes")
        self.treeview_estudiantes.heading("Miércoles", text="Miércoles")
        self.treeview_estudiantes.heading("Jueves", text="Jueves")
        self.treeview_estudiantes.heading("Viernes", text="Viernes")
        self.treeview_estudiantes.column("Nombres", width=150)
        self.treeview_estudiantes.column("Apellidos", width=150)
        self.treeview_estudiantes.column("Grado", width=100)
        self.treeview_estudiantes.column("Lunes", width=75)
        self.treeview_estudiantes.column("Martes", width=75)
        self.treeview_estudiantes.column("Miércoles", width=75)
        self.treeview_estudiantes.column("Jueves", width=75)
        self.treeview_estudiantes.column("Viernes", width=75)
        self.treeview_estudiantes.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.btn_guardar_asistencia = tk.Button(root, text="Guardar Asistencia", command=self.guardar_asistencia)
        self.btn_guardar_asistencia.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        self.btn_ver_todas_asistencias = tk.Button(root, text="Ver Todas las Asistencias", command=self.ver_todas_asistencias)
        self.btn_ver_todas_asistencias.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        self.treeview_estudiantes.bind("<Button-1>", self.marcar_asistencia)

    def create_table_asistencia(self):
        self.c_asistencia.execute('''
            CREATE TABLE IF NOT EXISTS asistencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_estudiante INTEGER,
                fecha TEXT,
                lunes TEXT,
                martes TEXT,
                miércoles TEXT,
                jueves TEXT,
                viernes TEXT,
                FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
            )
        ''')
        self.conn_asistencia.commit()

    def marcar_asistencia(self, event):
        item_id = self.treeview_estudiantes.focus()
        column_id = self.treeview_estudiantes.identify_column(event.x)
        
        # Verificar si se hizo clic en una columna válida
        if column_id in ["#4", "#5", "#6", "#7", "#8"]:  # Columnas correspondientes a Lunes, Martes, Miércoles, Jueves, Viernes
            # Obtener el índice de la columna en el Treeview
            column_index = int(column_id.replace("#", "")) - 1
            # Obtener los valores del ítem seleccionado en el Treeview
            item_values = self.treeview_estudiantes.item(item_id)["values"]
            
            # Verificar si el ítem tiene valores y si el índice de columna es válido
            if item_values and len(item_values) >= column_index:
                current_value = item_values[column_index]
                # Cambiar el valor actual
                new_value = "Asistió" if current_value == "No asistió" else "No asistió"
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
            estudiante_id = self.treeview_estudiantes.item(item_id, "text")
            # Obtener los valores de asistencia de cada día
            lunes = self.treeview_estudiantes.item(item_id, "values")[3]
            martes = self.treeview_estudiantes.item(item_id, "values")[4]
            miercoles = self.treeview_estudiantes.item(item_id, "values")[5]
            jueves = self.treeview_estudiantes.item(item_id, "values")[6]
            viernes = self.treeview_estudiantes.item(item_id, "values")[7]
            
            try:
                self.c_asistencia.execute('''
                    INSERT INTO asistencia (id_estudiante, fecha, lunes, martes, miércoles, jueves, viernes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (estudiante_id, fecha, lunes, martes, miercoles, jueves, viernes))
                self.conn_asistencia.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al guardar asistencia: {e}")
                return
        
        messagebox.showinfo("Asistencia Guardada", f"Asistencia para la fecha {fecha} guardada exitosamente.")

    def ver_asistencias(self):
        fecha = self.entry_fecha.get().strip()
        grado = self.combo_grado.get()

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
            asistencia = self.c_asistencia.fetchone()

            if asistencia:
                lunes = asistencia[0] if asistencia[0] else "No asistió"
                martes = asistencia[1] if asistencia[1] else "No asistió"
                miercoles = asistencia[2] if asistencia[2] else "No asistió"
                jueves = asistencia[3] if asistencia[3] else "No asistió"
                viernes = asistencia[4] if asistencia[4] else "No asistió"
            else:
                lunes = martes = miercoles = jueves = viernes = "No asistió"

            self.treeview_estudiantes.insert("", "end", text=estudiante_id, values=(nombre, apellido, grado, lunes, martes, miercoles, jueves, viernes))

    def ver_todas_asistencias(self):
        def obtener_asistencias():
            grado = entry_grado.get().strip()

            if not grado:
                messagebox.showerror("Error", "Ingrese un grado válido.")
                return

            # Limpiar el Treeview antes de cargar nuevos datos
            tree.delete(*tree.get_children())

            # Consultar la base de datos para obtener todos los estudiantes en el grado seleccionado
            self.c_matricula.execute("SELECT id, nombres, apellidos, grado_curso FROM matricula WHERE grado_curso = ?", (grado,))
            estudiantes = self.c_matricula.fetchall()

            for estudiante in estudiantes:
                estudiante_id = estudiante[0]
                nombre = estudiante[1]
                apellido = estudiante[2]
                grado = estudiante[3]

                # Consultar todas las asistencias del estudiante
                self.c_asistencia.execute("SELECT fecha, lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ?", (estudiante_id,))
                asistencias = self.c_asistencia.fetchall()

                for asistencia in asistencias:
                    fecha, lunes, martes, miercoles, jueves, viernes = asistencia

                    # Usar "Asistió" o "No asistió"
                    lunes = "Asistió" if lunes == "Asistió" else "No asistió"
                    martes = "Asistió" if martes == "Asistió" else "No asistió"
                    miercoles = "Asistió" if miercoles == "Asistió" else "No asistió"
                    jueves = "Asistió" if jueves == "Asistió" else "No asistió"
                    viernes = "Asistió" if viernes == "Asistió" else "No asistió"

                    tree.insert("", "end", values=(f"{nombre} {apellido}", fecha, lunes, martes, miercoles, jueves, viernes))

        # Crear ventana secundaria para buscar todas las asistencias
        ventana_todas_asistencias = tk.Toplevel(self.root)
        ventana_todas_asistencias.title("Ver Todas las Asistencias")

        # Crear un frame para la entrada
        frame_entrada = tk.Frame(ventana_todas_asistencias)
        frame_entrada.pack(padx=10, pady=10)

        # Etiqueta y entrada para el grado
        label_grado = tk.Label(frame_entrada, text="Grado:")
        label_grado.grid(row=0, column=0, padx=5, pady=5)
        entry_grado = tk.Entry(frame_entrada)
        entry_grado.grid(row=0, column=1, padx=5, pady=5)

        # Botón para buscar
        btn_buscar = tk.Button(frame_entrada, text="Buscar", command=obtener_asistencias)
        btn_buscar.grid(row=1, columnspan=2, pady=10)

        # Crear el árbol para mostrar resultados
        columns = ("Nombre", "Fecha", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
        tree = ttk.Treeview(ventana_todas_asistencias, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def obtener_grados(self):
        self.c_matricula.execute("SELECT DISTINCT grado_curso FROM matricula")
        grados = [row[0] for row in self.c_matricula.fetchall()]
        return grados

    def cargar_estudiantes_por_grado(self, event=None):
        grado = self.combo_grado.get()
        self.treeview_estudiantes.delete(*self.treeview_estudiantes.get_children())
        self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
        estudiantes = self.c_matricula.fetchall()
        for estudiante in estudiantes:
            self.treeview_estudiantes.insert("", "end", text=estudiante[0], values=(estudiante[1], estudiante[2], grado, "No asistió", "No asistió", "No asistió", "No asistió", "No asistió"))

    def __del__(self):
        self.conn_matricula.close()
        self.conn_asistencia.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenciaGUI(root)
    root.mainloop()
