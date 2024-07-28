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

        # Inicializar base de datos de matrícula y asistencia
        self.conn_matricula = sqlite3.connect('matricula.db')
        self.c_matricula = self.conn_matricula.cursor()

        self.conn_asistencia = sqlite3.connect('asistencia.db')
        self.c_asistencia = self.conn_asistencia.cursor()
        self.create_table_asistencia()

        # Crear widgets
        self.create_widgets()
        self.populate_grado_combobox()

    def create_widgets(self):
        # Etiqueta y combo para seleccionar grado
        self.label_grado = tk.Label(self.root, text="Seleccionar Grado:")
        self.label_grado.grid(row=0, column=0, padx=10, pady=5)
        self.combo_grado = ttk.Combobox(self.root)
        self.combo_grado.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y entrada para la fecha
        self.label_fecha = tk.Label(self.root, text="Fecha (YYYY-MM-DD):")
        self.label_fecha.grid(row=1, column=0, padx=10, pady=5)
        self.entry_fecha = tk.Entry(self.root)
        self.entry_fecha.grid(row=1, column=1, padx=10, pady=5)

        # Botón para ver asistencias
        self.btn_ver_asistencias = tk.Button(self.root, text="Ver Asistencias", command=self.ver_asistencias)
        self.btn_ver_asistencias.grid(row=1, column=2, padx=10, pady=5)

        # Treeview para mostrar resultados
        columns = ("Fecha", "Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
        self.treeview_estudiantes = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.treeview_estudiantes.heading(col, text=col)
            self.treeview_estudiantes.column(col, width=100)
        self.treeview_estudiantes.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Botones para guardar asistencia y ver todas las asistencias
        self.btn_guardar_asistencia = tk.Button(self.root, text="Guardar Asistencia", command=self.guardar_asistencia)
        self.btn_guardar_asistencia.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        self.btn_ver_todas_asistencias = tk.Button(self.root, text="Ver Todas las Asistencias", command=self.ver_todas_asistencias)
        self.btn_ver_todas_asistencias.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

        # Asociar evento de clic en el Treeview
        self.treeview_estudiantes.bind("<ButtonRelease-1>", self.on_treeview_click)

    def create_table_asistencia(self):
        self.c_asistencia.execute('''
            CREATE TABLE IF NOT EXISTS asistencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_estudiante INTEGER,
                fecha TEXT,
                lunes BOOLEAN,
                martes BOOLEAN,
                miércoles BOOLEAN,
                jueves BOOLEAN,
                viernes BOOLEAN,
                FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
            )
        ''')
        self.conn_asistencia.commit()

    def populate_grado_combobox(self):
        grados = self.obtener_grados()
        self.combo_grado['values'] = grados

    def obtener_grados(self):
        self.c_matricula.execute("SELECT DISTINCT grado_curso FROM matricula")
        grados = [row[0] for row in self.c_matricula.fetchall()]
        return grados

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
            estudiante_id, nombre, apellido = estudiante

            # Obtener la asistencia del estudiante para la fecha especificada
            self.c_asistencia.execute("SELECT lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ? AND fecha = ?",
                                    (estudiante_id, fecha))
            asistencia = self.c_asistencia.fetchone()

            if asistencia:
                lunes = "Asistió" if asistencia[0] else "No asistió"
                martes = "Asistió" if asistencia[1] else "No asistió"
                miercoles = "Asistió" if asistencia[2] else "No asistió"
                jueves = "Asistió" if asistencia[3] else "No asistió"
                viernes = "Asistió" if asistencia[4] else "No asistió"
            else:
                lunes = martes = miercoles = jueves = viernes = "No asistió"

            self.treeview_estudiantes.insert("", "end", values=(fecha, nombre, apellido, grado, lunes, martes, miercoles, jueves, viernes))

    def guardar_asistencia(self):
        fecha = self.entry_fecha.get().strip()
        if not fecha:
            messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
            return
        
        # Iterar sobre todos los estudiantes en el Treeview
        for item_id in self.treeview_estudiantes.get_children():
            estudiante_id = self.treeview_estudiantes.item(item_id)["text"]
            # Obtener los valores de asistencia de cada día
            lunes = self.treeview_estudiantes.set(item_id, "Lunes") == "Asistió"
            martes = self.treeview_estudiantes.set(item_id, "Martes") == "Asistió"
            miercoles = self.treeview_estudiantes.set(item_id, "Miércoles") == "Asistió"
            jueves = self.treeview_estudiantes.set(item_id, "Jueves") == "Asistió"
            viernes = self.treeview_estudiantes.set(item_id, "Viernes") == "Asistió"
            
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

    def on_treeview_click(self, event):
        item = self.treeview_estudiantes.identify('item', event.x, event.y)
        column = self.treeview_estudiantes.identify_column(event.x)
        
        # Verificar si se hizo clic en una columna de asistencia
        if column in ["#5", "#6", "#7", "#8", "#9"]:  # Columnas correspondientes a Lunes, Martes, Miércoles, Jueves, Viernes
            column_id = self.treeview_estudiantes["columns"].index(self.treeview_estudiantes.heading(column)["text"])
            current_value = self.treeview_estudiantes.item(item, "values")[column_id]

            # Cambiar el valor actual
            new_value = "Asistió" if current_value == "No asistió" else "No asistió"
            self.treeview_estudiantes.set(item, column, new_value)

    def ver_todas_asistencias(self):
        def obtener_asistencias():
            grado = entry_grado.get().strip()
            nombre_buscar = entry_nombre.get().strip()
            
            if not grado:
                messagebox.showerror("Error", "Ingrese un grado válido.")
                return

            # Limpiar el Treeview antes de cargar nuevos datos
            tree.delete(*tree.get_children())

            # Consultar la base de datos para obtener todos los estudiantes en el grado seleccionado
            self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
            estudiantes = self.c_matricula.fetchall()

            for estudiante in estudiantes:
                estudiante_id, nombre, apellido = estudiante

                if nombre_buscar.lower() not in nombre.lower():
                    continue

                # Obtener todas las asistencias del estudiante
                self.c_asistencia.execute("SELECT fecha, lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ?",
                                        (estudiante_id,))
                asistencias = self.c_asistencia.fetchall()

                for asistencia in asistencias:
                    fecha, lunes, martes, miercoles, jueves, viernes = asistencia

                    # Convertir booleanos a texto
                    lunes = "Asistió" if lunes else "No asistió"
                    martes = "Asistió" if martes else "No asistió"
                    miercoles = "Asistió" if miercoles else "No asistió"
                    jueves = "Asistió" if jueves else "No asistió"
                    viernes = "Asistió" if viernes else "No asistió"

                    tree.insert("", "end", values=(f"{nombre} {apellido}", fecha, lunes, martes, miercoles, jueves, viernes))

        # Crear ventana secundaria para buscar todas las asistencias
        ventana_todas_asistencias = tk.Toplevel(self.root)
        ventana_todas_asistencias.title("Buscar Asistencias por Grado")

        # Crear un frame para la entrada
        frame_entrada = tk.Frame(ventana_todas_asistencias)
        frame_entrada.pack(padx=10, pady=10)

        # Etiqueta y entrada para el grado
        label_grado = tk.Label(frame_entrada, text="Grado:")
        label_grado.grid(row=0, column=0, padx=5, pady=5)
        entry_grado = tk.Entry(frame_entrada)
        entry_grado.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y entrada para el nombre
        label_nombre = tk.Label(frame_entrada, text="Nombre:")
        label_nombre.grid(row=1, column=0, padx=5, pady=5)
        entry_nombre = tk.Entry(frame_entrada)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Botón para buscar
        btn_buscar = tk.Button(frame_entrada, text="Buscar", command=obtener_asistencias)
        btn_buscar.grid(row=2, columnspan=2, pady=10)

        # Crear el árbol para mostrar resultados
        columns = ("Nombre", "Fecha", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
        tree = ttk.Treeview(ventana_todas_asistencias, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def __del__(self):
        self.conn_matricula.close()
        self.conn_asistencia.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AsistenciaGUI(root)
    root.mainloop()
