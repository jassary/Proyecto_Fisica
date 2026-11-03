# app.py
import tkinter as tk
from Simulador_Termico.modelo.simulador import SimuladorTermico
from Simulador_Termico.modelo.parametros import ParametrosTermicos
from Simulador_Termico.IU.grafica import Grafica  

class AplicacionSimulador:
    def __init__(self):
        print("[App] Inicializando componentes del sistema...")
        
        # 1. Creamos la ventana principal de Tkinter
        self.root = tk.Tk()
        self.root.title("Simulador Térmico de CPU")
        self.root.geometry("800x500")
        
        # 2. Objeto simulado ficticio para el "Tema" visual que pide tu Grafica
        # (Ajusta los atributos si tu clase Tema real usa otros nombres)
        class TemaFicticio:
            panel = "#1e1e1e"        # Fondo oscuro para el canvas
            color_cpu = "#ff4d4d"    # Línea roja para CPU
            color_disipador = "#3399ff" # Línea azul para disipador
            color_ambiente = "#2ecc71"  # Línea verde para ambiente
        self.tema = TemaFicticio()

        # 3. Instanciamos los parámetros físicos y el simulador térmico
        self.ajustes = ParametrosTermicos(
            conductividad=0.85, 
            calor_especifico=4184, 
            temperatura_inicial=20.0
        )
        self.simulador = SimuladorTermico(
            parametros=self.ajustes, 
            duracion_segundos=120
        )

        # 4. Acoplamos tu lienzo de Grafica dentro de la interfaz
        self.grafica_visual = Grafica(master=self.root, tema=self.tema)
        self.grafica_visual.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def iniciar(self):
        """Método encargado de arrancar el bucle principal de la interfaz gráfica."""
        print("[App] Ejecutando el flujo principal...")
        self.ajustes.mostrar_configuracion()
        
        # Ejecutamos la lógica física
        self.simulador.ejecutar_simulacion()
        
        # Muestra la ventana en pantalla y congela el script en espera de interacciones del usuario
        self.root.mainloop()
