import tkinter as tk
from Clases.classMenu import MenuAplicacion
from Clases.classAdministrador import AdministradorSucursales

if __name__ == "__main__":

    admin=AdministradorSucursales()
    ventana=tk.Tk()
    
    app=MenuAplicacion(ventana, admin)

    ventana.mainloop()