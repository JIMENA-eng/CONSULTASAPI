from tkinter import*
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import requests
import datetime
from fpdf import FPDF
import xlsxwriter
from datetime import datetime
from tkinter import font
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import tempfile


def inicio_dmin():
    top.destroy()
    root=Tk()
    root.title("ADMINISTRADOR INICIO DE SESION")
    root.geometry("300x250")
    root.configure(background='lightblue')
    
    
    lb_usuario=tk.Label(root, text='USUARIO:')
    lb_usuario.grid(row=0, padx=10,pady=5, sticky=tk.W)
    en_usuario=tk.Entry(root)
    en_usuario.grid(row=0, column=1, padx=10, pady=5)
    
    lb_contraseña=tk.Label(root, text='CONTRASEÑA:')
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
    
    bt_inicio=tk.Button(root, text='iniciar sesion', command=ver_admin)
    bt_inicio.grid(row=2, columnspan=2, padx=10, pady=10)
    
def inicio_usuario():
    top.destroy()
    messagebox.showinfo('inicio de sesion', 'sesion inicia como usuario')

top=Tk()
top.title('seleciona tipo de usuario')
top.geometry("500x300")
top.configure(background='lightblue')

fuente_actual = font.Font(family="Times New Roman", size=20)

# Función para cambiar la fuente y tamaño del texto
def cambiar_fuente_tamano():
    global fuente_actual
    # Cambiar la familia de fuente y el tamaño
    fuente_actual.configure(family="Arial", size=16)  # Cambiar a Arial y tamaño 16
    # Aplicar la nueva fuente al texto en la etiqueta
    lb_user.config(font=fuente_actual)

lb_user = tk.Label(top, text='SELECCIONE SU INICIO DE SESION:', bg='lightblue', font=fuente_actual)
lb_user.pack()
bt_admin=tk.Button(top, text='INICIAR SESION COMO ADMINISTRADOR', command=inicio_dmin, bg='lightblue')
bt_admin.pack(pady=20)
bt_usuario=tk.Button(top, text='INICIAR SESION COMO USUARIO', command=inicio_usuario, bg='lightblue')
bt_usuario.pack(pady=20)

def DNI():
    def dni_consultar():
        dni=en_dni.get()
        if not dni:
            messagebox.showwarning('advertencia', 'por favor ingrese un numero de DNI')
            return
        try:
            url=f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if response.status_code == 200:
                if not data ['success']:
                    messagebox.showinfo("DNI no registrado", "el DNI no se encuentra registrado")
                else:
                    mostrar_datos(data)
            else:
                messagebox.showerror("Error en la consulta", f"Código de estado: {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error en la consulta", f"Error de conexión: {str(e)}")
    def mostrar_datos(data):
        wen.destroy()
        ven_da=tk.Toplevel()
        ven_da.title('DATOS DEL DNI')
        
        tk.Label(ven_da, text=f'DNI: {data["dni"]}').pack(padx=10, pady=5)
        tk.Label(ven_da, text=f'Nombres: {data["nombres"]}').pack(padx=10, pady=5)
        tk.Label(ven_da, text=f'Apellido Paterno: {data["apellidoPaterno"]}').pack(padx=10, pady=5)
        tk.Label(ven_da, text=f'Apellido Materno: {data["apellidoMaterno"]}').pack(padx=10, pady=5)

        # Sección para ingresar el estado civil
        frame_estado_civil = tk.LabelFrame(ven_da, text="Estado Civil")
        frame_estado_civil.pack(padx=10, pady=5, fill="both", expand="yes")

        estado_civil_options = ["Soltero/a", "Casado/a", "Viudo/a", "Divorciado/a", "Conviviente", "Otro"]

        estado_civil = tk.StringVar()
        estado_civil.set("")  # Valor inicial

        for option in estado_civil_options:
            tk.Radiobutton(frame_estado_civil, text=option, variable=estado_civil, value=option).pack(anchor="w")

        # Botones de género (ejemplo básico)
        tk.Label(ven_da, text="Género:").pack(padx=10, pady=5)
        tk.Button(ven_da, text="Femenino", command=lambda: guardar_en_db(data, "Femenino", estado_civil.get())).pack(pady=5)
        tk.Button(ven_da, text="Masculino", command=lambda: guardar_en_db(data, "Masculino", estado_civil.get())).pack(pady=5)
        tk.Button(ven_da, text="Otros", command=lambda: guardar_en_db(data, "Otros", estado_civil.get())).pack(pady=5)

        # Botón para cerrar ventana
        btn_cerrar = tk.Button(ven_da, text='registrar', command=ven_da.destroy)
        btn_cerrar.pack(pady=10)
        
    def guardar_en_db(data, genero, estado_civil):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('asistencia.db')
            cursor = conn.cursor()

            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insertar los datos en la tabla 'asistencia' junto con la fecha y hora
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
    wen = Tk()
    wen.title('Consulta de DNI')

    # Etiqueta y entrada para ingresar el número de DNI
    label_dni = tk.Label(wen, text='Ingrese el número de DNI:')
    label_dni.pack(pady=10)

    en_dni = tk.Entry(wen)
    en_dni.pack(pady=5)

    # Botón para consultar el DNI (se activará también con Enter)
    btn_consultar = tk.Button(wen, text='Consultar DNI', command=dni_consultar)
    btn_consultar.pack(pady=10)

    # Atajo para activar la función dni_consultar al presionar Enter en la entrada de texto
    en_dni.bind('<Return>', lambda event: dni_consultar())



