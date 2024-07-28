from tkinter import*
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import requests
import datetime
from fpdf import FPDF
import xlsxwriter
from datetime import datetime,timedelta
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import tempfile
import pandas as pd
import random



def inicio_dmin():
    top.destroy()
    root=Tk()
    root.title("ADMINISTRADOR INICIO DE SESION")
    root.geometry("400x350")
    root.configure(background='lightblue')
    
    lb_usuario=tk.Label(root, text='USUARIO:',bg='lightblue')
    lb_usuario.grid(row=0, padx=10,pady=5, sticky=tk.W)
    en_usuario=tk.Entry(root)
    en_usuario.grid(row=0, column=1, padx=10, pady=5)
    
    lb_contraseña=tk.Label(root, text='CONTRASEÑA:',bg='lightblue')
    lb_contraseña.grid(row=1, column=0, padx=10, pady=5)
    en_contraseña=tk.Entry(root, show='*')
    en_contraseña.grid(row=1, column=1,padx=10, pady=5)
    
    def ver_admin():
        usuario=en_usuario.get()
        contraseña=en_contraseña.get()
        
        if usuario == 'admin' and contraseña == 'admin123':
            root.destroy()
            
            ventana_administrador()
        else:
            messagebox.showerror('ERROR', 'USUARIO Y CONTRASEÑA INCORRECTA')
    
    bt_inicio=tk.Button(root, text='INICIAR SESION', command=ver_admin)
    bt_inicio.grid(row=2, columnspan=2, padx=10, pady=10)
    
def inicio_usuario():
    top.destroy()
    class RegistroLoginGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Registro e Inicio de Sesión")

            # Inicializar base de datos
            self.conn = sqlite3.connect('usuarios.bd')
            self.c = self.conn.cursor()
            self.create_table()

            # Variables de control
            self.usuario_var = tk.StringVar()
            self.correo_var = tk.StringVar()
            self.grado_var = tk.StringVar()

            # Crear widgets
            self.label_usuario = tk.Label(root, text="Usuario:")
            self.label_usuario.grid(row=0, column=0, padx=10, pady=5)
            self.entry_usuario = tk.Entry(root, textvariable=self.usuario_var)
            self.entry_usuario.grid(row=0, column=1, padx=10, pady=5)

            self.label_correo = tk.Label(root, text="Correo Electrónico:")
            self.label_correo.grid(row=1, column=0, padx=10, pady=5)
            self.entry_correo = tk.Entry(root, textvariable=self.correo_var)
            self.entry_correo.grid(row=1, column=1, padx=10, pady=5)

            self.label_grado = tk.Label(root, text="Grado a Enseñar:")
            self.label_grado.grid(row=2, column=0, padx=10, pady=5)
            self.entry_grado = tk.Entry(root, textvariable=self.grado_var)
            self.entry_grado.grid(row=2, column=1, padx=10, pady=5)

            self.btn_registro = tk.Button(root, text="Registrarse", command=self.registrar_usuario)
            self.btn_registro.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

            self.btn_login = tk.Button(root, text="Iniciar Sesión", command=self.iniciar_sesion)
            self.btn_login.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

        def create_table(self):
            self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL UNIQUE,
                                correo TEXT NOT NULL UNIQUE,
                                grado TEXT NOT NULL,
                                contrasena TEXT NOT NULL
                                )''')
            self.conn.commit()

        def generar_contrasena_unica(self):
            # Generar una contraseña única de 6 dígitos
            return str(random.randint(100000, 999999))

        def registrar_usuario(self):
            usuario = self.usuario_var.get().strip()
            correo = self.correo_var.get().strip()
            grado = self.grado_var.get().strip()

            if usuario and correo and grado:
                # Generar una contraseña única de 6 dígitos
                contrasena_unica = self.generar_contrasena_unica()

                # Guardar la contraseña única en la base de datos (sin encriptar para este ejemplo)
                try:
                    self.c.execute("INSERT INTO usuarios (usuario, correo, grado, contrasena) VALUES (?, ?, ?, ?)",
                                (usuario, correo, grado, contrasena_unica))
                    self.conn.commit()

                    messagebox.showinfo("Registro Exitoso", f"Usuario registrado correctamente.\nTu contraseña única es: {contrasena_unica}")
                    self.entry_usuario.delete(0, tk.END)
                    self.entry_correo.delete(0, tk.END)
                    self.entry_grado.delete(0, tk.END)
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
                    # Aquí deberías reemplazar MATRIX() con la función o clase que maneja el acceso tras el inicio de sesión
                    # MATRIX()
                    MATRIX_DOCENTE()
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


top=Tk()
top.title('seleciona tipo de usuario' )
top.geometry("500x300")
top.configure(background='lightblue')

lb_user = tk.Label(top, text='SELECCIONE SU INICIO DE SESION:', bg='lightblue')
lb_user.pack()
bt_admin=tk.Button(top, text='INICIAR SESION COMO ADMINISTRADOR', command=inicio_dmin, bg='lightblue')
bt_admin.pack(pady=20)
bt_usuario=tk.Button(top, text='INICIAR SESION COMO USUARIO', command=inicio_usuario, bg='lightblue')
bt_usuario.pack(pady=20)

def DNI():
    def dni_consultar():
        dni = en_dni.get()
        if not dni:
            messagebox.showwarning('Advertencia', 'Por favor ingrese un número de DNI')
            return
        try:
            url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            if response.status_code == 200:
                if not data['success']:
                    messagebox.showinfo("DNI no registrado", "El DNI no se encuentra registrado")
                else:
                    mostrar_datos(data)
            else:
                messagebox.showerror("Error en la consulta", f"Código de estado: {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error en la consulta", f"Error de conexión: {str(e)}")

    def mostrar_datos(data):
        wen.destroy()
        ven_da = tk.Toplevel()
        ven_da.title('DATOS DEL DNI')
        ven_da.geometry("500x600")
        ven_da.configure(background='lightblue')

        ttk.Label(ven_da, text=f'DNI: {data["dni"]}').pack(padx=10, pady=5)
        ttk.Label(ven_da, text=f'Nombres: {data["nombres"]}').pack(padx=10, pady=5)
        ttk.Label(ven_da, text=f'Apellido Paterno: {data["apellidoPaterno"]}').pack(padx=10, pady=5)
        ttk.Label(ven_da, text=f'Apellido Materno: {data["apellidoMaterno"]}').pack(padx=10, pady=5)

        # Sección para ingresar el estado civil
        frame_estado_civil = ttk.LabelFrame(ven_da, text="Estado Civil")
        frame_estado_civil.pack(padx=10, pady=5, fill="both", expand="yes")

        estado_civil_options = ["Soltero/a", "Casado/a", "Viudo/a", "Divorciado/a", "Conviviente", "Otro"]
        estado_civil = tk.StringVar()
        estado_civil.set("")  # Valor inicial

        for option in estado_civil_options:
            ttk.Radiobutton(frame_estado_civil, text=option, variable=estado_civil, value=option).pack(anchor="w")

        # Botones de género (ejemplo básico)
        ttk.Label(ven_da, text="Género:").pack(padx=10, pady=5)
        ttk.Button(ven_da, text="Femenino", command=lambda: guardar_en_db(data, "Femenino", estado_civil.get())).pack(pady=5)
        ttk.Button(ven_da, text="Masculino", command=lambda: guardar_en_db(data, "Masculino", estado_civil.get())).pack(pady=5)
        ttk.Button(ven_da, text="Otros", command=lambda: guardar_en_db(data, "Otros", estado_civil.get())).pack(pady=5)

       

    def guardar_en_db(data, genero, estado_civil):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('asistencia.db')
            cursor = conn.cursor()

            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insertar los datos en la tabla 'empleados' junto con la fecha y hora
            cursor.execute('''
                INSERT INTO empleados (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data["nombres"], data["apellidoPaterno"], data["apellidoMaterno"], data["dni"], genero, estado_civil, fecha_hora_actual))

            # Guardar cambios y cerrar la conexión
            conn.commit()
            conn.close()

            messagebox.showinfo("Registro exitoso", "Los datos se han guardado correctamente en la base de datos.")

        except sqlite3.Error as e:
            messagebox.showerror("Error al guardar", f"Error de SQLite: {str(e)}")

    # Crear la ventana principal
    wen = tk.Tk()
    wen.title('Consulta de DNI')
    wen.geometry("300x150")
    wen.configure(background='lightblue')

    # Etiqueta y entrada para ingresar el número de DNI
    label_dni = ttk.Label(wen, text='Ingrese el número de DNI:')
    label_dni.pack(pady=10)

    en_dni = ttk.Entry(wen)
    en_dni.pack(pady=5)

    # Botón para consultar el DNI (se activará también con Enter)
    btn_consultar = ttk.Button(wen, text='Consultar DNI', command=dni_consultar)
    btn_consultar.pack(pady=10)

    # Atajo para activar la función dni_consultar al presionar Enter en la entrada de texto
    en_dni.bind('<Return>', lambda event: dni_consultar())

    wen.mainloop()


