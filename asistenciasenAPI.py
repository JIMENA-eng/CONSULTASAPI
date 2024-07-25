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
    messagebox.showinfo('inicio de sesion', 'sesion inicia como usuario')
    MATRIX()

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

def  escaneo_camara ():
   def escanear_dni_camara():
    try:
        # Configurar la captura de video desde la cámara
        cap = cv2.VideoCapture(0)

        # Función para actualizar la imagen de la cámara en el widget tkinter
        def actualizar_camara():
            ret, frame = cap.read()
            if ret:
                # Convertir la imagen de OpenCV a formato de imagen de PIL
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img)
                img_tk = ImageTk.PhotoImage(image=img_pil)

                # Actualizar la etiqueta con la imagen de la cámara
                lbl_camara.img_tk = img_tk  # Mantener una referencia para evitar que Python la elimine automáticamente
                lbl_camara.config(image=img_tk)

            # Llamar a esta función nuevamente después de 10 ms
            lbl_camara.after(10, actualizar_camara)

        # Crear la ventana principal de tkinter
        root = tk.Tk()
        root.title("Escaneo de DNI con cámara")
        root.geometry("800x600")
        root.configure(bg='lightgreen')

        # Etiqueta para mostrar la imagen de la cámara
        lbl_camara = tk.Label(root)
        lbl_camara.pack(padx=10, pady=10)

        # Botón para escanear el código de barras del DNI con la cámara
        btn_escanear = tk.Button(root, text="Escanear DNI", command=lambda: escanear_dni(cap))
        btn_escanear.pack(pady=20)

        # Función para escanear el código de barras del DNI
        def escanear_dni(cap):
            try:
                # Capturar una sola imagen
                ret, frame = cap.read()

                # Guardar la imagen en un archivo temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                cv2.imwrite(temp_file.name, frame)

                # Cargar la imagen con Pillow y convertirla a escala de grises
                imagen = Image.open(temp_file.name).convert('L')

                # Decodificar el código de barras usando pyzbar
                resultado = decode(imagen)

                if resultado:
                    # Mostrar el código de barras encontrado
                    codigo = resultado[0].data.decode('utf-8')
                    messagebox.showinfo("Escaneo de DNI", f"Código de barras encontrado:\n{codigo}")
                    guardar_en_base_de_datos(codigo)
                else:
                    messagebox.showinfo("Escaneo de DNI", "No se encontró ningún código de barras válido.")

            except Exception as e:
                messagebox.showerror("Error", f"Error al escanear el código de barras: {str(e)}")

        # Función para guardar los datos en la base de datos
        def guardar_en_base_de_datos(dni):
            # Aquí deberías adaptar la lógica para guardar en tu base de datos SQLite
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()

            # Supongamos que aquí se guarda el número de DNI y la fecha actual en la tabla empleados
            now = datetime.now()
            fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")
            miCursor.execute('''INSERT INTO empleados (DNI, FECHA_HORA)
                                VALUES (?, ?)''', (dni, fecha_hora))
            miConexion.commit()

            miConexion.close()

        # Iniciar la actualización de la cámara
        actualizar_camara()

        # Ejecutar la interfaz gráfica de tkinter
        root.mainloop()

        # Liberar la captura de la cámara al cerrar la ventana
        cap.release()

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la cámara: {str(e)}")

# Llamar a la función para escanear el DNI con la cámara
    escanear_dni_camara()
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
        dni = miDNI.get()
        try:
            # Conexión a la base de datos
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            
            # Consulta para buscar registros por DNI
            miCursor.execute("SELECT * FROM empleados WHERE DNI=?", (dni,))
            registros = miCursor.fetchall()
            
            # Limpiar resultados anteriores en el Treeview
            for row in tree.get_children():
                tree.delete(row)
            
            # Mostrar resultados en el Treeview
            if registros:
                for registro in registros:
                    tree.insert("", "end", text=registro[0], values=(registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7]))
            else:
                messagebox.showinfo("Sin resultados", f"No se encontraron registros con el DNI {dni}.")
        
        except sqlite3.Error as error:
            messagebox.showerror("Error", f"Error al buscar por DNI: {error}")
        finally:
            # Cerrar la conexión a la base de datos
            if miConexion:
                miConexion.close()
        
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
    lectormenu.add_command(label="escaneo por camara de computadora", command=escaneo_camara)
    lectormenu.add_command(label="escaneo por archivos", command=escaneo_archivos)
    lectormenu.add_command(label="lector digital de dni")
    menubar.add_cascade(label="escaneo", menu=lectormenu)
    
    subirmenu=Menu(menubar, tearoff=0)
    subirmenu.add_command(label="subir archivo de excel", command=cargar_a_la_data)
    menubar.add_cascade(label="subir archivos", menu=subirmenu)
    
    matrixmenu=Menu(menubar, tearoff=0)
    matrixmenu.add_command(label="registar alumnos", command=MATRIX)
    menubar.add_cascade(label="registro alumnos", menu=matrixmenu)
    
    matrimenu=Menu(menubar, tearoff=0)
    matrimenu.add_command(label="SEMESTRES")
    menubar.add_cascade(label="matriculas", menu=matrixmenu)

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
    r2=Entry(root, width=10)
    r2.place(x=900, y=10)
    

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
    
