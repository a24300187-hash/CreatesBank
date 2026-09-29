import threading
import os
from tkinter import messagebox

class MonitorDTD(threading.Thread):

    def __init__(self, administrador, ruta_xml, ruta_dtd, ventana, tiempo_espera=10):
        super().__init__()

        self.administrador = administrador
        self.ruta_xml = ruta_xml
        self.ruta_dtd = ruta_dtd
        self.ventana = ventana
        self.tiempo_espera=tiempo_espera

        self._detener_hilo=threading.Event()
        
        # Guardamos la fecha de modificación inicial al arrancar
        if os.path.exists(self.ruta_xml):
            self.ultima_modificacion=os.path.getmtime(self.ruta_xml)
        else:
            self.ultima_modificacion=0

    def run(self):
        # Este mensaje solo sale UNA vez al iniciar el programa
        print(f"\n[MONITOR] Iniciando cada {self.tiempo_espera} segundos.")
        
        while not self._detener_hilo.is_set():
            # 1. Avisamos ruidosamente en la terminal que iniciamos el ciclo
            print("\n[MONITOR] 🕒 Pasaron 10 segundos. Validando XML...")
            try:

            # Si el usuario cerró el programa mientras validábamos, salimos limpiamente
                if not self.ventana.winfo_exists():
                    break
                valido = self.administrador.validar_xml_dtd(self.ruta_xml, self.ruta_dtd)
                if not valido:
                    print("[MONITOR] ❌ ALERTA: ¡La validación falló! El XML no cumple con el DTD.")
                    self.ventana.after(0, lambda: messagebox.showerror("Error", "El XML no cumple con el DTD"))
                    self.ventana.after(100, self.ventana.destroy)
                    break
                else:
                    # Si es válido, recargamos la RAM y lo festejamos en la terminal
                    self.administrador.cargar_xml()
                    print("[MONITOR] ✅ ÉXITO: Archivo perfectamente estructurado. Datos actualizados en memoria.")
                
                    # 2. Ahora revisamos si esa validación exitosa trajo cambios nuevos
                    modificacion_actual = os.path.getmtime(self.ruta_xml)
                
                    if modificacion_actual != self.ultima_modificacion:
                        # Avisamos en la terminal que encontramos cambios
                        print("[MONITOR] 🔔 ¡DETECTADO! Hubo una edición externa en el archivo XML.")
                    
                        # Actualizamos la estampa para no repetir el messagebox en el próximo ciclo de 10s
                        self.ultima_modificacion = modificacion_actual
                    
                        # Mandamos el messagebox a la pantalla
                        if self.ventana.winfo_exists():
                            self.ventana.after(0, lambda: messagebox.showinfo(
                                "Aviso de Actualización", 
                                "🔄 Se han detectado cambios externos en el archivo XML.\n\n"
                                "Los datos se actualizaron en el sistema. Por favor, vuelva a abrir o refrescar la ventana de inventario para ver los cambios reflejados."
                            ))
                    else:
                        # Si todo está bien pero nadie editó nada, también lo dejamos claro en la terminal
                        print("[MONITOR] ℹ️ Sin cambios externos detectados en este ciclo...")
            except (RuntimeError, Exception):
            # Si Tkinter se destruyó en medio de la ejecución, este bloque atrapa el pánico,
            # rompe el ciclo 'while' limpiamente y evita que salga la molesta excepción en la terminal.
                break

            # Espera estrictamente los 10 segundos congelado antes de volver a imprimir
            self._detener_hilo.wait(self.tiempo_espera)
            
        print("[MONITOR] Hilo detenido.")
        
    def detener(self):
        self._detener_hilo.set()