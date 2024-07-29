

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Función para obtener el grado del usuario desde la base de datos
def obtener_grado_usuario(usuario):
    conn = sqlite3.connect('usuarios.bd')
    c = conn.cursor()
    c.execute("SELECT grado FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = c.fetchone()
    conn.close()
    if resultado:
        return resultado[0]
    else:
        raise ValueError("Usuario no encontrado")

# Función para registrar un nuevo usuario
def registrar_usuario(usuario, correo, grado, contrasena):
    conn = sqlite3.connect('usuarios.bd')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (usuario, correo, grado, contrasena) VALUES (?, ?, ?, ?)", 
                  (usuario, correo, grado, contrasena))
        conn.commit()
        messagebox.showinfo("Registro Exitoso", "Usuario registrado exitosamente.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario o correo ya existe.")
    finally:
        conn.close()

# Función para autenticar un usuario
def autenticar_usuario(usuario, contrasena):
    conn = sqlite3.connect('usuarios.bd')
    c = conn.cursor()
    c.execute("SELECT grado FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    resultado = c.fetchone()
    conn.close()
    if resultado:
        return resultado[0]
    else:
        raise ValueError("Usuario o contraseña incorrectos")

# Clase para manejar la interfaz gráfica y la lógica de asistencia
class AsistenciaGUI:
    def __init__(self, root, grado_usuario):
        self.root = root
        self.grado_usuario = grado_usuario
        self.root.title("Registro de Asistencia por Grado")

        # Inicializar base de datos de matrícula y asistencia
        self.conn_matricula = sqlite3.connect('matricula.db')
        self.c_matricula = self.conn_matricula.cursor()

        self.conn_asistencia = sqlite3.connect('asistencia.db')
        self.c_asistencia = self.conn_asistencia.cursor()
        self.create_table_asistencia()

        # Crear widgets
        self.create_widgets()

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

    def ver_asistencias(self):
        fecha = self.entry_fecha.get().strip()
        grado = self.combo_grado.get()

        if not fecha:
            messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
            return

        if grado != self.grado_usuario:
            messagebox.showerror("Error", "No tiene permiso para ver las asistencias de este grado.")
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
            new_value = "Asistió" if current_value == "No asistió" else "No asistió"
            self.treeview_estudiantes.item(item, values=(self.treeview_estudiantes.item(item, "values")[0],  # Fecha
                                                        self.treeview_estudiantes.item(item, "values")[1],  # Nombres
                                                        self.treeview_estudiantes.item(item, "values")[2],  # Apellidos
                                                        self.treeview_estudiantes.item(item, "values")[3],  # Grado
                                                        new_value if i == column_id else v for i, v in enumerate(self.treeview_estudiantes.item(item, "values")[4:])))
    
    def ver_todas_asistencias(self):
        def obtener_asistencias():
            grado = entry_grado.get().strip()
            nombre_buscar = entry_nombre.get().strip().lower()

            if not grado:
                messagebox.showerror("Error", "Ingrese un grado válido.")
                return

            if grado != self.grado_usuario:
                messagebox.showerror("Error", "No tiene permiso para ver las asistencias de este grado.")
                return

            # Limpiar el Treeview antes de cargar nuevos datos
            tree.delete(*tree.get_children())

            # Consultar la base de datos para obtener todos los estudiantes en el grado seleccionado
            self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
            estudiantes = self.c_matricula.fetchall()

            for estudiante in estudiantes:
                estudiante_id, nombre, apellido = estudiante

                if nombre_buscar not in nombre.lower():
                    continue

                # Obtener la asistencia del estudiante para todas las fechas
                self.c_asistencia.execute("SELECT fecha, lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ?",
                                        (estudiante_id,))
                asistencias = self.c_asistencia.fetchall()

                for asistencia in asistencias:
                    fecha, lunes, martes, miercoles, jueves, viernes = asistencia
                    tree.insert("", "end", values=(fecha, nombre, apellido, grado, 
                                                    "Asistió" if lunes else "No asistió",
                                                    "Asistió" if martes else "No asistió",
                                                    "Asistió" if miercoles else "No asistió",
                                                    "Asistió" if jueves else "No asistió",
                                                    "Asistió" if viernes else "No asistió"))

        # Crear ventana secundaria para ver todas las asistencias
        ver_asistencias_window = tk.Toplevel(self.root)
        ver_asistencias_window.title("Ver Todas las Asistencias")
        tk.Label(ver_asistencias_window, text="Grado:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(ver_asistencias_window, text="Nombre (opcional):").grid(row=1, column=0, padx=10, pady=5)
        
        entry_grado = tk.Entry(ver_asistencias_window)
        entry_grado.grid(row=0, column=1, padx=10, pady=5)
        entry_nombre = tk.Entry(ver_asistencias_window)
        entry_nombre.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(ver_asistencias_window, text="Buscar", command=obtener_asistencias).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Crear Treeview para mostrar las asistencias
        columns = ("Fecha", "Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
        tree = ttk.Treeview(ver_asistencias_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()
    root.title("Inicio de Sesión")

    # Widgets para iniciar sesión
    tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5)
    entry_contrasena = tk.Entry(root, show="*")
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    def login():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get().strip()
        try:
            grado_usuario = autenticar_usuario(usuario, contrasena)
            root.destroy()  # Cerrar ventana de inicio de sesión
            app = tk.Tk()
            AsistenciaGUI(app, grado_usuario)
            app.mainloop()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Iniciar Sesión", command=login).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Botones para registrar nuevo usuario
    tk.Button(root, text="Registrar Usuario", command=lambda: registrar_usuario_window(root)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def registrar_usuario_window(parent):
    def registrar():
        usuario = entry_usuario.get().strip()
        correo = entry_correo.get().strip()
        grado = entry_grado.get().strip()
        contrasena = entry_contrasena.get().strip()
        registrar_usuario(usuario, correo, grado, contrasena)
        reg_window.destroy()

    reg_window = tk.Toplevel(parent)
    reg_window.title("Registrar Usuario")

    tk.Label(reg_window, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
    entry_usuario = tk.Entry(reg_window)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(reg_window, text="Correo:").grid(row=1, column=0, padx=10, pady=5)
    entry_correo = tk.Entry(reg_window)
    entry_correo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(reg_window, text="Grado:").grid(row=2, column=0, padx=10, pady=5)
    entry_grado = tk.Entry(reg_window)
    entry_grado.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(reg_window, text="Contraseña:").grid(row=3, column=0, padx=10, pady=5)
    entry_contrasena = tk.Entry(reg_window, show="*")
    entry_contrasena.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(reg_window, text="Registrar", command=registrar).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar la aplicación principal
if __name__ == "__main__":
    main()
