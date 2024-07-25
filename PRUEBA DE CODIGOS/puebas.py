import tkinter as tk
from tkinter import ttk, messagebox
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
def registrar_dni_gui():
    nombres = entry_nombres.get().strip()
    apellidos = entry_apellidos.get().strip()
    dni = entry_dni.get().strip()
    dni_completo = f"{dni}{'X' if len(dni) == 7 else ''}"  # Agrega la 'X' si el DNI es de 7 dígitos
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if nombres and apellidos and dni:
        conn = sqlite3.connect('dni_registros.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registros (nombres, apellidos, dni, fecha_registro)
            VALUES (?, ?, ?, ?)
        ''', (nombres, apellidos, dni_completo, fecha_registro))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Registro Exitoso", "Registro exitoso en la base de datos.")
        
        # Limpiar los campos después del registro exitoso
        entry_nombres.delete(0, tk.END)
        entry_apellidos.delete(0, tk.END)
        entry_dni.delete(0, tk.END)
        
        # Actualizar el Treeview con los nuevos registros
        actualizar_treeview()
    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")

# Función para actualizar el Treeview con los registros de la base de datos
def actualizar_treeview():
    # Limpiar Treeview antes de actualizar
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Conectar a la base de datos y obtener los registros
    conn = sqlite3.connect('dni_registros.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()
    
    # Insertar registros en el Treeview
    for registro in registros:
        treeview.insert('', 'end', values=registro)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Registro de DNI")

# Crear la tabla si no existe al inicio del programa
crear_tabla()

# Frame principal
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Etiquetas y entradas para ingresar datos del DNI
label_nombres = tk.Label(frame, text="Nombres:")
label_nombres.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

entry_nombres = tk.Entry(frame, width=30)
entry_nombres.grid(row=0, column=1, padx=10, pady=5)

label_apellidos = tk.Label(frame, text="Apellidos:")
label_apellidos.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

entry_apellidos = tk.Entry(frame, width=30)
entry_apellidos.grid(row=1, column=1, padx=10, pady=5)

label_dni = tk.Label(frame, text="Número de DNI:")
label_dni.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

entry_dni = tk.Entry(frame, width=20)
entry_dni.grid(row=2, column=1, padx=10, pady=5)

# Botón para registrar el DNI
btn_registrar = tk.Button(frame, text="Registrar", command=registrar_dni_gui)
btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)

# Crear Treeview
treeview_frame = tk.Frame(root)
treeview_frame.pack(padx=10, pady=10)

columns = ('#1', '#2', '#3', '#4', '#5')
treeview = ttk.Treeview(treeview_frame, columns=columns, show='headings')
treeview.heading('#1', text='ID')
treeview.heading('#2', text='Nombres')
treeview.heading('#3', text='Apellidos')
treeview.heading('#4', text='DNI')
treeview.heading('#5', text='Fecha de Registro')
treeview.pack()

# Actualizar Treeview con los registros actuales
actualizar_treeview()

# Ejecutar la interfaz gráfica
root.mainloop()
