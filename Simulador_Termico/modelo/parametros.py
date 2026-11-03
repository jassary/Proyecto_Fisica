# modelo/parametros.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Parametros:
    c_cpu: float = 12.0            # capacidad térmica CPU [J/°C]
    c_disipador: float = 60.0      # capacidad térmica disipador [J/°C]
    g_conduccion: float = 4.0      # conductancia CPU→disipador [W/°C]  (R = 0,25 °C/W)
    h_natural: float = 0.4         # intercambio con ventilador al 0 % [W/°C]
    h_forzada: float = 0.026       # incremento por cada 1 % de ventilador [W/°C/%]
    p_reposo: float = 10.0         # potencia en reposo [W]
    p_carga: float = 0.9           # potencia adicional por 1 % de carga [W/%]
    t_max: float = 95.0            # umbral de throttling [°C]
    t_histeresis: float = 5.0      # evita oscilaciones al activar/desactivar
    factor_throttling: float = 0.5 # fracción de potencia que queda al limitar