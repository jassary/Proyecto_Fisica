import os
import sys
import tkinter as tk

# Truco de entorno: Añade la carpeta actual al buscador de Python para evitar errores de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from IU.app import AplicacionSimulador

def main():
    root_window = tk.Tk()
    root_window.geometry("800x600")
    
    # Arranca la aplicación pasando la ventana verdadera de Tkinter
    app = AplicacionSimulador(master=root_window)
    
    # Inicia el bucle de actualización física e interfaz
    root_window.after(30, app._tick)
    root_window.mainloop()

if __name__ == "__main__":
    main()
