import sqlite3
import tkinter as tk
from tkinter import messagebox

# Variables globales para almacenar listas de estudiantes y cursos
lista_estudiantes = None
lista_cursos = None

# Función para crear la tabla estudiantes, cursos y la tabla de relación estudiantes_cursos si no existen
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

    # Crear tabla de relación estudiantes_cursos si no existe
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

# Función para insertar datos de ejemplo en la tabla estudiantes y cursos
def insertar_datos_ejemplo():
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    # Insertar datos de ejemplo en la tabla estudiantes
    estudiantes = [
        ('Juan', 'Pérez', 'García', '12345678', 'Masculino', 'Soltero', '2023-01-01 08:00:00'),
        ('María', 'López', 'Martínez', '87654321', 'Femenino', 'Casado', '2023-01-02 09:00:00'),
        ('Pedro', 'Gómez', 'Fernández', '56789123', 'Masculino', 'Divorciado', '2023-01-03 10:00:00'),
        ('Ana', 'Rodríguez', 'Sánchez', '43218765', 'Femenino', 'Soltero', '2023-01-04 11:00:00'),
    ]

    cursor.executemany('''
        INSERT INTO estudiantes (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', estudiantes)

    # Insertar datos de ejemplo en la tabla cursos
    cursos = [
        ('Matemáticas', 'Curso avanzado de matemáticas'),
        ('Literatura', 'Curso de literatura moderna'),
        ('Programación', 'Curso introductorio a la programación'),
    ]

    cursor.executemany('''
        INSERT INTO cursos (NOMBRE, DESCRIPCION)
        VALUES (?, ?)
    ''', cursos)

    conn.commit()
    conn.close()

# Función para consultar estudiantes y cursos
def consultar_estudiantes():
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, NOMBRES, APELLIDO_PATERNO FROM estudiantes ORDER BY APELLIDO_PATERNO, NOMBRES')
    estudiantes = cursor.fetchall()

    cursor.execute('SELECT id, NOMBRE FROM cursos')
    cursos = cursor.fetchall()

    conn.close()
    
    return estudiantes, cursos

# Función para obtener los cursos asignados a un estudiante
def obtener_cursos_asignados(id_estudiante):
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT cursos.id, cursos.NOMBRE, estudiantes_cursos.grado
        FROM cursos
        INNER JOIN estudiantes_cursos ON cursos.id = estudiantes_cursos.id_curso
        WHERE estudiantes_cursos.id_estudiante = ?
    ''', (id_estudiante,))

    cursos_asignados = cursor.fetchall()

    conn.close()

    return cursos_asignados

# Función para asignar cursos a un estudiante con un grado específico
def asignar_cursos(id_estudiante, cursos_seleccionados, grados_seleccionados):
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    # Eliminar todas las asignaciones previas del estudiante
    cursor.execute('DELETE FROM estudiantes_cursos WHERE id_estudiante = ?', (id_estudiante,))

    # Insertar los nuevos cursos asignados con los grados correspondientes
    for idx, id_curso in enumerate(cursos_seleccionados):
        id_grado = grados_seleccionados[idx]
        cursor.execute('''
            INSERT INTO estudiantes_cursos (id_estudiante, id_curso, grado)
            VALUES (?, ?, ?)
        ''', (id_estudiante, id_curso, id_grado))

    conn.commit()
    conn.close()

# Función para obtener todos los estudiantes asignados por cursos
def obtener_estudiantes_por_cursos():
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT estudiantes.id, estudiantes.NOMBRES, estudiantes.APELLIDO_PATERNO, cursos.NOMBRE, estudiantes_cursos.grado
        FROM estudiantes
        INNER JOIN estudiantes_cursos ON estudiantes.id = estudiantes_cursos.id_estudiante
        INNER JOIN cursos ON cursos.id = estudiantes_cursos.id_curso
        ORDER BY cursos.NOMBRE, estudiantes.APELLIDO_PATERNO, estudiantes.NOMBRES
    ''')

    estudiantes_por_cursos = cursor.fetchall()

    conn.close()

    return estudiantes_por_cursos

# Función para mostrar los estudiantes asignados por cursos
def mostrar_estudiantes_asignados():
    estudiantes_por_cursos = obtener_estudiantes_por_cursos()

    if estudiantes_por_cursos:
        texto = "Estudiantes asignados por cursos:\n\n"
        curso_actual = None

        for estudiante in estudiantes_por_cursos:
            id_estudiante, nombres, apellido_paterno, nombre_curso, grado = estudiante

            if nombre_curso != curso_actual:
                texto += f"Curso: {nombre_curso}\n"
                curso_actual = nombre_curso

            texto += f"  - {nombres} {apellido_paterno} (Grado: {grado})\n"

        messagebox.showinfo("Estudiantes por cursos", texto)
    else:
        messagebox.showinfo("Estudiantes por cursos", "No hay estudiantes asignados a cursos.")

# Función para manejar la asignación de cursos desde la interfaz gráfica
def asignar_curso():
    global lista_estudiantes, lista_cursos

    if lista_estudiantes and lista_cursos:
        estudiante_seleccionado = lista_estudiantes.get(tk.ACTIVE)
        cursos_seleccionados = [lista_cursos.get(idx).split(':')[0] for idx in lista_cursos.curselection()]
        grados_seleccionados = [grados_combo[idx].get() for idx in lista_cursos.curselection()]

        if estudiante_seleccionado and cursos_seleccionados:
            id_estudiante = estudiante_seleccionado.split(':')[0]

            asignar_cursos(id_estudiante, cursos_seleccionados, grados_seleccionados)

            messagebox.showinfo("Asignación de cursos", "Cursos asignados correctamente al estudiante.")
        else:
            messagebox.showwarning("Asignación de cursos", "Por favor, selecciona un estudiante y al menos un curso.")
    else:
        messagebox.showwarning("Asignación de cursos", "No se han cargado los datos de estudiantes y cursos.")

# Función para agregar un nuevo curso a la base de datos
def agregar_curso(nombre_curso, descripcion_curso):
    conn = sqlite3.connect('escuela.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO cursos (NOMBRE, DESCRIPCION)
        VALUES (?, ?)
    ''', (nombre_curso, descripcion_curso))

    conn.commit()
    conn.close()