def exportar_a_pdf():
    try:
        # Conexión a la base de datos
        miConexion = sqlite3.connect("asistencia.db")
        miCursor = miConexion.cursor()
        
        # Consulta para obtener todos los registros
        miCursor.execute("SELECT * FROM empleados")
        registros = miCursor.fetchall()
        
        # Configuración del documento PDF con orientación vertical
        class PDF(FPDF):
            def __init__(self):
                super().__init__()
                self.format = (210, 297)  # Tamaño A4 en orientación vertical (297 mm x 210 mm)
                self.orientation = 'L'    # Orientación vertical

        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Títulos de las columnas
        columnas = ["ID", "NOMBRES", "APELLIDO PATERNO", "APELLIDO MATERNO", "DNI", "GENERO", "ESTADO CIVIL", "FECHA Y HORA"]
        pdf.set_fill_color(200, 220, 255)
        for col in columnas:
            pdf.cell(30, 10, col, 1, 0, 'C', 1)
        
        # Agregar registros al PDF
        pdf.set_fill_color(255, 255, 255)
        pdf.ln()
        for row in registros:
            for dato in row:
                pdf.cell(30, 10, str(dato), 1, 0, 'C')
            pdf.ln()
        
        # Guardar el PDF
        pdf.output("registros_asistencia_vertical.pdf")
        messagebox.showinfo("Exportar a PDF", "Datos exportados a registros_asistencia_vertical.pdf")
        
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
        workbook = xlsxwriter.Workbook('registros_asistencia.xlsx')
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
        messagebox.showinfo("Exportar a Excel", "Datos exportados a registros_asistencia.xlsx")
        
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
        root.configure(bg='light green')

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
            ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen del DNI",
                                                    filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp"), ("Todos los archivos", "*.*")))
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
            else:
                messagebox.showinfo("Escaneo de DNI", "No se encontró ningún código de barras válido en la imagen.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al escanear el código de barras: {str(e)}")

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Escaneo de DNI")
    root.geometry("400x200")
    root.configure(background='lightgreen')

    # Botón para escanear el código de barras del DNI
    btn_escanear = tk.Button(root, text="Escanear DNI", command=escanear_dni)
    btn_escanear.pack(pady=20)


def diario():
    def mostrar_registros_diarios():
        try:
            fecha_actual = datetime.date.today()
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM empleados WHERE DATE(FECHA_HORA_ENTRADA) = ?", (fecha_actual,))
            registros = miCursor.fetchall()
            ventan_reportes()
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al mostrar registros diarios: {error}")

def semana():
    def mostrar_registros_semanales():
        try:
            fecha_actual = datetime.date.today()
            fecha_inicio_semana = fecha_actual - datetime.timedelta(days=fecha_actual.weekday())
            fecha_fin_semana = fecha_inicio_semana + datetime.timedelta(days=6)
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM empleados WHERE DATE(FECHA_HORA_ENTRADA) BETWEEN ? AND ?", (fecha_inicio_semana, fecha_fin_semana))
            registros = miCursor.fetchall()
            ventan_reportes()
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al mostrar registros semanales: {error}")

