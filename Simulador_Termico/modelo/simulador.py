# modelo/simulador.py
from dataclasses import dataclass
from .parametros import Parametros

@dataclass
class Entradas:
    carga: float        # %
    ventilador: float   # %
    ambiente: float     # °C

@dataclass
class Balance:
    potencia: float     # W generados en la CPU
    conduccion: float   # W de CPU a disipador
    salida: float       # W de disipador a aire
    throttling: bool

class Simulador:
    def __init__(self, params: Parametros | None = None, t_inicial: float = 28.0):
        self.p = params or Parametros()
        self.reiniciar(t_inicial)

    def reiniciar(self, t_inicial: float) -> None:
        self.t_cpu = self.t_disipador = t_inicial
        self.tiempo = 0.0
        self.throttling = False

    def _potencia(self, e: Entradas) -> float:
        # Histéresis: se activa en t_max y se desactiva t_histeresis grados antes
        if self.t_cpu >= self.p.t_max:
            self.throttling = True
        elif self.t_cpu <= self.p.t_max - self.p.t_histeresis:
            self.throttling = False
        base = self.p.p_reposo + self.p.p_carga * e.carga
        return base * (self.p.factor_throttling if self.throttling else 1.0)

    def balance(self, e: Entradas) -> Balance:
        """Única fuente de verdad para P, Q y salida: la UI solo lee esto."""
        h = self.p.h_natural + self.p.h_forzada * e.ventilador
        return Balance(
            potencia=self._potencia(e),
            conduccion=self.p.g_conduccion * (self.t_cpu - self.t_disipador),
            salida=h * (self.t_disipador - e.ambiente),
            throttling=self.throttling,
        )

    def avanzar(self, e: Entradas, dt: float = 0.05) -> Balance:
        b = self.balance(e)
        self.t_cpu += dt * (b.potencia - b.conduccion) / self.p.c_cpu
        self.t_disipador += dt * (b.conduccion - b.salida) / self.p.c_disipador
        self.tiempo += dt
        return b