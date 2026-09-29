import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from Clases.classProducto import Producto
from Clases.classCategoria import Categoria
from Clases.classSucursal import Sucursal
from Clases.classAdministrador import AdministradorSucursales
from Clases.classMonitorDTD import MonitorDTD
import os
import time
import xml.etree.ElementTree as ET

class MenuAplicacion:

    def __init__(self, root, administrador):
        self.root=root
        self.administrador=administrador
        self.root.withdraw()
        self.mostrar_splash()
        self.monitor_dtd=MonitorDTD(self.administrador,"src/config/inventario.xml","src/config/inventario.dtd",self.root,10)
        self.monitor_dtd.start()

    def mostrar_splash(self):
        splash=tk.Toplevel(self.root)
        splash.overrideredirect(True)

        imagen=Image.open("src/imagen/oxxo.png")
        imagen=imagen.resize((500, 300))
        img=ImageTk.PhotoImage(imagen)

        label=tk.Label(splash, image=img)
        label.image=img
        label.pack()

        # Barra de carga
        barra=ttk.Progressbar(splash,orient="horizontal",length=300,mode="determinate")
        barra.pack(pady=10)
        
        tk.Label(splash,text="Cargando sistema...",font=("Arial", 10)).pack()

        # Centrar ventana
        ancho=img.width()
        alto=img.height()

        x=(splash.winfo_screenwidth() // 2) - (ancho // 2)
        y=(splash.winfo_screenheight() // 2) - (alto // 2)

        splash.geometry(f"{ancho}x{alto+90}+{x}+{y}")

        def cargar():

            for i in range(101):
                barra["value"]=i
                splash.update()
                time.sleep(0.02)

            ruta_xml="src/config/inventario.xml"
            ruta_dtd="src/config/inventario.dtd"

            valido=self.administrador.validar_xml_dtd(ruta_xml, ruta_dtd)

            if valido:
                self.administrador.cargar_xml()
                self.root.deiconify() #muestra la ventana root oculta
                self.crear_menu()
                
            else:
                messagebox.showerror("Error", "El archivo XML no cumple con el DTD.")
                self.root.destroy()

            splash.destroy()

        cargar() #ejecuta funcion

    
    def crear_menu(self):

        self.root.title("Gestión de Inventario por Sucursal")
        self.root.geometry("500x480")
        self.root.configure(bg="#6C4F7C")

        titulo=tk.Label(self.root,text="Menu Principal",font=("Helvetica", 20, "bold"),bg="#ddd4d4",fg="#0f2b41")
        titulo.pack(pady=30)
        #Botones
        self.crear_boton("➕ Agregar Sucursal", self.ventana_agregar_sucursal)
        self.crear_boton("📦 Agregar Producto a Inventario", self.ventana_agregar_producto)
        self.crear_boton("📄 Mostrar Inventario", self.mostrar_inventario)
        self.crear_boton("❌ Salir", self.salir)

    #funcion para creae botones
    def crear_boton(self, texto,comando):
        boton=tk.Button(self.root,text=texto,command=comando,font=("Arial", 14),bg="#327CA7",fg="black",width=30,height=2,relief="raised",bd=3)
        boton.pack(pady=10)

    # Validaciones

    def validar_datos(self, nombre_producto, precio_producto, existencia_producto):

        if not nombre_producto or not precio_producto or not existencia_producto:
            messagebox.showinfo("❗️Error", "Todos los campos deben ser completados.")
            return False
        # Verficar num precio
        try:
            if float(precio_producto) < 0:
                messagebox.showinfo("❗️Error", "El precio no puede ser negativo.")
                return False

            if int(existencia_producto) < 0:
                messagebox.showinfo("❗️Error", "El stock no puede ser negativo.")
                return False
        except ValueError:
            messagebox.showinfo("❗️Error", "El precio debe ser un número válido.")
            return False
        #verificar num stock
        try:
            int(existencia_producto)
        except ValueError:
            messagebox.showinfo("❗️Error", "El stock debe ser un número válido.")
            return False

        return True


    def validar_nombre_sucursal(self, nombre):
    
        if not nombre:
            messagebox.showinfo("❗️Error", "Debes ingresar un nombre de sucursal")
            return False
        
        #validar que no se ingresen digitos
        if not nombre.replace(" ", "").isalpha():
            messagebox.showinfo("❗️Error", "El nombre solo debe contener letras")
            return False

        return True


    # Sucursales

    def guardar_sucursal(self):
        #asigna entry a nombre sucursal
        #title: convierte texto en Mayuscula la primera
        nombre=self.entrada_sucursal.get().strip().title()

        if not self.validar_nombre_sucursal(nombre):
            return

        # Verificar sucursales duplicadas
        for suc in self.administrador.obtener_sucursales():
            if suc.get_nombre().lower()==nombre.lower():
                messagebox.showinfo("❗️Error", "Esa sucursal ya existe.")
                return
        #asignar entry de sucursal a objeto sucursal
        sucursal=Sucursal(nombre)
        self.administrador.agregar_sucursal(sucursal)

        messagebox.showinfo("Informacion", f"¡Sucursal '{nombre}' agregada correctamente!✅")


    def ventana_agregar_sucursal(self):

        ventana=tk.Toplevel(self.root)
        ventana.title("Agregar Sucursal")
        ventana.geometry("300x200")
        ventana.configure(bg="#419893")
        label=tk.Label(ventana, text="Nombre de la Sucursal:")
        label.pack(pady=10)
        self.entrada_sucursal=tk.Entry(ventana)
        self.entrada_sucursal.pack(pady=5)
        boton_guardar=tk.Button(ventana,text="📩 Guardar",command=self.guardar_sucursal)
        boton_guardar.pack(pady=15)
        

    # Productos
    def agregar_producto(self):
        #entry de nombre y categoria sera tipo oracion (title)
        nombre=self.entrada_producto.get().strip().title()
        precio=self.entrada_precio.get()
        stock=self.entrada_stock.get()
        categoria_nombre=self.entrada_categoria.get().strip().title()
        nombre_sucursal=self.opcion_sucursal.get()

        #verificar que se seleccione una sucursal
        if nombre_sucursal=="Selecciona una sucursal":
            messagebox.showinfo("❗️Error", "Debes seleccionar una sucursal.")
            return

        if not categoria_nombre:
            messagebox.showinfo("❗️Error", "Debes escribir una categoría.")
            return

        if not self.validar_datos(nombre, precio, stock):
            messagebox.showinfo("❗️Error", "Verifica tus datos.")
            return
        
        sucursal_obj=None

        for sucursal in self.administrador.obtener_sucursales():
            if sucursal.get_nombre()==nombre_sucursal:
                sucursal_obj=sucursal
                break

        if sucursal_obj is None:
            messagebox.showinfo("❗️Error", "Sucursal no encontrada.")
            return

        categoria_obj=None

        for categoria in sucursal_obj.categorias:
            if categoria.get_nombre()==categoria_nombre:
                categoria_obj=categoria
                break

        if categoria_obj is None:
            categoria_obj=Categoria(categoria_nombre)
            sucursal_obj.agregar_categoria(categoria_obj)

        # Verificar productos duplicados
        for prod in categoria_obj.productos:
            if prod.get_nombre().lower() == nombre.lower():
                messagebox.showinfo("❗️Error", "Ese producto ya existe.")
                return

        producto = Producto(nombre, precio, stock)
        categoria_obj.agregar_producto(producto)
        messagebox.showinfo("Éxito", "Producto agregado correctamente✅")


    def ventana_agregar_producto(self):

        ventana=tk.Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("400x500")
        ventana.configure(bg="#419893")
        label_sucursal=tk.Label(ventana, text="Seleccione una Sucursal:",font=("Arial",18))
        label_sucursal.pack()
        self.opcion_sucursal=tk.StringVar()
        self.opcion_sucursal.set("Selecciona una sucursal")
        sucursales=self.administrador.obtener_sucursales()
        nombres_sucursales=[]
        for sucursal in sucursales:
            nombre=sucursal.get_nombre()
            if nombre not in nombres_sucursales:
                nombres_sucursales.append(nombre)
        #Lista de opciones
        menu_sucursales = tk.OptionMenu(ventana, self.opcion_sucursal, *nombres_sucursales)
        menu_sucursales.pack(pady=15)

        label_categoria=tk.Label(ventana, text="🛒 Categoría:")
        label_categoria.pack(pady=10)

        self.entrada_categoria=tk.Entry(ventana)
        self.entrada_categoria.pack()

        label_producto=tk.Label(ventana, text="✏️ Nombre del producto:")
        label_producto.pack(pady=10)

        self.entrada_producto=tk.Entry(ventana)
        self.entrada_producto.pack()

        label_precio=tk.Label(ventana, text="💲 Precio:")
        label_precio.pack(pady=10)

        self.entrada_precio=tk.Entry(ventana)
        self.entrada_precio.pack()

        label_stock=tk.Label(ventana, text="📦 Existencia:")
        label_stock.pack(pady=10)

        self.entrada_stock=tk.Entry(ventana)
        self.entrada_stock.pack()

        boton_guardar=tk.Button(ventana,text="📩 Guardar Producto",font=("Arial",16),command=self.agregar_producto)
        boton_guardar.pack(pady=15)


    # Inventario

    def mostrar_inventario(self):

        sucursales=self.administrador.obtener_sucursales()
        if not sucursales:
            messagebox.showinfo("Inventario", "No hay sucursales registradas❌")
            return
        texto= ""

        for sucursal in sucursales:
            texto += f"Inventario de la sucursal: {sucursal.get_nombre()}\n"
            for categoria in sucursal.categorias:
                texto += f"Categoría: {categoria.get_nombre()}\n"
                categoria.productos.sort(key=lambda p: p.get_nombre())
                for producto in categoria.productos:
                    texto += f" - {producto}\n"
            texto += "\n"

        messagebox.showinfo("Inventario Completo", texto)


    # funcion salir
    def salir(self):
        ruta=os.path.join("src", "config")
        archivo=os.path.join(ruta, "inventario.xml")

        if not os.path.exists(ruta):
            os.makedirs(ruta)

        archivo=os.path.join(ruta, "inventario.xml")

        raiz=ET.Element("Sucursales")
        for sucursal in self.administrador.obtener_sucursales():
            sucursal_xml=ET.SubElement(raiz, "Sucursal", {"nombre": sucursal.get_nombre()})

            for categoria in sucursal.get_categorias():
                categoria_xml=ET.SubElement(sucursal_xml, "Categoria", {
                    "nombre": categoria.get_nombre()})

                for producto in categoria.get_productos():
                    ET.SubElement(categoria_xml, "Producto", {
                        "nombre": producto.get_nombre(),
                        "precio": str(producto.get_precio()),
                        "stock": str(producto.get_stock())})

        arbol=ET.ElementTree(raiz)
        ET.indent(arbol, space="    ",level=0)
        arbol.write(archivo, encoding="utf-8", xml_declaration=True)
        print("Archivo 'inventario.xml' guardado exitosamente.")
        if self.monitor_dtd:
            self.monitor_dtd.detener()
        self.root.destroy()