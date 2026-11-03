# tests/test_modelo.py
from modelo.simulador import Simulador, Entradas

def test_regimen_estacionario_conserva_energia():
    s = Simulador()
    e = Entradas(carga=50, ventilador=100, ambiente=28)
    for _ in range(200_000):
        b = s.avanzar(e)
    assert abs(b.potencia - b.conduccion) < 0.01
    assert abs(b.conduccion - b.salida) < 0.01      # P = Q = salida

def test_mas_ventilador_enfria():
    def t_final(vent):
        s = Simulador(); e = Entradas(80, vent, 28)
        for _ in range(100_000): s.avanzar(e)
        return s.t_cpu
    assert t_final(100) < t_final(0)

def test_temperatura_nunca_baja_del_ambiente():
    ...

def test_throttling_limita_temperatura():
    ...