def mes():
    def mostrar_registros_mensuales():
        try:
            fecha_actual = datetime.date.today()
            primer_dia_mes = fecha_actual.replace(day=1)
            ultimo_dia_mes = fecha_actual.replace(day=datetime.date.today().day)
            miConexion = sqlite3.connect("asistencia.db")
            miCursor = miConexion.cursor()
            miCursor.execute("SELECT * FROM empleados WHERE DATE(FECHA_HORA_ENTRADA) BETWEEN ? AND ?", (primer_dia_mes, ultimo_dia_mes))
            registros = miCursor.fetchall()
            ventan_reportes()
        except sqlite3.Error as error:
            messagebox.showerror("ERROR", f"Error al mostrar registros mensuales: {error}")
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
    root.configure(background='lightgreen')


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
    
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=250)
    
    tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    tree_scroll_x.config(command=tree.xview)

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
    repormenu.add_command(label="reporte diario", command=diario)
    repormenu.add_command(label="reporte semanal", command=semana)
    repormenu.add_command(label="reporte mensual", command=mes)
    menubar.add_cascade(label="reportes", menu=repormenu)

    expomenu=Menu(menubar, tearoff=0)
    expomenu.add_command(label="exportar datos a excel", command=exportar_a_excel)
    expomenu.add_command(label="descargar datos en pdf", command=exportar_a_pdf)
    menubar.add_cascade(label="exportar", menu=expomenu)
    
    subirmenu=Menu(menubar, tearoff=0)
    subirmenu.add_command(label="subir documento")
    
    lectormenu=Menu(menubar, tearoff=0)
    lectormenu.add_command(label="escaneo por camara de computadora", command=escaneo_camara)
    lectormenu.add_command(label="escaneo por archivos", command=escaneo_archivos)
    lectormenu.add_command(label="lector digital de dni")
    menubar.add_cascade(label="escaneo", menu=lectormenu)


    ayudamenu=Menu(menubar, tearoff=0)
    ayudamenu.add_command(label="resetear campos", command=limpiarCampos)
    ayudamenu.add_command(label="acerca", command=mensaje)
    menubar.add_cascade(label="ayuda",menu=ayudamenu)


    e1=Entry(root, textvariable=miID)

    l2=Label(root,text="NOMBRES")
    l2.place(x=50,y=10)
    e2=Entry(root,textvariable=miNombres, width=50)
    e2.place(x=100,y=10)

    l3=Label(root,text="APELLIDO PATERNO")
    l3.place(x=50,y=40)
    e3=Entry(root,textvariable=miApellidoPaterno)
    e3.place(x=100,y=40)

    l4=Label(root,text="APELLIDO MATERNO")
    l4.place(x=50,y=60)
    e4=Entry(root, textvariable=miApellidoMaterno, width=10)
    e4.place(x=100,y=60)

    l5=Label(root, text="DNI")
    l5.place(x=50,y=80)
    e5=Entry(root, textvariable=miDNI, width=10)
    e5.place(x=100,y=80)

    l6=Label(root,text="GENERO")
    l6.place(x=50,y=100)
    e6=Entry(root,textvariable=miGenero, width=10)
    e6.place(x=100,y=100)
    
    l7=Label(root, text="ESTADO CIVIL")
    l7.place(x=50,y=120)
    e7=Entry(root, textvariable=miEstado_civil, width=10)
    e7.place(x=100,y=120)

    b1=Button(root, text="crear registro", command=crear)
    b1.place(x=90,y=250)
    b2=Button(root, text="modificar registro", command=actualizar)
    b2.place(x=150,y=250)
    b3=Button(root, text="mostrar lista", command=mostrar)
    b3.place(x=350, y=250)
    b4=Button(root, text="eliminar registro", bg="blue", command=borrar)
    b4.place(x=500,y=250)

    root.config(menu=menubar)
    conexionBBDD()


if __name__ == "__main__":
    root =Tk()
    top.mainloop()
    root.mainloop()


