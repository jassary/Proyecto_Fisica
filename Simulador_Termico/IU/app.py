# ui/app.py (fragmento)
from logging import root
from Simulador_Termico.IU.controles import PanelControles
from Simulador_Termico.IU.esquema import Esquema
from Simulador_Termico.config import TEMA

self.esquema = Esquema(root, TEMA)
self.esquema.pack(fill='x', padx=16)

# dentro de _tick(), después de avanzar la simulación:
self.esquema.actualizar(b)      # b es el Balance que devolvió sim.avanzar()

self.controles = PanelControles(
    root, TEMA,
    on_pausar=self.pausar,
    on_reiniciar=self.reiniciar,
    on_exportar=self.exportar,
    on_guia=self.mostrar_guia,
)
self.controles.pack(fill='x', padx=16)

def pausar(self):
    self.activo = not self.activo
    self.controles.set_pausado(not self.activo)

def reiniciar(self):
    self.sim.reiniciar(self.controles.entradas().ambiente)
    self.hist.limpiar()