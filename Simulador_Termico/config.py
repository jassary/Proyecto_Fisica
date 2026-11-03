from dataclasses import dataclass

@dataclass(frozen=True)
class Tema:
    fondo: str = '#FFFFFF'
    panel: str = '#D4D4D4'
    texto: str = '#2B2B2B'
    rejilla: str = '#B3B3B3'
    cpu: str = '#D9534F'
    disipador: str = '#F0AD4E'
    ambiente: str = '#0275D8'
    limite: str = '#8B0000'

TEMA = Tema()
VENTANA_GRAFICA_S = 180      # segundos visibles
PERIODO_TICK_MS = 100
DT_SIMULACION = 0.05