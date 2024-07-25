import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import secrets

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
        self.contrasena_var = tk.StringVar()

        # Crear widgets
        self.label_usuario = tk.Label(root, text="Usuario:")
        self.label_usuario.grid(row=0, column=0, padx=10, pady=5)
        self.entry_usuario = tk.Entry(root, textvariable=self.usuario_var)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=5)

        self.label_contrasena = tk.Label(root, text="Contraseña:")
        self.label_contrasena.grid(row=1, column=0, padx=10, pady=5)
        self.entry_contrasena = tk.Entry(root, textvariable=self.contrasena_var, show='*')
        self.entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

        self.btn_registro = tk.Button(root, text="Registrarse", command=self.registrar_usuario)
        self.btn_registro.grid(row=2, column=0, padx=10, pady=10, sticky="WE")

        self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_login.grid(row=2, column=1, padx=10, pady=10, sticky="WE")

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL UNIQUE,
                            codigo TEXT NOT NULL UNIQUE,
                            contrasena TEXT NOT NULL
                            )''')
        self.conn.commit()

    def registrar_usuario(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()

        if usuario and contrasena:
            # Generar un código único para el usuario
            codigo = secrets.token_hex(8)  # Genera un código hexadecimal de 8 bytes

            # Encriptar la contraseña usando hash SHA-256
            hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

            try:
                self.c.execute("INSERT INTO usuarios (usuario, codigo, contrasena) VALUES (?, ?, ?)",
                               (usuario, codigo, hash_contrasena))
                self.conn.commit()
                messagebox.showinfo("Registro Exitoso", f"Usuario registrado correctamente.\nSu código único es: {codigo}")
                self.entry_usuario.delete(0, tk.END)
                self.entry_contrasena.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El usuario ya existe. Por favor, elija otro nombre de usuario.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def iniciar_sesion(self):
        usuario = self.usuario_var.get().strip()
        contrasena = self.contrasena_var.get().strip()

        if usuario and contrasena:
            # Encriptar la contraseña ingresada para compararla con la almacenada en la base de datos
            hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

            self.c.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?",
                           (usuario, hash_contrasena))
            usuario_registrado = self.c.fetchone()

            if usuario_registrado:
                messagebox.showinfo("Inicio de Sesión Exitoso", f"Bienvenido, {usuario}!")
                # Aquí podrías abrir una nueva ventana o realizar otras acciones después del inicio de sesión exitoso
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroLoginGUI(root)
    root.mainloop()
