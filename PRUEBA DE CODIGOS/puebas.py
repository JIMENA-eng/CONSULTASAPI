import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

class RegistroLoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro e Inicio de Sesión")

        # Inicializar base de datos
        self.conn = sqlite3.connect('usuarios.db')
        self.c = self.conn.cursor()
        self.create_table()

        # Variables de control
        self.usuario_var = tk.StringVar()
        self.correo_var = tk.StringVar()

        # Crear widgets
        self.label_usuario = tk.Label(root, text="Usuario:")
        self.label_usuario.grid(row=0, column=0, padx=10, pady=5)
        self.entry_usuario = tk.Entry(root, textvariable=self.usuario_var)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=5)

        self.label_correo = tk.Label(root, text="Correo Electrónico:")
        self.label_correo.grid(row=1, column=0, padx=10, pady=5)
        self.entry_correo = tk.Entry(root, textvariable=self.correo_var)
        self.entry_correo.grid(row=1, column=1, padx=10, pady=5)

        self.btn_registro = tk.Button(root, text="Registrarse", command=self.registrar_usuario)
        self.btn_registro.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL UNIQUE,
                            correo TEXT NOT NULL UNIQUE,
                            contrasena TEXT NOT NULL
                            )''')
        self.conn.commit()

    def generar_contrasena_unica(self):
        # Generar una contraseña única de 6 dígitos
        return str(random.randint(100000, 999999))

    def registrar_usuario(self):
        usuario = self.usuario_var.get().strip()
        correo = self.correo_var.get().strip()

        if usuario and correo:
            # Generar una contraseña única de 6 dígitos
            contrasena_unica = self.generar_contrasena_unica()

            # Guardar la contraseña única en la base de datos (sin encriptar para este ejemplo)
            try:
                self.c.execute("INSERT INTO usuarios (usuario, correo, contrasena) VALUES (?, ?, ?)",
                               (usuario, correo, contrasena_unica))
                self.conn.commit()

                messagebox.showinfo("Registro Exitoso", f"Usuario registrado correctamente.\nTu contraseña única es: {contrasena_unica}")
                self.entry_usuario.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El usuario o correo electrónico ya existe. Por favor, elija otro.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def iniciar_sesion(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.correo_var.get().strip()  # Utilizamos el campo de correo para ingresar la contraseña única

        if usuario and contrasena:
            # Verificar si el usuario y la contraseña coinciden en la base de datos
            self.c.execute("SELECT contrasena FROM usuarios WHERE usuario=?", (usuario,))
            resultado = self.c.fetchone()

            if resultado and resultado[0] == contrasena:
                messagebox.showinfo("Inicio de Sesión Exitoso", f"Bienvenido, {usuario}!")
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroLoginGUI(root)
    root.mainloop()