def exportar_a_pdf():
    try:
        # Conexión a la base de datos
        miConexion = sqlite3.connect("asistencia.db")
        miCursor = miConexion.cursor()
        
        # Consulta para obtener todos los registros
        miCursor.execute("SELECT * FROM empleados")
        registros = miCursor.fetchall()
        
        # Configuración del documento PDF con orientación horizontal
        class PDF(FPDF):
            def __init__(self):
                super().__init__(orientation='L')  # Orientación horizontal
                self.set_auto_page_break(auto=True, margin=15)
        
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        # Títulos de las columnas
        columnas = ["ID","NOMBRES", "APELLIDO PATERNO", "APELLIDO MATERNO", "DNI", "GENERO", "ESTADO CIVIL", "FECHA Y HORA"]
        pdf.set_fill_color(180, 200, 235)
        cell_width = pdf.w / len(columnas)
        cell_width =35
        cell_height = 7
        
        for col in columnas:
            pdf.cell(cell_width, cell_height, col, border=1, align='C', fill=True)
        
        pdf.ln()
        
        # Agregar registros al PDF
        pdf.set_fill_color(255, 255, 255)
        for row in registros:
            for dato in row:
                pdf.cell(cell_width, cell_height, str(dato), border=1, align='C')
            pdf.ln()
        
        # Guardar el PDF
        pdf_filename = "registros_asistencia_horizontal.pdf"
        pdf.output(pdf_filename)
        messagebox.showinfo("Exportar a PDF", f"Datos exportados a {pdf_filename}")
        
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error al exportar a PDF: {error}")



def exportar_a_excel():
    try:
        # Conexión a la base de datos
        miConexion = sqlite3.connect("asistencia.db")
        miCursor = miConexion.cursor()
        
        # Consulta para obtener todos los registros
        miCursor.execute("SELECT * FROM empleados")
        registros = miCursor.fetchall()
        
        # Configuración del archivo Excel
        workbook = xlsxwriter.Workbook('registros_generales.xlsx')
        worksheet = workbook.add_worksheet()
        
        # Encabezados de las columnas
        columnas = ["ID", "NOMBRES", "APELLIDO PATERNO", "APELLIDO MATERNO", "DNI", "GENERO", "ESTADO CIVIL", "FECHA Y HORA"]
        for col_num, col_title in enumerate(columnas):
            worksheet.write(0, col_num, col_title)
        
        # Escribir registros en el archivo Excel
        for row_num, row_data in enumerate(registros):
            for col_num, cell_data in enumerate(row_data):
                worksheet.write(row_num + 1, col_num, cell_data)
        
        # Cerrar el archivo Excel
        workbook.close()
        messagebox.showinfo("Exportar a Excel", "Datos exportados a registros_generales.xlsx")
        
    except sqlite3.Error as error:
        messagebox.showerror("Error", f"Error al exportar a Excel: {error}")