def MATRIX():

    # Desarrollo de la Interfaz grafica
    root=Tk()
    root.title("REGISTROS DE ESTUDIANTES")
    root.geometry("600x350")

    miId=StringVar()
    miNombre=StringVar()
    miCargo=StringVar()
    miSalario=StringVar()

    def conexionBBDD():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()

        try:
            miCursor.execute('''
                CREATE TABLE empleado (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50) NOT NULL,
                CARGO VARCHAR(50) NOT NULL,
                SALARIO INT NOT NULL)
                ''')
            messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")
        except:
            messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")

    def eliminarBBDD():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()
        if messagebox.askyesno(message="¿Los Datos se perderan definitivamente, Desea continuar?", title="ADVERTENCIA"):
            miCursor.execute("DROP TABLE empleado")
        else:
            pass
        limpiarCampos()
        mostrar()

    def salirAplicacion():
        valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
        if valor=="yes":
            root.destroy()

    def limpiarCampos():
        miId.set("")
        miNombre.set("")
        miCargo.set("")
        miSalario.set("")

    def mensaje():
        acerca='''
        Aplicación CRUD
        Version 1.0
        Tecnología Python Tkinter
        '''
        messagebox.showinfo(title="INFORMACION", message=acerca)

    ################################ Métodos CRUD ##############################

    def crear():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()
        try:
            datos=miNombre.get(),miCargo.get(),miSalario.get()
            miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", (datos))
            miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con BBDD")
            pass
        limpiarCampos()
        mostrar()

    def mostrar():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()
        registros=tree.get_children()
        for elemento in registros:
            tree.delete(elemento)

        try:
            miCursor.execute("SELECT * FROM empleado")
            for row in miCursor:
                tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
        except:
            pass

                    ################################## Tabla ################################
    tree=ttk.Treeview(height=10, columns=('#0','#1','#2'))
    tree.place(x=0, y=130)
    tree.column('#0',width=100)
    tree.heading('#0', text="ID", anchor=CENTER)
    tree.heading('#1', text="Nombre del Empleado", anchor=CENTER)
    tree.heading('#2', text="Cargo", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Salario", anchor=CENTER)

    def seleccionarUsandoClick(event):
        item=tree.identify('item',event.x,event.y)
        miId.set(tree.item(item,"text"))
        miNombre.set(tree.item(item,"values")[0])
        miCargo.set(tree.item(item,"values")[1])
        miSalario.set(tree.item(item,"values")[2])

    tree.bind("<Double-1>", seleccionarUsandoClick)



    def actualizar():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()
        try:
            datos=miNombre.get(),miCargo.get(),miSalario.get()
            miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=? WHERE ID="+miId.get(), (datos))
            miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
            pass
        limpiarCampos()
        mostrar()

    def borrar():
        miConexion=sqlite3.connect("base")
        miCursor=miConexion.cursor()
        try:
            if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
                miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
                miConexion.commit()
        except:
            messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
            pass
        limpiarCampos()
        mostrar()

    ###################### Colocar widgets en la VISTA ######################
    ########## Creando Los menus ###############
    menubar=Menu(root)
    menubasedat=Menu(menubar,tearoff=0)
    menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
    menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
    menubasedat.add_command(label="Salir", command=salirAplicacion)
    menubar.add_cascade(label="Inicio", menu=menubasedat)

    ayudamenu=Menu(menubar,tearoff=0)
    ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
    ayudamenu.add_command(label="Acerca", command=mensaje)
    menubar.add_cascade(label="Ayuda",menu=ayudamenu)

    ############## Creando etiquetas y cajas de texto ###########################
    e1=Entry(root, textvariable=miId)

    l2=Label(root, text="Nombre")
    l2.place(x=50,y=10)
    e2=Entry(root, textvariable=miNombre, width=50)
    e2.place(x=100, y=10)

    l3=Label(root, text="Cargo")
    l3.place(x=50,y=40)
    e3=Entry(root, textvariable=miCargo)
    e3.place(x=100, y=40)

    l4=Label(root, text="Salario")
    l4.place(x=280,y=40)
    e4=Entry(root, textvariable=miSalario, width=10)
    e4.place(x=320, y=40)

    l5=Label(root, text="USD")
    l5.place(x=380,y=40)

    ################# Creando botones ###########################

    b1=Button(root, text="Crear Registro", command=crear)
    b1.place(x=50, y=90)
    b2=Button(root, text="Modificar Registro", command=actualizar)
    b2.place(x=180, y=90)
    b3=Button(root, text="Mostrar Lista", command=mostrar)
    b3.place(x=320, y=90)
    b4=Button(root, text="Eliminar Registro",bg="red", command=borrar)
    b4.place(x=450, y=90)


    root.config(menu=menubar)


    root.mainloop()


if __name__ == "__main__":
    
    root =Tk()
    top.mainloop()
    root.mainloop()