# Función para actualizar la lista de cursos en la interfaz gráfica
def actualizar_lista_cursos():
    global lista_cursos

    cursos = consultar_estudiantes()[1]  # Obtener la lista de cursos actualizada

    if lista_cursos:
        lista_cursos.delete(0, tk.END)  # Limpiar la lista actual

        for curso in cursos:
            id_curso, nombre_curso = curso
            texto_curso = f"{id_curso}: {nombre_curso}"
            lista_cursos.insert(tk.END, texto_curso)

# Función para mostrar la interfaz gráfica
def mostrar_interfaz():
    global lista_estudiantes, lista_cursos, grados_combo

    root = tk.Tk()
    root.title("Asignación de Estudiantes a Cursos")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label_titulo = tk.Label(frame, text="Asignación de Estudiantes a Cursos")
    label_titulo.pack()

    # Consultar estudiantes y cursos desde la base de datos
    estudiantes, cursos = consultar_estudiantes()

    # Lista de estudiantes
    label_estudiantes = tk.Label(frame, text="Estudiantes:")
    label_estudiantes.pack()

    scrollbar_estudiantes = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar_estudiantes.pack(side=tk.RIGHT, fill=tk.Y)

    lista_estudiantes = tk.Listbox(frame, yscrollcommand=scrollbar_estudiantes.set)
    lista_estudiantes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for estudiante in estudiantes:
        id_estudiante, nombres, apellido_paterno = estudiante
        texto_estudiante = f"{id_estudiante}: {nombres} {apellido_paterno}"
        lista_estudiantes.insert(tk.END, texto_estudiante)

    scrollbar_estudiantes.config(command=lista_estudiantes.yview)

    # Lista de cursos con grados
    label_cursos = tk.Label(frame, text="Cursos:")
    label_cursos.pack()

    scrollbar_cursos = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar_cursos.pack(side=tk.RIGHT, fill=tk.Y)

    lista_cursos = tk.Listbox(frame, yscrollcommand=scrollbar_cursos.set, selectmode=tk.MULTIPLE)
    lista_cursos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    grados_combo = []

    for curso in cursos:
        id_curso, nombre_curso = curso
        texto_curso = f"{id_curso}: {nombre_curso}"
        lista_cursos.insert(tk.END, texto_curso)

        # Agregar combobox para seleccionar el grado
        frame_grado = tk.Frame(root)
        frame_grado.pack()

        label_grado = tk.Label(frame_grado, text="Grado:")
        label_grado.pack(side=tk.LEFT)

        grados = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
        combo_grado = tk.StringVar()
        combo_grado.set("I")  # Establecer el grado por defecto
        combo = tk.OptionMenu(frame_grado, combo_grado, *grados)
        combo.pack(side=tk.LEFT)

        grados_combo.append(combo_grado)

    scrollbar_cursos.config(command=lista_cursos.yview)

    # Botón para asignar cursos
    boton_asignar = tk.Button(root, text="Asignar cursos", command=asignar_curso)
    boton_asignar.pack(pady=10)

    # Marco y campos para agregar nuevo curso
    frame_agregar_curso = tk.Frame(root, bd=1, relief=tk.RIDGE)
    frame_agregar_curso.pack(pady=10)

    label_nuevo_curso = tk.Label(frame_agregar_curso, text="Agregar nuevo curso:")
    label_nuevo_curso.grid(row=0, column=0, padx=5, pady=5)

    label_nombre_curso = tk.Label(frame_agregar_curso, text="Nombre:")
    label_nombre_curso.grid(row=1, column=0, padx=5, pady=5)

    entry_nombre_curso = tk.Entry(frame_agregar_curso, width=30)
    entry_nombre_curso.grid(row=1, column=1, padx=5)

    label_descripcion_curso = tk.Label(frame_agregar_curso, text="Descripción:")
    label_descripcion_curso.grid(row=2, column=0, padx=5, pady=5)

    entry_descripcion_curso = tk.Entry(frame_agregar_curso, width=30)
    entry_descripcion_curso.grid(row=2, column=1, padx=5)

    boton_agregar_curso = tk.Button(frame_agregar_curso, text="Agregar curso", command=lambda: agregar_curso(entry_nombre_curso.get(), entry_descripcion_curso.get()))
    boton_agregar_curso.grid(row=3, columnspan=2, pady=5)

    # Botón para actualizar la lista de cursos
    boton_actualizar_cursos = tk.Button(root, text="Actualizar cursos", command=actualizar_lista_cursos)
    boton_actualizar_cursos.pack(pady=10)

    # Botón para mostrar estudiantes asignados por cursos
    boton_mostrar_estudiantes = tk.Button(root, text="Mostrar Estudiantes por Cursos", command=mostrar_estudiantes_asignados)
    boton_mostrar_estudiantes.pack(pady=10)

    # Botón para salir
    boton_salir = tk.Button(root, text="Salir", command=root.quit)
    boton_salir.pack(pady=10)

    root.mainloop()

# Crear las tablas y insertar datos de ejemplo si no existen
crear_tablas()
insertar_datos_ejemplo()

# Mostrar la interfaz gráfica para asignar estudiantes a cursos
mostrar_interfaz()
