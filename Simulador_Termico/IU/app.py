import tkinter as tk
# Se eliminó "from logging import root" que causaba el bug del RootLogger
from IU.controles import PanelControles
from IU.esquema import Esquema
from config import TEMA
from modelo.simulador import Simulador  # Asegura la ruta interna correcta
from datos.historial import Historial

class AplicacionSimulador(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Simulador Térmico - Ley de Enfriamiento")
        self.pack(fill='both', expand=True)
        
        self.activo = False
        
        # Corrección: Pasamos 'self' (el Frame de Tkinter) como contenedor, NO el root de logging
        self.esquema = Esquema(self, TEMA)
        self.esquema.pack(fill='x', padx=16, pady=8)
        
        self.controles = PanelControles(
            self, TEMA,
            on_pausar=self.pausar,
            on_reiniciar=self.reiniciar,
            on_exportar=self.exportar,
            on_guia=self.mostrar_guia,
        )
        self.controles.pack(fill='x', padx=16, pady=8)
        
        # Inicialización de dependencias físicas y persistencia
        self.sim = Simulador()
        self.hist = Historial()

    def _tick(self):
        if self.activo:
            # Avanzar la simulación física
            entradas = self.controles.entradas()
            b = self.sim.avanzar(entradas.k, entradas.ambiente, entradas.paso)
            
            # Actualizar la interfaz y la gráfica con el balance devuelto
            self.esquema.actualizar(b)
            self.hist.registrar(b)
            
        # Bucle de animación en tiempo real (cada 30ms aprox)
        self.master.after(30, self._tick)

    def pausar(self):
        self.activo = not self.activo
        self.controles.set_pausado(not self.activo)

    def reiniciar(self):
        entradas = self.controles.entradas()
        self.sim.reiniciar(entradas.inicial, entradas.ambiente)
        self.hist.limpiar()
        self.esquema.reiniciar_grafica()

    def exportar(self):
        self.hist.guardar_a_csv()

    def mostrar_guia(self):
        # Lógica para desplegar una ventana de ayuda con la Ley de Newton
        pass
