from .classSucursal import Sucursal
from .classCategoria import Categoria
from .classProducto import Producto
import xml.etree.ElementTree as ET
from lxml import etree
import os

class AdministradorSucursales:

    def __init__(self):
        self.sucursales=[]

    def agregar_sucursal(self, sucursal):
        self.sucursales.append(sucursal)

    def obtener_sucursales(self):
        return self.sucursales

    def cargar_xml(self):
        self.sucursales=[]
        ruta=os.path.join("src", "config", "inventario.xml")

        if not os.path.exists(ruta):
            print(f"DEBUG: No se encontró el archivo en {os.path.abspath(ruta)}")
            return

        arbol=ET.parse(ruta)
        raiz=arbol.getroot()

        for sucursal_xml in raiz.findall("Sucursal"):
            sucursal=Sucursal(sucursal_xml.get("nombre"))

            for categoria_xml in sucursal_xml.findall("Categoria"):
                categoria=Categoria(categoria_xml.get("nombre"))

                for producto_xml in categoria_xml.findall("Producto"):
                    producto=Producto(producto_xml.get("nombre"),float(producto_xml.get("precio")),int(producto_xml.get("stock")))
                    categoria.agregar_producto(producto)

                sucursal.agregar_categoria(categoria)

            self.agregar_sucursal(sucursal)
    
    def validar_xml_dtd(self, nombre_archivo_xml: str, nombre_archivo_dtd: str) -> bool:
        try:
            #1 cargar dtd
            dtd=etree.DTD(nombre_archivo_dtd)

            #2 crear un parser estandar sin argumentos dtd
            parser=etree.XMLParser()

            #3 Parser el XML
            tree=etree.parse(nombre_archivo_xml,parser)

            #4 validar el arbol parseado contra el Dtd cargado
            if dtd.validate(tree):
                print(f"¡El archivo '{nombre_archivo_xml}' es valido estructuralmente!")
                return True
            else:
                print(f"El archivo XML NO es valido. Errores de validacion")
                #mostrar los errores especificos del dtd
                for error in dtd.error_log:
                    print(f" -Linea {error.line}, Columna {error.column}: {error.message}")
                    return False
                    
        except etree.DTDParseError as e:
            print(f"Error al parsear DTD (Revisa la sintaxis): {e}")
            return False
        
        except etree.XMLSyntaxError as e:
            #captura erroes de sintaxis basicos en el XML
            print(f"Error de Sintaxis XML: {e}")
            return False
        
        except FileNotFoundError:
            print(f"Error uno de los archivos no fue encontrado")
            return False
        
        except Exception as e:
            print(f"Ocurrio un error inesperado durante la validacion: {e}")
            return False
    