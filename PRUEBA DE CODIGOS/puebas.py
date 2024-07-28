import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def setup_databases():
    # Crear o modificar la base de datos de asistencia
    conn_asistencia = sqlite3.connect('asistencia.db')
    cursor_asistencia = conn_asistencia.cursor()
    
    # Crear tabla de asistencia si no existe
    cursor_asistencia.execute('''CREATE TABLE IF NOT EXISTS asistencia (
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

    # Agregar columna 'nota' a la tabla de asistencia si no existe
    try:
        cursor_asistencia.execute("ALTER TABLE asistencia ADD COLUMN nota TEXT")
    except sqlite3.OperationalError:
        pass  # La columna ya existe o no se puede agregar

    conn_asistencia.commit()
    conn_asistencia.close()
    
    # Crear tabla de matricula si no existe en la base de datos matriculas
    conn_matriculas = sqlite3.connect('matriculas.db')
    cursor_matriculas = conn_matriculas.cursor()
    
    cursor_matriculas.execute('''CREATE TABLE IF NOT EXISTS matricula (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                grado TEXT
                                )''')
    
    conn_matriculas.commit()
    conn_matriculas.close()

def buscar_asistencias(grado):
    if not grado:
        messagebox.showerror("Error", "Por favor, ingrese un grado.")
        return
    
    conn_asistencia = sqlite3.connect('asistencia.db')
    cursor_asistencia = conn_asistencia.cursor()
    
    conn_matriculas = sqlite3.connect('matriculas.db')
    cursor_matriculas = conn_matriculas.cursor()
    
    # Obtener IDs de estudiantes en el grado dado
    cursor_matriculas.execute("SELECT id FROM matricula WHERE grado = ?", (grado,))
    ids_estudiantes = cursor_matriculas.fetchall()
    
    if not ids_estudiantes:
        messagebox.showinfo("Resultado", "No se encontraron estudiantes en este grado.")
        conn_asistencia.close()
        conn_matriculas.close()
        return
    
    ids_estudiantes = [id[0] for id in ids_estudiantes]
    placeholder = ','.join('?' * len(ids_estudiantes))
    
    # Obtener asistencias para los IDs de estudiantes
    query = f'''
    SELECT m.nombre, a.fecha, a.lunes, a.martes, a.miércoles, a.jueves, a.viernes
    FROM asistencia a
    JOIN matricula m ON a.id_estudiante = m.id
    WHERE a.id_estudiante IN ({placeholder})
    '''
    
    cursor_asistencia.execute(query, ids_estudiantes)
    resultados = cursor_asistencia.fetchall()
    
    conn_asistencia.close()
    conn_matriculas.close()
    
    # Limpiar el árbol
    for item in tree.get_children():
        tree.delete(item)
    
    # Insertar resultados en el árbol
    for resultado in resultados:
        nombre, fecha, lunes, martes, miercoles, jueves, viernes = resultado
        tree.insert("", tk.END, values=(nombre, fecha, "Sí" if lunes else "No", "Sí" if martes else "No", 
                                        "Sí" if miercoles else "No", "Sí" if jueves else "No", 
                                        "Sí" if viernes else "No"))

# Crear la ventana principal
root = tk.Tk()
root.title("Buscar Asistencias por Grado")

# Configuración inicial de la base de datos
setup_databases()

# Crear un frame para la entrada
frame_entrada = tk.Frame(root)
frame_entrada.pack(padx=10, pady=10)

# Etiqueta y entrada para el grado
label_grado = tk.Label(frame_entrada, text="Grado:")
label_grado.grid(row=0, column=0, padx=5, pady=5)
entry_grado = tk.Entry(frame_entrada)
entry_grado.grid(row=0, column=1, padx=5, pady=5)

# Botón para buscar
btn_buscar = tk.Button(frame_entrada, text="Buscar", command=lambda: buscar_asistencias(entry_grado.get()))
btn_buscar.grid(row=1, columnspan=2, pady=10)

# Crear el árbol para mostrar resultados
columns = ("Nombre", "Fecha", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("Nombre", text="Nombre")
tree.heading("Fecha", text="Fecha")
tree.heading("Lunes", text="Lunes")
tree.heading("Martes", text="Martes")
tree.heading("Miércoles", text="Miércoles")
tree.heading("Jueves", text="Jueves")
tree.heading("Viernes", text="Viernes")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Ejecutar la aplicación
root.mainloop()
