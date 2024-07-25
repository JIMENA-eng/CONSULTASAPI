import tkinter as tk
import tkinter.messagebox as messagebox
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

# Función para registrar datos del DNI en la base de datos
def registrar_dni(dni):
    # Simulamos la consulta a un servicio web que devuelve los nombres y apellidos
    # Aquí se debería realizar una solicitud real a un servicio web de la RENIEC u otro proveedor autorizado
    # En este ejemplo, suponemos una respuesta ficticia
    nombres = "Juan Carlos"
    apellidos = "Pérez Gómez"
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect('dni_registros.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (nombres, apellidos, dni, fecha_registro)
        VALUES (?, ?, ?, ?)
    ''', (nombres, apellidos, dni, fecha_registro))
    
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Registro Exitoso", "Registro exitoso en la base de datos.")

# Función para manejar el evento del botón de registro
def on_registrar():
    dni = entry_dni.get().strip()
    if dni.isdigit() and len(dni) == 8:  # Validar que el DNI tenga 8 dígitos
        registrar_dni(dni)
    else:
        messagebox.showerror("Error", "Por favor, ingrese un número de DNI válido (8 dígitos numéricos).")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Registro de DNI")

# Crear la tabla si no existe al inicio del programa
crear_tabla()

# Frame principal
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Etiqueta y entrada para ingresar el DNI
label_dni = tk.Label(frame, text="Número de DNI:")
label_dni.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

entry_dni = tk.Entry(frame, width=20)
entry_dni.grid(row=0, column=1, padx=10, pady=5)

# Botón para registrar el DNI
btn_registrar = tk.Button(frame, text="Registrar", command=on_registrar)
btn_registrar.grid(row=1, column=0, columnspan=2, pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
