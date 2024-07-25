import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Función para crear la base de datos y las tablas
def crear_base_de_datos():
    try:
        conn = sqlite3.connect('escuela.db')
        cursor = conn.cursor()

        # Crear tabla de grados si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')

        # Crear tabla de cursos si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                grado_id INTEGER,
                FOREIGN KEY (grado_id) REFERENCES grados(id)
            )
        ''')

        # Insertar datos de ejemplo de grados si la tabla está vacía
        cursor.execute('SELECT * FROM grados')
        if not cursor.fetchall():
            grados = [
                ('I',),
                ('II',),
                ('III',),
                ('IV',),
                ('V',),
                ('VI',),
                ('VII',),
                ('VIII',),
                ('IX',),
                ('X',)
            ]
            cursor.executemany('INSERT INTO grados (nombre) VALUES (?)', grados)

        # Insertar datos de ejemplo de cursos si la tabla está vacía
        cursor.execute('SELECT * FROM cursos')
        if not cursor.fetchall():
            cursos = [
                ('Matemáticas', 1),  # Curso de Matemáticas asociado al grado I
                ('Ciencias Naturales', 2),  # Curso de Ciencias Naturales asociado al grado II
                ('Historia', 3),  # Curso de Historia asociado al grado III
                ('Literatura', 4),  # Curso de Literatura asociado al grado IV
                ('Geografía', 5),  # Curso de Geografía asociado al grado V
                ('Arte', 6),  # Curso de Arte asociado al grado VI
                ('Música', 7),  # Curso de Música asociado al grado VII
                ('Educación Física', 8),  # Curso de Educación Física asociado al grado VIII
                ('Informática', 9),  # Curso de Informática asociado al grado IX
                ('Educación Cívica', 10)  # Curso de Educación Cívica asociado al grado X
            ]
            cursor.executemany('INSERT INTO cursos (nombre, grado_id) VALUES (?, ?)', cursos)

        conn.commit()
        print("Base de datos y tablas creadas correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")

    finally:
        if conn:
            conn.close()

# Llamar a la función para crear la base de datos y las tablas
crear_base_de_datos()

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Selección de Grado y Cursos")
        self.geometry("400x300")

        self.label_grado = tk.Label(self, text="Seleccione un grado:")
        self.label_grado.pack(pady=10)

        # Obtener los grados desde la base de datos
        self.grados = self.obtener_grados_desde_db()

        # Crear un Combobox para seleccionar el grado
        self.combobox_grados = ttk.Combobox(self, values=self.grados, state="readonly")
        self.combobox_grados.pack(pady=10)
        self.combobox_grados.bind("<<ComboboxSelected>>", self.actualizar_lista_cursos)

        self.label_cursos = tk.Label(self, text="Cursos del grado seleccionado:")
        self.label_cursos.pack(pady=10)

        # Crear una Listbox para mostrar los cursos
        self.lista_cursos = tk.Listbox(self, width=50, height=10)
        self.lista_cursos.pack(padx=10, pady=10)

        self.cargar_cursos_iniciales()

    def obtener_grados_desde_db(self):
        try:
            conn = sqlite3.connect('escuela.db')
            cursor = conn.cursor()

            cursor.execute('SELECT nombre FROM grados')
            grados = [row[0] for row in cursor.fetchall()]

            return grados

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener los grados: {e}")

        finally:
            if conn:
                conn.close()

    def cargar_cursos_iniciales(self):
        try:
            conn = sqlite3.connect('escuela.db')
            cursor = conn.cursor()

            # Obtener los cursos asociados al primer grado inicialmente
            cursor.execute('''
                SELECT cursos.nombre
                FROM cursos
                INNER JOIN grados ON cursos.grado_id = grados.id
                WHERE grados.nombre = ?
            ''', (self.grados[0],))

            cursos = [row[0] for row in cursor.fetchall()]
            self.actualizar_lista_cursos(cursos)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los cursos: {e}")

        finally:
            if conn:
                conn.close()

    def actualizar_lista_cursos(self, event):
        seleccion_grado = self.combobox_grados.get()

        try:
            conn = sqlite3.connect('escuela.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT cursos.nombre
                FROM cursos
                INNER JOIN grados ON cursos.grado_id = grados.id
                WHERE grados.nombre = ?
            ''', (seleccion_grado,))

            cursos = [row[0] for row in cursor.fetchall()]
            self.lista_cursos.delete(0, tk.END)  # Limpiar la lista antes de actualizar
            for curso in cursos:
                self.lista_cursos.insert(tk.END, curso)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar los cursos: {e}")

        finally:
            if conn:
                conn.close()

# Función principal para inicializar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