def escaneo_archivos():
        def escanear_dni():
            try:
                # Abrir un cuadro de diálogo para seleccionar la imagen del DNI
                ruta_imagen = filedialog.askopenfilename(
                    title="Seleccionar imagen del DNI",
                    filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp"), ("Todos los archivos", "*.*"))
                )
                
                if not ruta_imagen:
                    return  # Si no se selecciona ninguna imagen, salir
                
                # Cargar la imagen y convertirla a escala de grises
                imagen = Image.open(ruta_imagen).convert('L')
                
                # Decodificar el código de barras usando pyzbar
                resultado = decode(imagen)
                
                if resultado:
                    # Mostrar el código de barras encontrado
                    codigo = resultado[0].data.decode('utf-8')
                    messagebox.showinfo("Escaneo de DNI", f"Código de barras encontrado:\n{codigo}")
                    # Obtener información del DNI desde la API
                    url = f'https://dniruc.apisperu.com/api/v1/dni/{codigo}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if response.status_code == 200:
                        if not data.get('success', False):
                            messagebox.showinfo("DNI no registrado", "El DNI no se encuentra registrado en la base de datos.")
                        else:
                            mostrar_datos(data)
                    else:
                        messagebox.showerror("Error en la consulta", f"Código de estado: {response.status_code}")
                
                else:
                    messagebox.showinfo("Escaneo de DNI", "No se encontró ningún código de barras válido en la imagen.")
                
            
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error en la consulta", f"Error de conexión: {str(e)}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al escanear el código de barras: {str(e)}")

        # Función para mostrar los datos del DNI en una nueva ventana
        def mostrar_datos(data):
            try:
                # Crear la ventana de datos del DNI
                ventana_datos = tk.Toplevel()
                ventana_datos.title('Datos del DNI')
                ventana_datos.geometry("500x600")
                
                # Mostrar los datos del DNI en etiquetas
                tk.Label(ventana_datos, text=f'DNI: {data["dni"]}').pack(padx=10, pady=5)
                tk.Label(ventana_datos, text=f'Nombres: {data["nombres"]}').pack(padx=10, pady=5)
                tk.Label(ventana_datos, text=f'Apellido Paterno: {data["apellidoPaterno"]}').pack(padx=10, pady=5)
                tk.Label(ventana_datos, text=f'Apellido Materno: {data["apellidoMaterno"]}').pack(padx=10, pady=5)
                
                # Sección para seleccionar el estado civil
                frame_estado_civil = tk.LabelFrame(ventana_datos, text="Estado Civil")
                frame_estado_civil.pack(padx=10, pady=5, fill="both", expand="yes")
                
                estado_civil_options = ["Soltero/a", "Casado/a", "Viudo/a", "Divorciado/a", "Conviviente", "Otro"]
                
                estado_civil = tk.StringVar()
                estado_civil.set("")  # Valor inicial
                
                for option in estado_civil_options:
                    tk.Radiobutton(frame_estado_civil, text=option, variable=estado_civil, value=option).pack(anchor="w")
                
                # Botones para registrar datos en la base de datos
                tk.Button(ventana_datos, text="Registrar - Femenino", command=lambda: guardar_en_db(data, "Femenino", estado_civil.get())).pack(pady=5)
                tk.Button(ventana_datos, text="Registrar - Masculino", command=lambda: guardar_en_db(data, "Masculino", estado_civil.get())).pack(pady=5)
                tk.Button(ventana_datos, text="Registrar - Otros", command=lambda: guardar_en_db(data, "Otros", estado_civil.get())).pack(pady=5)
                
                # Botón para cerrar la ventana
                tk.Button(ventana_datos, text="Cerrar", command=ventana_datos.destroy).pack(pady=10)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar los datos del DNI: {str(e)}")

        # Función para guardar datos en la base de datos
        def guardar_en_db(data, genero, estado_civil):
            try:
                # Conectar a la base de datos
                conn = sqlite3.connect('asistencia.db')
                cursor = conn.cursor()

                # Obtener la fecha y hora actual
                fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insertar datos en la tabla 'empleados' junto con la fecha y hora
                cursor.execute('''
                    INSERT INTO empleados (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data["nombres"], data["apellidoPaterno"], data["apellidoMaterno"], data["dni"], genero, estado_civil, fecha_hora_actual))

                # Guardar cambios y cerrar la conexión
                conn.commit()
                conn.close()

                messagebox.showinfo("Registro exitoso", "Los datos se han guardado correctamente en la base de datos.")

            except sqlite3.Error as e:
                messagebox.showerror("Error al guardar", f"Error de SQLite: {str(e)}")

        # Configuración de la ventana principal
        root = tk.Tk()
        root.title("Escaneo de DNI")
        root.geometry("250x100")
        root.configure(background='lightblue')
        
        # Botón para escanear el código de barras del DNI
        btn_escanear = tk.Button(root, text="Escanear DNI", command=escanear_dni)
        btn_escanear.pack(pady=20)

def reportes():
    def obtener_cantidad_registros_diarios(fecha):
        fecha_str = fecha.strftime('%Y-%m-%d')
        miConexion = sqlite3.connect("asistencia.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM empleados WHERE FECHA_HORA LIKE ?", (f"{fecha_str}%",))
        registros = miCursor.fetchall()
        miConexion.close()
        return registros

    # Función para obtener la cantidad de registros entre dos fechas en la base de datos
    def obtener_cantidad_registros_entre_fechas(fecha_inicio, fecha_fin):
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        miConexion = sqlite3.connect("asistencia.db")
        miCursor = miConexion.cursor()
        miCursor.execute("SELECT * FROM empleados WHERE FECHA_HORA BETWEEN ? AND ?", (fecha_inicio_str, fecha_fin_str))
        registros = miCursor.fetchall()
        miConexion.close()
        return registros

    # Función para mostrar registros en el Treeview
    def mostrar_registros(tree, registros):
        # Limpiar datos anteriores en el Treeview
        for row in tree.get_children():
            tree.delete(row)
        
        # Insertar nuevos datos en el Treeview
        for registro in registros:
            tree.insert("", tk.END, values=registro)

    # Función para mostrar resultados en la GUI usando Treeview
    def mostrar_resultados(titulo, registros):
        root = tk.Tk()
        root.title(titulo)
        root.geometry("800x400")
        
        label_titulo = tk.Label(root, text=titulo, font=("Arial", 14))
        label_titulo.pack(pady=10)

        # Crear el Treeview con columnas
        columns = ["ID", "NOMBRES", "APELLIDO_PATERNO", "APELLIDO_MATERNO", "DNI", "GENERO", "ESTADO_CIVIL", "FECHA_HORA"]
        tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        
        # Configurar encabezados de las columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Mostrar registros en el Treeview
        mostrar_registros(tree, registros)
        
        tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        root.mainloop()

    # Función principal para mostrar las opciones al usuario
    def mostrar_interfaz():
        root = tk.Tk()
        root.title("Reporte de Registros")
        root.geometry("300x250")
        root.configure(background='lightblue')

        label_titulo = tk.Label(root, text="Seleccione el tipo de reporte:", font=("Arial", 14), bg='lightblue')
        label_titulo.pack(pady=10)

        # Botones para seleccionar el tipo de reporte
        btn_diarios = tk.Button(root, text="Registros Diarios", command=mostrar_registros_diarios_gui)
        btn_diarios.pack(pady=5)

        btn_semanales = tk.Button(root, text="Registros Semanales", command=mostrar_registros_semanales_gui)
        btn_semanales.pack(pady=5)

        btn_mensuales = tk.Button(root, text="Registros Mensuales", command=mostrar_registros_mensuales_gui)
        btn_mensuales.pack(pady=5)

        btn_salir = tk.Button(root, text="Salir", command=root.destroy)
        btn_salir.pack(pady=10)

        root.mainloop()

    # Funciones para mostrar registros diarios, semanales y mensuales usando Treeview
    def mostrar_registros_diarios_gui():
        try:
            # Obtener fecha actual
            hoy = datetime.now()

            # Obtener registros diarios
            registros_diarios = obtener_cantidad_registros_diarios(hoy)

            # Mostrar resultados en la interfaz gráfica usando Treeview
            mostrar_resultados("Registros Diarios", registros_diarios)

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener registros diarios: {str(e)}")

    def mostrar_registros_semanales_gui():
        try:
            # Obtener fecha actual
            hoy = datetime.now()

            # Obtener registros semanales (últimos 7 días)
            semana_pasada = hoy - timedelta(days=7)
            registros_semanales = obtener_cantidad_registros_entre_fechas(semana_pasada, hoy)

            # Mostrar resultados en la interfaz gráfica usando Treeview
            mostrar_resultados("Registros Semanales", registros_semanales)

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener registros semanales: {str(e)}")

    def mostrar_registros_mensuales_gui():
        try:
            # Obtener fecha actual
            hoy = datetime.now()

            # Obtener primer día del mes actual
            primer_dia_mes_actual = hoy.replace(day=1)

            # Obtener registros mensuales
            registros_mensuales = obtener_cantidad_registros_entre_fechas(primer_dia_mes_actual, hoy)

            # Mostrar resultados en la interfaz gráfica usando Treeview
            mostrar_resultados("Registros Mensuales", registros_mensuales)

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener registros mensuales: {str(e)}")

    # Llamar a la función principal para mostrar la interfaz de usuario
    mostrar_interfaz()
    
    
def cargar_a_la_data():
    def seleccionar_y_cargar_excel():
        try:
            # Crear ventana de selección de archivo
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de tkinter

            # Obtener el archivo Excel seleccionado por el usuario
            archivo_excel = filedialog.askopenfilename(
                title="Seleccionar archivo Excel",
                filetypes=[("Archivos de Excel", "*.xlsx;*.xls"), ("Todos los archivos", "*.*")]
            )

            if not archivo_excel:
                return  # Salir si no se selecciona ningún archivo

            # Leer el archivo Excel en un DataFrame de pandas
            df = pd.read_excel(archivo_excel)

            # Conexión a la base de datos SQLite
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()

            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Iterar sobre las filas del DataFrame y cargar en la base de datos
            registros_insertados = 0
            for index, row in df.iterrows():
                # Extraer los valores de cada fila del DataFrame
                nombres = row['NOMBRES']
                apellido_paterno = row['APELLIDO_PATERNO']
                apellido_materno = row['APELLIDO_MATERNO']
                dni = row['DNI']
                genero = row['GENERO']
                estado_civil = row['ESTADO_CIVIL']

                # Crear la tupla de valores para la consulta SQL
                valores = (nombres, apellido_paterno, apellido_materno, dni, genero, estado_civil, fecha_hora_actual)
                
                # Ejecutar la consulta SQL para insertar en la base de datos
                miCursor.execute("INSERT INTO empleados (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA) VALUES (?, ?, ?, ?, ?, ?, ?)", valores)
                registros_insertados += 1

            # Guardar cambios en la base de datos
            miConexion.commit()
            miConexion.close()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Se han insertado {registros_insertados} registros desde el archivo Excel.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar desde Excel a la base de datos: {str(e)}")
            if 'miConexion' in locals():
                miConexion.rollback()  # Revertir cambios si ocurre un error
            else:
                messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")

    # Función principal para ejecutar la selección y carga de Excel
    def main():
        seleccionar_y_cargar_excel()

    if __name__ == "__main__":
        main()

def ventan_reportes():

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Registros de Asistencia")
    root.geometry("800x500")
    root.configure(background='lightgreen')

    # Crear Treeview y Scrollbar
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, height=10, columns=('#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7'), yscrollcommand=tree_scroll.set)
    tree.pack()

    tree_scroll.config(command=tree.yview)

    tree.column('#0', width=50)
    tree.heading('#0', text="ID", anchor=tk.CENTER)
    tree.heading('#1', text="NOMBRES", anchor=tk.CENTER)
    tree.heading('#2', text="APELLIDO PATERNO", anchor=tk.CENTER)
    tree.heading('#3', text="APELLIDO MATERNO", anchor=tk.CENTER)
    tree.heading('#4', text="DNI", anchor=tk.CENTER)
    tree.heading('#5', text="GENERO", anchor=tk.CENTER)
    tree.heading('#6', text="ESTADO CIVIL", anchor=tk.CENTER)
    tree.heading('#7', text="FECHA Y HORA", anchor=tk.CENTER)


def ventana_administrador():

    root=Tk()
    root.title("CONSULTAS Y ASISTENCIAS EN EL API")
    root.geometry("800x500")
    root.configure(background='lightblue')


    def conexionBBDD():
        try:
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute('''CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOMBRES TEXT,
                    APELLIDO_PATERNO TEXT,
                    APELLIDO_MATERNO TEXT,
                    DNI TEXT,
                    GENERO TEXT,
                    ESTADO_CIVIL TEXT,
                    FECHA_HORA TEXT
                )''')
    
            messagebox.showinfo("CONEXION", "Base de datos creada")
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al conectar a la base de datos: {error}")


    def eliminarBBDD():
        miConexion=sqlite3.connect("asistencia.db")
        miCursor=miConexion.cursor()
        if messagebox.askyesno(message="los datos se borraran difinitivamente, desea continuar", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE empleados")
        else:
            pass
        limpiarCampos()
        mostrar()

    def salirAplicacion():
        valor=messagebox.askquestion("salir","esta seguro de que quiere salir")
        if valor=="yes":
            root.destroy()

    def limpiarCampos():
        miID.set("")
        miNombres.set("")
        miApellidoPaterno.set("")
        miApellidoMaterno.set("")
        miDNI.set("")
        miGenero.set("")
        miEstado_civil.set("")
        
    miID=StringVar()
    miNombres=StringVar()
    miApellidoPaterno=StringVar()
    miApellidoMaterno=StringVar()
    miGenero=StringVar()
    miEstado_civil=StringVar()
    miDNI=StringVar()
    
            

    def mensaje():
        acerca='''
        aplicacion CRUD
        version 1.0
        TECNOLOGIA PYTHON TKINTER
        ES ALGO QUE ME MANDA HACER EL PROFE XDXDXDXD
        '''
        messagebox.showinfo(title="IMFORMACION", message=acerca)

    import datetime 

    def crear():
        try:
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            datos = (miNombres.get(), miApellidoPaterno.get(), miApellidoMaterno.get(),
                    miDNI.get(), miGenero.get(), miEstado_civil.get(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            miCursor.execute("INSERT INTO empleados VALUES (NULL,?,?,?,?,?,?,?)", datos)
            miConexion.commit()
            messagebox.showinfo("CREAR", "Registro creado correctamente")
            limpiarCampos()
            mostrar()
        except:
            pass


    def mostrar():
        try:
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM empleados")
            registros = miCursor.fetchall()
            for row in registros:
                tree.insert("",0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        except:
            pass

    def actualizar():
        try:
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            datos = (miNombres.get(), miApellidoPaterno.get(), miApellidoMaterno.get(),
                    miDNI.get(), miGenero.get(), miEstado_civil.get(), miID.get())
            miCursor.execute("UPDATE empleados SET NOMBRES=?, APELLIDO_PATERNO=?, APELLIDO_MATERNO=?, DNI=?, GENERO=?, ESTADO_CIVIL=? WHERE id=?", datos)
            miConexion.commit()
            messagebox.showinfo("ACTUALIZAR", "Registro actualizado correctamente")
            limpiarCampos()
            mostrar()
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al actualizar el registro: {error}")

    def borrar():
        try:
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute("DELETE FROM empleados WHERE id=?", (miID.get(),))
            miConexion.commit()
            messagebox.showinfo("BORRAR", "Registro eliminado correctamente")
            limpiarCampos()
            mostrar()
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al borrar el registro: {error}")

    def buscar_por_dni():
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
            
    def matriculas():
        class Curso:
            def __init__(self, nombre, codigo, grado):
                self.nombre = nombre
                self.codigo = codigo
                self.grado = grado

        class Matricula:
            def __init__(self, nombres, apellidos, grado_curso):
                self.nombres = nombres
                self.apellidos = apellidos
                self.grado_curso = grado_curso

        class RegistroCursosGUI:
            def __init__(self, root):
                self.root = root
                self.root.title("Registro de Cursos y Matrícula")

                # Inicializar base de datos de cursos
                self.conn_cursos = sqlite3.connect('registro_cursos.db')
                self.c_cursos = self.conn_cursos.cursor()
                self.create_table_cursos()

                # Inicializar base de datos de matrícula
                self.conn_matricula = sqlite3.connect('matricula.db')
                self.c_matricula = self.conn_matricula.cursor()
                self.create_table_matricula()

                # Inicializar base de datos de empleados
                self.conn_empleados = sqlite3.connect('asistencia.db')
                self.c_empleados = self.conn_empleados.cursor()

                # Crear widgets
                self.label_dni = tk.Label(root, text="Ingrese DNI del Empleado:")
                self.label_dni.grid(row=0, column=0, padx=10, pady=5)
                self.entry_dni = tk.Entry(root)
                self.entry_dni.grid(row=0, column=1, padx=10, pady=5)

                self.btn_buscar = tk.Button(root, text="Buscar Empleado", command=self.buscar_empleado)
                self.btn_buscar.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

                self.label_nombre = tk.Label(root, text="Nombre del Curso:")
                self.label_nombre.grid(row=2, column=0, padx=10, pady=5)
                self.entry_nombre = tk.Entry(root)
                self.entry_nombre.grid(row=2, column=1, padx=10, pady=5)

                self.label_grado = tk.Label(root, text="Grado del Curso:")
                self.label_grado.grid(row=3, column=0, padx=10, pady=5)
                self.entry_grado = tk.Entry(root)
                self.entry_grado.grid(row=3, column=1, padx=10, pady=5)

                self.btn_agregar_curso = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
                self.btn_agregar_curso.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

                self.label_buscar_grado = tk.Label(root, text="Buscar Cursos por Grado:")
                self.label_buscar_grado.grid(row=5, column=0, padx=10, pady=5)
                self.entry_buscar_grado = tk.Entry(root)
                self.entry_buscar_grado.grid(row=5, column=1, padx=10, pady=5)

                self.btn_buscar_grado = tk.Button(root, text="Buscar", command=self.buscar_cursos_por_grado)
                self.btn_buscar_grado.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

                self.label_matricula = tk.Label(root, text="Matricular en Curso:")
                self.label_matricula.grid(row=7, column=0, padx=10, pady=5)

                self.btn_matricular = tk.Button(root, text="Matricular", command=self.matricular_empleado)
                self.btn_matricular.grid(row=7, column=1, padx=10, pady=5)

                self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
                self.resultado_text.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

            def create_table_cursos(self):
                self.c_cursos.execute('''CREATE TABLE IF NOT EXISTS cursos (
                                    codigo TEXT PRIMARY KEY,
                                    nombre TEXT NOT NULL,
                                    grado TEXT NOT NULL
                                    )''')
                self.conn_cursos.commit()

            def create_table_matricula(self):
                self.c_matricula.execute('''CREATE TABLE IF NOT EXISTS matricula (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nombres TEXT NOT NULL,
                                    apellidos TEXT NOT NULL,
                                    grado_curso TEXT NOT NULL,
                                    FOREIGN KEY (grado_curso) REFERENCES cursos (grado)
                                    )''')
                self.conn_matricula.commit()

            def buscar_empleado(self):
                dni = self.entry_dni.get()

                if dni:
                    self.c_empleados.execute("SELECT NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO FROM empleados WHERE DNI=?", (dni,))
                    empleado = self.c_empleados.fetchone()
                    if empleado:
                        nombres, apellido_paterno, apellido_materno = empleado
                        self.mostrar_resultado(f"Empleado encontrado:\n{apellido_paterno} {apellido_materno}, {nombres}")
                    else:
                        self.mostrar_resultado("No se encontró ningún empleado con el DNI especificado.")
                else:
                    messagebox.showerror("Error", "Por favor, ingrese el DNI del empleado.")

            def agregar_curso(self):
                nombre = self.entry_nombre.get()
                grado = self.entry_grado.get()

                if nombre and grado:
                    codigo = f"{nombre[:3]}-{grado}"  # Generar código basado en nombre y grado
                    curso = Curso(nombre, codigo, grado)
                    try:
                        self.c_cursos.execute("INSERT INTO cursos (codigo, nombre, grado) VALUES (?, ?, ?)",
                                            (curso.codigo, curso.nombre, curso.grado))
                        self.conn_cursos.commit()
                        messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")
                        self.entry_nombre.delete(0, tk.END)
                        self.entry_grado.delete(0, tk.END)
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Error", "Ya existe un curso con el mismo código.")
                else:
                    messagebox.showerror("Error", "Por favor, complete todos los campos.")

            def matricular_empleado(self):
                dni = self.entry_dni.get()
                grado = self.entry_grado.get()

                if dni and grado:
                    # Buscar empleado por DNI
                    self.c_empleados.execute("SELECT NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO FROM empleados WHERE DNI=?", (dni,))
                    empleado = self.c_empleados.fetchone()
                    if empleado:
                        nombres, apellido_paterno, apellido_materno = empleado
                        # Insertar matrícula en la tabla matricula
                        try:
                            self.c_matricula.execute("INSERT INTO matricula (nombres, apellidos, grado_curso) VALUES (?, ?, ?)",
                                                    (nombres, f"{apellido_paterno} {apellido_materno}", grado))
                            self.conn_matricula.commit()
                            messagebox.showinfo("Matrícula", f"Empleado matriculado en el curso de grado {grado}.")
                        except sqlite3.IntegrityError:
                            messagebox.showerror("Error", "El empleado ya está matriculado en este curso.")
                    else:
                        messagebox.showerror("Error", "No se encontró un empleado con el DNI especificado.")
                else:
                    messagebox.showerror("Error", "Por favor, ingrese el DNI del empleado y el grado del curso.")

            def buscar_cursos_por_grado(self):
                grado = self.entry_buscar_grado.get()

                if grado:
                    self.c_cursos.execute("SELECT nombre, codigo FROM cursos WHERE grado=?", (grado,))
                    cursos = self.c_cursos.fetchall()
                    if cursos:
                        resultado = "Cursos encontrados:\n"
                        for curso in cursos:
                            resultado += f"Nombre: {curso[0]}, Código: {curso[1]}\n"
                    else:
                        resultado = f"No se encontraron cursos para el grado {grado}."
                    self.mostrar_resultado(resultado)
                else:
                    messagebox.showerror("Error", "Por favor, ingrese un grado para buscar cursos.")

            def mostrar_resultado(self, resultado):
                self.resultado_text.delete(1.0, tk.END)
                self.resultado_text.insert(tk.END, resultado)

            def __del__(self):
                self.conn_cursos.close()
                self.conn_matricula.close()
                self.conn_empleados.close()

        if __name__ == "__main__":
            root = tk.Tk()
            app = RegistroCursosGUI(root)
            root.mainloop()
            
    def ver_matriculas():
        class Curso:
            def __init__(self, nombre, grado):
                self.nombre = nombre
                self.grado = grado

            class Matricula:
                def __init__(self, nombres, apellidos, grado_curso):
                    self.nombres = nombres
                    self.apellidos = apellidos
                    self.grado_curso = grado_curso

            class RegistroCursosGUI:
                def __init__(self, root):
                    self.root = root
                    self.root.title("Registro de Cursos y Matrícula")

                    # Inicializar base de datos de cursos
                    self.conn_cursos = sqlite3.connect('registro_cursos.db')
                    self.c_cursos = self.conn_cursos.cursor()
                    self.create_table_cursos()

                    # Inicializar base de datos de matrícula
                    self.conn_matricula = sqlite3.connect('matricula.db')
                    self.c_matricula = self.conn_matricula.cursor()
                    self.create_table_matricula()

                    # Crear widgets
                    self.label_nombre = tk.Label(root, text="Nombre del Curso:")
                    self.label_nombre.grid(row=0, column=0, padx=10, pady=5)
                    self.entry_nombre = tk.Entry(root)
                    self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

                    self.label_grado = tk.Label(root, text="Grado del Curso:")
                    self.label_grado.grid(row=1, column=0, padx=10, pady=5)
                    self.entry_grado = tk.Entry(root)
                    self.entry_grado.grid(row=1, column=1, padx=10, pady=5)

                    self.btn_agregar_curso = tk.Button(root, text="Agregar Curso", command=self.agregar_curso)
                    self.btn_agregar_curso.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

                    self.label_buscar_grado = tk.Label(root, text="Buscar Estudiantes por Grado:")
                    self.label_buscar_grado.grid(row=3, column=0, padx=10, pady=5)
                    self.entry_buscar_grado = tk.Entry(root)
                    self.entry_buscar_grado.grid(row=3, column=1, padx=10, pady=5)

                    self.btn_buscar_estudiantes = tk.Button(root, text="Buscar Estudiantes", command=self.buscar_estudiantes_por_grado)
                    self.btn_buscar_estudiantes.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

                    self.resultado_text = tk.Text(root, height=10, width=50, wrap="word")
                    self.resultado_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

                def create_table_cursos(self):
                    self.c_cursos.execute('''CREATE TABLE IF NOT EXISTS cursos (
                                        codigo TEXT PRIMARY KEY,
                                        nombre TEXT NOT NULL,
                                        grado TEXT NOT NULL
                                        )''')
                    self.conn_cursos.commit()

                def create_table_matricula(self):
                    self.c_matricula.execute('''CREATE TABLE IF NOT EXISTS matricula (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        nombres TEXT NOT NULL,
                                        apellidos TEXT NOT NULL,
                                        grado_curso TEXT NOT NULL,
                                        FOREIGN KEY (grado_curso) REFERENCES cursos (grado)
                                        )''')
                    self.conn_matricula.commit()

                def agregar_curso(self):
                    nombre = self.entry_nombre.get()
                    grado = self.entry_grado.get()

                    if nombre and grado:
                        codigo = f"{nombre[:3]}-{grado}"  # Generar código basado en nombre y grado
                        curso = Curso(nombre, grado)
                        try:
                            self.c_cursos.execute("INSERT INTO cursos (codigo, nombre, grado) VALUES (?, ?, ?)",
                                                (codigo, curso.nombre, curso.grado))
                            self.conn_cursos.commit()
                            messagebox.showinfo("Registro de Cursos", f"Curso {curso.nombre} registrado con éxito.")
                            self.entry_nombre.delete(0, tk.END)
                            self.entry_grado.delete(0, tk.END)
                        except sqlite3.IntegrityError:
                            messagebox.showerror("Error", "Ya existe un curso con el mismo código.")
                    else:
                        messagebox.showerror("Error", "Por favor, complete todos los campos.")

                def buscar_estudiantes_por_grado(self):
                    grado = self.entry_buscar_grado.get()

                    if grado:
                        self.c_matricula.execute("SELECT nombres, apellidos FROM matricula WHERE grado_curso=?", (grado,))
                        estudiantes = self.c_matricula.fetchall()
                        if estudiantes:
                            resultado = f"Estudiantes matriculados en el grado {grado}:\n"
                            for estudiante in estudiantes:
                                resultado += f"Nombres: {estudiante[0]}, Apellidos: {estudiante[1]}\n"
                        else:
                            resultado = f"No se encontraron estudiantes matriculados en el grado {grado}."
                        self.mostrar_resultado(resultado)
                    else:
                        messagebox.showerror("Error", "Por favor, ingrese un grado para buscar estudiantes.")

                def mostrar_resultado(self, resultado):
                    self.resultado_text.delete(1.0, tk.END)
                    self.resultado_text.insert(tk.END, resultado)

                def __del__(self):
                    self.conn_cursos.close()
                    self.conn_matricula.close()

            if __name__ == "__main__":
                root = tk.Tk()
                app = RegistroCursosGUI(root)
                root.mainloop()

                    
            
    tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7'))
    tree.place(x=0, y=300)
    tree.column('#0', width=50)
    tree.heading('#0', text="ID", anchor=tk.CENTER)
    tree.heading('#1', text="NOMBRES", anchor=tk.CENTER)
    tree.heading('#2', text="APELLIDO PATERNO", anchor=tk.CENTER)
    tree.heading('#3', text="APELLIDO MATERNO", anchor=tk.CENTER)
    tree.heading('#4', text="DNI", anchor=tk.CENTER)
    tree.heading('#5', text="GENERO", anchor=tk.CENTER)
    tree.heading('#6', text="ESTADO CIVIL", anchor=tk.CENTER)
    tree.heading('#7', text="FECHA Y HORA", anchor=tk.CENTER)
    

    def seleccionarUsandoClick(event):
        item = tree.selection()[0]
        miID.set(tree.item(item, "text"))
        miNombres.set(tree.item(item, "values")[0])
        miApellidoPaterno.set(tree.item(item, "values")[1])
        miApellidoMaterno.set(tree.item(item, "values")[2])
        miDNI.set(tree.item(item, "values")[3])
        miGenero.set(tree.item(item, "values")[4])
        miEstado_civil.set(tree.item(item, "values")[5])

    tree.bind("<ButtonRelease-1>", seleccionarUsandoClick)
            
    menubar=Menu(root)
    menubasedat=Menu(menubar,tearoff=0)
    menubasedat.add_command(label="crear/conectar con la base de datos", command=conexionBBDD)
    menubasedat.add_command(label="eliminar base de datos", command=eliminarBBDD)
    menubasedat.add_command(label="salir", command=salirAplicacion)
    menubar.add_cascade(label="inicio", menu=menubasedat)

    consultarmenu=Menu(menubar, tearoff=0)
    consultarmenu.add_command(label="DNI", command=DNI)
    menubar.add_cascade(label="consultar", menu=consultarmenu)

    repormenu=Menu(menubar, tearoff=0)
    repormenu.add_command(label="mostrar", command=reportes)
    menubar.add_cascade(label="reportes", menu=repormenu)

    expomenu=Menu(menubar, tearoff=0)
    expomenu.add_command(label="exportar datos a excel", command=exportar_a_excel)
    expomenu.add_command(label="descargar datos en pdf", command=exportar_a_pdf)
    menubar.add_cascade(label="exportar", menu=expomenu)
    
    subirmenu=Menu(menubar, tearoff=0)
    subirmenu.add_command(label="subir documento", command=cargar_a_la_data)
    subirmenu.add_cascade(label="subir archivo excel", menu=subirmenu)
    
    lectormenu=Menu(menubar, tearoff=0)
    lectormenu.add_command(label="escaneo por archivos", command=escaneo_archivos)
    menubar.add_cascade(label="escaneo", menu=lectormenu)
    
    subirmenu=Menu(menubar, tearoff=0)
    subirmenu.add_command(label="subir archivo de excel", command=cargar_a_la_data)
    menubar.add_cascade(label="subir archivos", menu=subirmenu)
    
    matrixmenu=Menu(menubar, tearoff=0)
    matrixmenu.add_command(label="ver", command=MATRIX_ADMIN)
    menubar.add_cascade(label="asistencia", menu=matrixmenu)
    
    matrimenu=Menu(menubar, tearoff=0)
    matrimenu.add_command(label="SEMESTRES", command=matriculas)
    matrimenu.add_command(label="VER", command=ver_matriculas)
    menubar.add_cascade(label="matriculas", menu=matrimenu)

    ayudamenu=Menu(menubar, tearoff=0)
    ayudamenu.add_command(label="resetear campos", command=limpiarCampos)
    ayudamenu.add_command(label="acerca", command=mensaje)
    menubar.add_cascade(label="ayuda",menu=ayudamenu)


    e1=Entry(root, textvariable=miID)

    l2=Label(root,text="NOMBRES", bg='lightblue')
    l2.place(x=100,y=10)
    e2=Entry(root,textvariable=miNombres, width=50)
    e2.place(x=250,y=10)
     
    b2=Button(root, text="BUSCAR", command=buscar_por_dni)
    b2.place(x=800,y=10)
    
    l3=Label(root,text="APELLIDO PATERNO",bg='lightblue')
    l3.place(x=100,y=40)
    e3=Entry(root,textvariable=miApellidoPaterno, width=50)
    e3.place(x=250,y=40)

    l4=Label(root,text="APELLIDO MATERNO",bg='lightblue')
    l4.place(x=100,y=70)
    e4=Entry(root, textvariable=miApellidoMaterno, width=50)
    e4.place(x=250,y=70)

    l5=Label(root, text="DNI", bg='lightblue')
    l5.place(x=100,y=100)
    e5=Entry(root, textvariable=miDNI,  width=50)
    e5.place(x=250,y=100)

    l6=Label(root,text="GENERO", bg='lightblue')
    l6.place(x=100,y=130)
    e6=Entry(root,textvariable=miGenero, width=50)
    e6.place(x=250,y=130)
    
    l7=Label(root, text="ESTADO CIVIL",bg='lightblue')
    l7.place(x=100,y=160)
    e7=Entry(root, textvariable=miEstado_civil, width=50)
    e7.place(x=250,y=160)

    b1=Button(root, text="crear registro", command=crear)
    b1.place(x=100,y=250)
    b2=Button(root, text="modificar registro", command=actualizar)
    b2.place(x=400,y=250)
    b3=Button(root, text="mostrar lista", command=mostrar)
    b3.place(x=700, y=250)
    b4=Button(root, text="eliminar registro", bg="red", command=borrar)
    b4.place(x=1000,y=250)
   
    root.config(menu=menubar)
    conexionBBDD()
    
def MATRIX_ADMIN():

    class Matricula:
        def __init__(self, nombres, apellidos, grado_curso):
            self.nombres = nombres
            self.apellidos = apellidos
            self.grado_curso = grado_curso

    class AsistenciaGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Registro de Asistencia por Grado")

            # Inicializar base de datos de matrícula y asistencia
            self.conn_matricula = sqlite3.connect('matricula.db')
            self.c_matricula = self.conn_matricula.cursor()

            self.conn_asistencia = sqlite3.connect('asistencia.db')
            self.c_asistencia = self.conn_asistencia.cursor()
            self.create_table_asistencia()

            # Crear widgets
            self.create_widgets()
            self.populate_grado_combobox()

        def create_widgets(self):
            # Etiqueta y combo para seleccionar grado
            self.label_grado = tk.Label(self.root, text="Seleccionar Grado:")
            self.label_grado.grid(row=0, column=0, padx=10, pady=5)
            self.combo_grado = ttk.Combobox(self.root)
            self.combo_grado.grid(row=0, column=1, padx=10, pady=5)

            # Etiqueta y entrada para la fecha
            self.label_fecha = tk.Label(self.root, text="Fecha (YYYY-MM-DD):")
            self.label_fecha.grid(row=1, column=0, padx=10, pady=5)
            self.entry_fecha = tk.Entry(self.root)
            self.entry_fecha.grid(row=1, column=1, padx=10, pady=5)

            # Botón para ver asistencias
            self.btn_ver_asistencias = tk.Button(self.root, text="Ver Asistencias", command=self.ver_asistencias)
            self.btn_ver_asistencias.grid(row=1, column=2, padx=10, pady=5)

            # Treeview para mostrar resultados
            columns = ("Fecha", "Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
            self.treeview_estudiantes = ttk.Treeview(self.root, columns=columns, show='headings')
            for col in columns:
                self.treeview_estudiantes.heading(col, text=col)
                self.treeview_estudiantes.column(col, width=100)
            self.treeview_estudiantes.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

            # Botones para guardar asistencia y ver todas las asistencias
            self.btn_guardar_asistencia = tk.Button(self.root, text="Guardar Asistencia", command=self.guardar_asistencia)
            self.btn_guardar_asistencia.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

            self.btn_ver_todas_asistencias = tk.Button(self.root, text="Ver Todas las Asistencias", command=self.ver_todas_asistencias)
            self.btn_ver_todas_asistencias.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

            # Asociar evento de clic en el Treeview
            self.treeview_estudiantes.bind("<ButtonRelease-1>", self.on_treeview_click)

        def create_table_asistencia(self):
            self.c_asistencia.execute('''
                CREATE TABLE IF NOT EXISTS asistencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_estudiante INTEGER,
                    fecha TEXT,
                    lunes BOOLEAN,
                    martes BOOLEAN,
                    miércoles BOOLEAN,
                    jueves BOOLEAN,
                    viernes BOOLEAN,
                    FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
                )
            ''')
            self.conn_asistencia.commit()

        def populate_grado_combobox(self):
            grados = self.obtener_grados()
            self.combo_grado['values'] = grados

        def obtener_grados(self):
            self.c_matricula.execute("SELECT DISTINCT grado_curso FROM matricula")
            grados = [row[0] for row in self.c_matricula.fetchall()]
            return grados

        def ver_asistencias(self):
            fecha = self.entry_fecha.get().strip()
            grado = self.combo_grado.get()

            if not fecha:
                messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
                return

            # Limpiar el Treeview antes de cargar nuevos datos
            self.treeview_estudiantes.delete(*self.treeview_estudiantes.get_children())

            # Consultar la base de datos para obtener los estudiantes y su asistencia
            self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
            estudiantes = self.c_matricula.fetchall()

            for estudiante in estudiantes:
                estudiante_id, nombre, apellido = estudiante

                # Obtener la asistencia del estudiante para la fecha especificada
                self.c_asistencia.execute("SELECT lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ? AND fecha = ?",
                                        (estudiante_id, fecha))
                asistencia = self.c_asistencia.fetchone()

                if asistencia:
                    lunes = "Asistió" if asistencia[0] else "No asistió"
                    martes = "Asistió" if asistencia[1] else "No asistió"
                    miercoles = "Asistió" if asistencia[2] else "No asistió"
                    jueves = "Asistió" if asistencia[3] else "No asistió"
                    viernes = "Asistió" if asistencia[4] else "No asistió"
                else:
                    lunes = martes = miercoles = jueves = viernes = "No asistió"

                self.treeview_estudiantes.insert("", "end", values=(fecha, nombre, apellido, grado, lunes, martes, miercoles, jueves, viernes))

        def guardar_asistencia(self):
            fecha = self.entry_fecha.get().strip()
            if not fecha:
                messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
                return
            
            # Iterar sobre todos los estudiantes en el Treeview
            for item_id in self.treeview_estudiantes.get_children():
                estudiante_id = self.treeview_estudiantes.item(item_id)["text"]
                # Obtener los valores de asistencia de cada día
                lunes = self.treeview_estudiantes.set(item_id, "Lunes") == "Asistió"
                martes = self.treeview_estudiantes.set(item_id, "Martes") == "Asistió"
                miercoles = self.treeview_estudiantes.set(item_id, "Miércoles") == "Asistió"
                jueves = self.treeview_estudiantes.set(item_id, "Jueves") == "Asistió"
                viernes = self.treeview_estudiantes.set(item_id, "Viernes") == "Asistió"
                
                try:
                    self.c_asistencia.execute('''
                        INSERT INTO asistencia (id_estudiante, fecha, lunes, martes, miércoles, jueves, viernes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (estudiante_id, fecha, lunes, martes, miercoles, jueves, viernes))
                    self.conn_asistencia.commit()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al guardar asistencia: {e}")
                    return
            
            messagebox.showinfo("Asistencia Guardada", f"Asistencia para la fecha {fecha} guardada exitosamente.")

        def on_treeview_click(self, event):
            item = self.treeview_estudiantes.identify('item', event.x, event.y)
            column = self.treeview_estudiantes.identify_column(event.x)
            
            # Verificar si se hizo clic en una columna de asistencia
            if column in ["#5", "#6", "#7", "#8", "#9"]:  # Columnas correspondientes a Lunes, Martes, Miércoles, Jueves, Viernes
                column_id = self.treeview_estudiantes["columns"].index(self.treeview_estudiantes.heading(column)["text"])
                current_value = self.treeview_estudiantes.item(item, "values")[column_id]

                # Cambiar el valor actual
                new_value = "Asistió" if current_value == "No asistió" else "No asistió"
                self.treeview_estudiantes.set(item, column, new_value)

        def ver_todas_asistencias(self):
            def obtener_asistencias():
                grado = entry_grado.get().strip()
                nombre_buscar = entry_nombre.get().strip()
                
                if not grado:
                    messagebox.showerror("Error", "Ingrese un grado válido.")
                    return

                # Limpiar el Treeview antes de cargar nuevos datos
                tree.delete(*tree.get_children())

                # Consultar la base de datos para obtener todos los estudiantes en el grado seleccionado
                self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
                estudiantes = self.c_matricula.fetchall()

                for estudiante in estudiantes:
                    estudiante_id, nombre, apellido = estudiante

                    if nombre_buscar.lower() not in nombre.lower():
                        continue

                    # Obtener todas las asistencias del estudiante
                    self.c_asistencia.execute("SELECT fecha, lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ?",
                                            (estudiante_id,))
                    asistencias = self.c_asistencia.fetchall()

                    for asistencia in asistencias:
                        fecha, lunes, martes, miercoles, jueves, viernes = asistencia

                        # Convertir booleanos a texto
                        lunes = "Asistió" if lunes else "No asistió"
                        martes = "Asistió" if martes else "No asistió"
                        miercoles = "Asistió" if miercoles else "No asistió"
                        jueves = "Asistió" if jueves else "No asistió"
                        viernes = "Asistió" if viernes else "No asistió"

                        tree.insert("", "end", values=(f"{nombre} {apellido}", fecha, lunes, martes, miercoles, jueves, viernes))

            # Crear ventana secundaria para buscar todas las asistencias
            ventana_todas_asistencias = tk.Toplevel(self.root)
            ventana_todas_asistencias.title("Buscar Asistencias por Grado")

            # Crear un frame para la entrada
            frame_entrada = tk.Frame(ventana_todas_asistencias)
            frame_entrada.pack(padx=10, pady=10)

            # Etiqueta y entrada para el grado
            label_grado = tk.Label(frame_entrada, text="Grado:")
            label_grado.grid(row=0, column=0, padx=5, pady=5)
            entry_grado = tk.Entry(frame_entrada)
            entry_grado.grid(row=0, column=1, padx=5, pady=5)

            # Etiqueta y entrada para el nombre
            label_nombre = tk.Label(frame_entrada, text="Nombre:")
            label_nombre.grid(row=1, column=0, padx=5, pady=5)
            entry_nombre = tk.Entry(frame_entrada)
            entry_nombre.grid(row=1, column=1, padx=5, pady=5)

            # Botón para buscar
            btn_buscar = tk.Button(frame_entrada, text="Buscar", command=obtener_asistencias)
            btn_buscar.grid(row=2, columnspan=2, pady=10)

            # Crear el árbol para mostrar resultados
            columns = ("Nombre", "Fecha", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
            tree = ttk.Treeview(ventana_todas_asistencias, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        def __del__(self):
            self.conn_matricula.close()
            self.conn_asistencia.close()

    if __name__ == "__main__":
        root = tk.Tk()
        app = AsistenciaGUI(root)
        root.mainloop()


        if __name__ == "__main__":
            root = tk.Tk()
            app = AsistenciaGUI(root)
            root.mainloop()

def MATRIX_DOCENTE():
    class AsistenciaGUI:
        def __init__(self, root, grado):
            self.root = root
            self.grado = grado
            self.root.title("Registro de Asistencia por Grado")

            # Inicializar base de datos de matrícula y asistencia
            self.conn_matricula = sqlite3.connect('matricula.db')
            self.c_matricula = self.conn_matricula.cursor()

            self.conn_asistencia = sqlite3.connect('asistencia.db')
            self.c_asistencia = self.conn_asistencia.cursor()
            self.create_table_asistencia()

            # Crear widgets
            self.create_widgets()
            self.populate_grado_combobox()

            # Mostrar el grado actual en la interfaz
            self.combo_grado.set(self.grado)

        def create_widgets(self):
            # Etiqueta y combo para seleccionar grado
            self.label_grado = tk.Label(self.root, text="Seleccionar Grado:")
            self.label_grado.grid(row=0, column=0, padx=10, pady=5)
            self.combo_grado = ttk.Combobox(self.root, state="disabled")
            self.combo_grado.grid(row=0, column=1, padx=10, pady=5)

            # Etiqueta y entrada para la fecha
            self.label_fecha = tk.Label(self.root, text="Fecha (YYYY-MM-DD):")
            self.label_fecha.grid(row=1, column=0, padx=10, pady=5)
            self.entry_fecha = tk.Entry(self.root)
            self.entry_fecha.grid(row=1, column=1, padx=10, pady=5)

            # Botón para ver asistencias
            self.btn_ver_asistencias = tk.Button(self.root, text="Ver Asistencias", command=self.ver_asistencias)
            self.btn_ver_asistencias.grid(row=1, column=2, padx=10, pady=5)

            # Treeview para mostrar resultados
            columns = ("Fecha", "Nombres", "Apellidos", "Grado", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
            self.treeview_estudiantes = ttk.Treeview(self.root, columns=columns, show='headings')
            for col in columns:
                self.treeview_estudiantes.heading(col, text=col)
                self.treeview_estudiantes.column(col, width=100)
            self.treeview_estudiantes.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

            # Botones para guardar asistencia y ver todas las asistencias
            self.btn_guardar_asistencia = tk.Button(self.root, text="Guardar Asistencia", command=self.guardar_asistencia)
            self.btn_guardar_asistencia.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

            self.btn_ver_todas_asistencias = tk.Button(self.root, text="Ver Todas las Asistencias", command=self.ver_todas_asistencias)
            self.btn_ver_todas_asistencias.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="WE")

            # Asociar evento de clic en el Treeview
            self.treeview_estudiantes.bind("<ButtonRelease-1>", self.on_treeview_click)

        def create_table_asistencia(self):
            self.c_asistencia.execute('''
                CREATE TABLE IF NOT EXISTS asistencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_estudiante INTEGER,
                    fecha TEXT,
                    lunes BOOLEAN,
                    martes BOOLEAN,
                    miércoles BOOLEAN,
                    jueves BOOLEAN,
                    viernes BOOLEAN,
                    FOREIGN KEY (id_estudiante) REFERENCES matricula (id)
                )
            ''')
            self.conn_asistencia.commit()

        def populate_grado_combobox(self):
            # Opcional: Población del combobox con grados disponibles
            # Aquí no se necesita porque el grado es fijo
            pass

        def ver_asistencias(self):
            fecha = self.entry_fecha.get().strip()
            grado = self.combo_grado.get()

            if not fecha:
                messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
                return

            # Limpiar el Treeview antes de cargar nuevos datos
            self.treeview_estudiantes.delete(*self.treeview_estudiantes.get_children())

            # Consultar la base de datos para obtener los estudiantes y su asistencia
            self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (self.grado,))
            estudiantes = self.c_matricula.fetchall()

            for estudiante in estudiantes:
                estudiante_id, nombre, apellido = estudiante

                # Obtener la asistencia del estudiante para la fecha especificada
                self.c_asistencia.execute("SELECT lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ? AND fecha = ?",
                                        (estudiante_id, fecha))
                asistencia = self.c_asistencia.fetchone()

                if asistencia:
                    lunes = "Asistió" if asistencia[0] else "No asistió"
                    martes = "Asistió" if asistencia[1] else "No asistió"
                    miercoles = "Asistió" if asistencia[2] else "No asistió"
                    jueves = "Asistió" if asistencia[3] else "No asistió"
                    viernes = "Asistió" if asistencia[4] else "No asistió"
                else:
                    lunes = martes = miercoles = jueves = viernes = "No asistió"

                self.treeview_estudiantes.insert("", "end", values=(fecha, nombre, apellido, self.grado, lunes, martes, miercoles, jueves, viernes))

        def guardar_asistencia(self):
            fecha = self.entry_fecha.get().strip()
            if not fecha:
                messagebox.showerror("Error", "Ingrese una fecha válida (YYYY-MM-DD).")
                return

            # Iterar sobre todos los estudiantes en el Treeview
            for item_id in self.treeview_estudiantes.get_children():
                estudiante_id = self.treeview_estudiantes.item(item_id)["text"]
                # Obtener los valores de asistencia de cada día
                lunes = self.treeview_estudiantes.set(item_id, "Lunes") == "Asistió"
                martes = self.treeview_estudiantes.set(item_id, "Martes") == "Asistió"
                miercoles = self.treeview_estudiantes.set(item_id, "Miércoles") == "Asistió"
                jueves = self.treeview_estudiantes.set(item_id, "Jueves") == "Asistió"
                viernes = self.treeview_estudiantes.set(item_id, "Viernes") == "Asistió"

                try:
                    self.c_asistencia.execute('''
                        INSERT INTO asistencia (id_estudiante, fecha, lunes, martes, miércoles, jueves, viernes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (estudiante_id, fecha, lunes, martes, miercoles, jueves, viernes))
                    self.conn_asistencia.commit()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al guardar asistencia: {e}")
                    return

            messagebox.showinfo("Asistencia Guardada", f"Asistencia para la fecha {fecha} guardada exitosamente.")

        def on_treeview_click(self, event):
            item = self.treeview_estudiantes.identify('item', event.x, event.y)
            column = self.treeview_estudiantes.identify_column(event.x)
            
            # Verificar si se hizo clic en una columna de asistencia
            if column in ["#5", "#6", "#7", "#8", "#9"]:  # Columnas correspondientes a Lunes, Martes, Miércoles, Jueves, Viernes
                column_id = self.treeview_estudiantes["columns"].index(self.treeview_estudiantes.heading(column)["text"])
                current_value = self.treeview_estudiantes.item(item, "values")[column_id]

                # Cambiar el valor actual
                new_value = "Asistió" if current_value == "No asistió" else "No asistió"
                self.treeview_estudiantes.set(item, column, new_value)

        def ver_todas_asistencias(self):
            def obtener_asistencias():
                grado = entry_grado.get().strip()
                nombre_buscar = entry_nombre.get().strip()
                
                if not grado:
                    messagebox.showerror("Error", "Ingrese un grado válido.")
                    return

                # Limpiar el Treeview antes de cargar nuevos datos
                tree.delete(*tree.get_children())

                # Consultar la base de datos para obtener todos los estudiantes en el grado seleccionado
                self.c_matricula.execute("SELECT id, nombres, apellidos FROM matricula WHERE grado_curso = ?", (grado,))
                estudiantes = self.c_matricula.fetchall()

                for estudiante in estudiantes:
                    estudiante_id, nombre, apellido = estudiante

                    if nombre_buscar.lower() not in nombre.lower():
                        continue

                    # Obtener todas las asistencias del estudiante
                    self.c_asistencia.execute("SELECT fecha, lunes, martes, miércoles, jueves, viernes FROM asistencia WHERE id_estudiante = ?",
                                            (estudiante_id,))
                    asistencias = self.c_asistencia.fetchall()

                    for asistencia in asistencias:
                        fecha, lunes, martes, miercoles, jueves, viernes = asistencia

                        # Convertir booleanos a texto
                        lunes = "Asistió" if lunes else "No asistió"
                        martes = "Asistió" if martes else "No asistió"
                        miercoles = "Asistió" if miercoles else "No asistió"
                        jueves = "Asistió" if jueves else "No asistió"
                        viernes = "Asistió" if viernes else "No asistió"

                        tree.insert("", "end", values=(f"{nombre} {apellido}", fecha, lunes, martes, miercoles, jueves, viernes))

            # Crear ventana secundaria para buscar todas las asistencias
            ventana_todas_asistencias = tk.Toplevel(self.root)
            ventana_todas_asistencias.title("Buscar Asistencias por Grado")

            # Crear un frame para la entrada
            frame_entrada = tk.Frame(ventana_todas_asistencias)
            frame_entrada.pack(padx=10, pady=10)

            # Etiqueta y entrada para el grado
            label_grado = tk.Label(frame_entrada, text="Grado:")
            label_grado.grid(row=0, column=0, padx=5, pady=5)
            entry_grado = tk.Entry(frame_entrada)
            entry_grado.grid(row=0, column=1, padx=5, pady=5)

            # Etiqueta y entrada para el nombre
            label_nombre = tk.Label(frame_entrada, text="Nombre:")
            label_nombre.grid(row=1, column=0, padx=5, pady=5)
            entry_nombre = tk.Entry(frame_entrada)
            entry_nombre.grid(row=1, column=1, padx=5, pady=5)

            # Botón para buscar
            btn_buscar = tk.Button(frame_entrada, text="Buscar", command=obtener_asistencias)
            btn_buscar.grid(row=2, columnspan=2, pady=10)

            # Crear el árbol para mostrar resultados
            columns = ("Nombre", "Fecha", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes")
            tree = ttk.Treeview(ventana_todas_asistencias, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        def __del__(self):
            self.conn_matricula.close()
            self.conn_asistencia.close()

    if __name__ == "__main__":
        root = tk.Tk()
        app = AsistenciaGUI(root, grado="2")  # Cambia el grado según sea necesario
        root.mainloop()



if __name__ == "__main__":
    
    root =Tk()
    top.mainloop()
    root.mainloop()


