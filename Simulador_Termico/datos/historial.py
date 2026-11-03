from collections import deque
import csv

class Historial:
    ENCABEZADO = ['tiempo_s', 'cpu_C', 'disipador_C', 'ambiente_C',
                  'carga_%', 'ventilador_%', 'potencia_W', 'throttling']

    def __init__(self, ventana_puntos: int = 1800, max_exportar: int = 100_000):
        self.ventana = deque(maxlen=ventana_puntos)   # lo que se grafica: O(1)
        self.completo = deque(maxlen=max_exportar)    # lo que se exporta, con tope

    def agregar(self, fila: tuple) -> None:
        self.ventana.append(fila)
        self.completo.append(fila)

    def limpiar(self) -> None:
        self.ventana.clear(); self.completo.clear()

    def exportar_csv(self, ruta: str) -> None:
        with open(ruta, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(self.ENCABEZADO)
            w.writerows(self.completo)