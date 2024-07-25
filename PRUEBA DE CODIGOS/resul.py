import sqlite3
import tkinter as tk
from tkinter import messagebox

# Función para crear las tablas si no existen
def crear_tablas():
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    # Crear tabla estudiantes si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRES TEXT,
            APELLIDO_PATERNO TEXT,
            APELLIDO_MATERNO TEXT,
            DNI TEXT,
            GENERO TEXT,
            ESTADO_CIVIL TEXT,
            FECHA_HORA TEXT
        )
    ''')

    # Crear tabla cursos si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT,
            DESCRIPCION TEXT
        )
    ''')

    # Verificar si la tabla estudiantes_cursos necesita ser creada o actualizada
    cursor.execute("PRAGMA table_info('estudiantes_cursos')")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]

    if 'grado' not in column_names:
        # Crear tabla de relación estudiantes_cursos si no existe o actualizarla con la columna grado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes_cursos (
                id_estudiante INTEGER,
                id_curso INTEGER,
                grado TEXT,
                FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),
                FOREIGN KEY (id_curso) REFERENCES cursos(id),
                PRIMARY KEY (id_estudiante, id_curso)
            )
        ''')

    conn.commit()
    conn.close()

# Función para insertar datos de ejemplo (estudiantes y cursos)
def insertar_datos_ejemplo():
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    # Insertar estudiantes de ejemplo
    estudiantes = [
        ('Juan', 'Perez', 'Gomez', '12345678', 'Masculino', 'Soltero', '2024-07-25 10:00:00'),
        ('Maria', 'Gonzalez', 'Lopez', '87654321', 'Femenino', 'Casada', '2024-07-25 11:00:00'),
        ('Pedro', 'Martinez', 'Rodriguez', '55556666', 'Masculino', 'Soltero', '2024-07-25 12:00:00')
    ]
    cursor.executemany('''
        INSERT INTO estudiantes (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', estudiantes)

    # Insertar cursos de ejemplo
    cursos = [
        ('Matemáticas', 'Curso de matemáticas avanzadas'),
        ('Historia', 'Curso de historia universal'),
        ('Literatura', 'Curso de literatura clásica')
    ]
    cursor.executemany('''
        INSERT INTO cursos (NOMBRE, DESCRIPCION)
        VALUES (?, ?)
    ''', cursos)

    conn.commit()
    conn.close()

# Función para asignar cursos a un estudiante con un grado específico
def asignar_cursos(id_estudiante, cursos_seleccionados, grado):
    try:
        conn = sqlite3.connect('escuela.db')
        cursor = conn.cursor()

        # Eliminar todas las asignaciones previas del estudiante
        cursor.execute('DELETE FROM estudiantes_cursos WHERE id_estudiante = ?', (id_estudiante,))

        # Insertar los nuevos cursos asignados con el mismo grado para todos
        for id_curso in cursos_seleccionados:
            cursor.execute('''
                INSERT INTO estudiantes_cursos (id_estudiante, id_curso, grado)
                VALUES (?, ?, ?)
            ''', (id_estudiante, id_curso, grado))

        conn.commit()
        messagebox.showinfo("Éxito", "Cursos asignados correctamente.")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al asignar cursos: {e}")

    finally:
        if conn:
            conn.close()

# Función para mostrar estudiantes asignados a un curso específico
def mostrar_estudiantes_por_curso(id_curso):
    try:
        conn = sqlite3.connect('escuela.db')
        cursor = conn.cursor()

        # Consultar estudiantes asignados al curso específico
        cursor.execute('''
            SELECT e.id, e.NOMBRES, e.APELLIDO_PATERNO, e.APELLIDO_MATERNO, ec.grado
            FROM estudiantes AS e
            INNER JOIN estudiantes_cursos AS ec ON e.id = ec.id_estudiante
            WHERE ec.id_curso = ?
        ''', (id_curso,))
        estudiantes = cursor.fetchall()

        # Mostrar los estudiantes en una ventana emergente
        if estudiantes:
            info = "Estudiantes asignados al curso:\n\n"
            for estudiante in estudiantes:
                info += f"ID: {estudiante[0]}, Nombre: {estudiante[1]} {estudiante[2]} {estudiante[3]}, Grado: {estudiante[4]}\n"
            messagebox.showinfo("Estudiantes Asignados", info)
        else:
            messagebox.showinfo("Estudiantes Asignados", "No hay estudiantes asignados a este curso.")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al consultar estudiantes: {e}")

    finally:
        if conn:
            conn.close()

# Interfaz gráfica usando Tkinter
class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Asignación de Cursos")
        self.geometry("500x400")

        # Crear los widgets
        self.frame_estudiantes = tk.Frame(self)
        self.frame_estudiantes.pack(pady=10)

        self.label_estudiantes = tk.Label(self.frame_estudiantes, text="Estudiantes:")
        self.label_estudiantes.grid(row=0, column=0, padx=10, pady=5)

        self.lista_estudiantes = tk.Listbox(self.frame_estudiantes, width=50, height=10)
        self.lista_estudiantes.grid(row=1, column=0, padx=10, pady=5)

        self.scroll_estudiantes = tk.Scrollbar(self.frame_estudiantes, orient=tk.VERTICAL, command=self.lista_estudiantes.yview)
        self.scroll_estudiantes.grid(row=1, column=1, sticky='ns')

        self.lista_estudiantes.config(yscrollcommand=self.scroll_estudiantes.set)

        self.frame_cursos = tk.Frame(self)
        self.frame_cursos.pack(pady=10)

        self.label_cursos = tk.Label(self.frame_cursos, text="Cursos:")
        self.label_cursos.grid(row=0, column=0, padx=10, pady=5)

        self.lista_cursos = tk.Listbox(self.frame_cursos, width=50, height=5)
        self.lista_cursos.grid(row=1, column=0, padx=10, pady=5)

        self.scroll_cursos = tk.Scrollbar(self.frame_cursos, orient=tk.VERTICAL, command=self.lista_cursos.yview)
        self.scroll_cursos.grid(row=1, column=1, sticky='ns')

        self.lista_cursos.config(yscrollcommand=self.scroll_cursos.set)

        self.frame_opciones = tk.Frame(self)
        self.frame_opciones.pack(pady=10)

        self.label_grado = tk.Label(self.frame_opciones, text="Grado:")
        self.label_grado.grid(row=0, column=0, padx=10, pady=5)

        self.entry_grado = tk.Entry(self.frame_opciones, width=30)
        self.entry_grado.grid(row=0, column=1, padx=10, pady=5)

        self.boton_asignar = tk.Button(self.frame_opciones, text="Asignar Curso", command=self.asignar_curso)
        self.boton_asignar.grid(row=0, column=2, padx=10, pady=5)

        self.boton_mostrar_estudiantes = tk.Button(self.frame_opciones, text="Mostrar Estudiantes", command=self.mostrar_estudiantes)
        self.boton_mostrar_estudiantes.grid(row=0, column=3, padx=10, pady=5)

        # Llenar las listas con datos
        self.cargar_estudiantes()
        self.cargar_cursos()

    def cargar_estudiantes(self):
        try:
            conn = sqlite3.connect('escuela.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id, NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO FROM estudiantes')
            estudiantes = cursor.fetchall()

            for estudiante in estudiantes:
                self.lista_estudiantes.insert(tk.END, f"{estudiante[1]} {estudiante[2]} {estudiante[3]}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {e}")

        finally:
            if conn:
                conn.close()

    def cargar_cursos(self):
        try:
            conn = sqlite3.connect('escuela.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id, NOMBRE FROM cursos')
            cursos = cursor.fetchall()

            for curso in cursos:
                self.lista_cursos.insert(tk.END, f"{curso[1]}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {e}")

        finally:
            if conn:
                conn.close()

    def asignar_curso(self):
        try:
            seleccion_estudiante = self.lista_estudiantes.curselection()
            seleccion_curso = self.lista_cursos.curselection()
            grado = self.entry_grado.get()

            if not seleccion_estudiante or not seleccion_curso or not grado:
                messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante, al menos un curso y un grado.")
                return

            id_estudiante = seleccion_estudiante[0] + 1  # Sumamos 1 porque los IDs de Listbox empiezan en 0
            id_curso = seleccion_curso[0] + 1            # Sumamos 1 porque los IDs de Listbox empiezan en 0

            asignar_cursos(id_estudiante, [id_curso], grado)
            self.limpiar_campos()
            self.cargar_estudiantes()

        except IndexError:
            messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante y un curso.")

    def mostrar_estudiantes(self):
        seleccion_curso = self.lista_cursos.curselection()

        if not seleccion_curso:
            messagebox.showwarning("Advertencia", "Por favor seleccione un curso para mostrar los estudiantes.")
            return

        id_curso = seleccion_curso[0] + 1  # Sumamos 1 porque los IDs de Listbox empiezan en 0
        mostrar_estudiantes_por_curso(id_curso)

    def limpiar_campos(self):
        self.lista_estudiantes.selection_clear(0, tk.END)
        self.lista_cursos.selection_clear(0, tk.END)
        self.entry_grado.delete(0, tk.END)

# Función principal para inicializar la aplicación
if __name__ == "__main__":
    crear_tablas()
    insertar_datos_ejemplo()

    app = Aplicacion()
    app.mainloop()
