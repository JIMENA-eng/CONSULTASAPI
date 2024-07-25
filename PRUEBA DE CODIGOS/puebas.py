import tkinter as tk
from tkinter import messagebox
import sqlite3

import tkinter as tk
from tkinter import messagebox
import sqlite3

class RegistroEmpleadosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Empleados")

        # Inicializar base de datos
        self.conn = sqlite3.connect("asistencia.db")
        self.c = self.conn.cursor()

        # Crear widgets
        self.label_dni = tk.Label(root, text="Ingrese DNI del Empleado:")
        self.label_dni.grid(row=0, column=0, padx=10, pady=5)
        self.entry_dni = tk.Entry(root)
        self.entry_dni.grid(row=0, column=1, padx=10, pady=5)

        self.btn_buscar = tk.Button(root, text="Buscar Empleado", command=self.buscar_empleado)
        self.btn_buscar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
        self.resultado_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar_empleado(self):
        dni = self.entry_dni.get()

        if dni:
            self.c.execute("SELECT * FROM empleados WHERE DNI=?", (dni,))
            empleado = self.c.fetchone()
            if empleado:
                resultado = f"ID: {empleado[0]}\n"
                resultado += f"Nombres: {empleado[1]}\n"
                resultado += f"Apellido Paterno: {empleado[2]}\n"
                resultado += f"Apellido Materno: {empleado[3]}\n"
                resultado += f"DNI: {empleado[4]}\n"
                resultado += f"Género: {empleado[5]}\n"
                resultado += f"Estado Civil: {empleado[6]}\n"
                resultado += f"Fecha y Hora: {empleado[7]}"
            else:
                resultado = f"No se encontró ningún empleado con el DNI {dni}."
            self.resultado_text.delete(1.0, tk.END)  # Limpiar resultados anteriores
            self.resultado_text.insert(tk.END, resultado)
        else:
            messagebox.showerror("Error", "Por favor, ingrese el DNI del empleado.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroEmpleadosGUI(root)
    root.mainloop()