import sqlite3
from datetime import datetime

# Función para crear la tabla si no existe
def crear_tabla():
    conn = sqlite3.connect('dni_registros.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombres TEXT,
            apellidos TEXT,
            dni TEXT,
            fecha_registro TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para ingresar datos del DNI y registrar en la base de datos
def registrar_dni():
    nombres = input("Ingrese nombres: ")
    apellidos = input("Ingrese apellidos: ")
    dni = input("Ingrese número de DNI (sin letra): ")
    dni_completo = f"{dni}{'X' if len(dni) == 7 else ''}"  # Agrega la 'X' si el DNI es de 7 dígitos
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('dni_registros.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (nombres, apellidos, dni, fecha_registro)
        VALUES (?, ?, ?, ?)
    ''', (nombres, apellidos, dni_completo, fecha_registro))
    
    conn.commit()
    conn.close()
    
    print("Registro exitoso en la base de datos.")

# Crear la tabla si no existe al inicio del programa
crear_tabla()

# Ejecutar la función para registrar un DNI
registrar_dni()
