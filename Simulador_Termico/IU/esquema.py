import tkinter as tk
from config import TEMA, Tema  # Importación corregida para evitar fallos de ruta
from modelo.simulador import Balance

class Esquema(tk.Canvas):
    """Diagrama de flujo de calor: CPU -> disipador -> aire."""

    ALTO = 135
    ANCHO_MIN = 800
    MEDIO_ANCHO_CAJA = 130        # mitad del ancho de cada recuadro
    Y_SUP, Y_INF = 22, 105        # bordes superior e inferior de las cajas
    Y_FLECHA = 62
    NOTA = ('El ventilador mueve aire: no produce frío. '
            'El calor fluye espontáneamente hacia zonas de menor temperatura.')

    def __init__(self, master, tema: Tema):
        super().__init__(master, height=self.ALTO, bg=tema.panel,
                         highlightthickness=0)
        self.tema = tema
        self._ultimo: Balance | None = None
        self._ids: dict[str, int] = {}
        self.bind('<Configure>', self._al_redimensionar)
        self._construir()

    # ---------- construcción (solo al crear o redimensionar) ----------
    def _construir(self) -> None:
        self.delete('all')
        self._ids.clear()
        w = max(self.winfo_width(), self.ANCHO_MIN)
        t, m = self.tema, self.MEDIO_ANCHO_CAJA

        cajas = (
            ('cpu', 0.17, 'PROCESADOR', t.cpu),
            ('disipador', 0.50, 'DISIPADOR', t.disipador),
            ('aire', 0.83, 'AIRE AMBIENTE', t.ambiente),
        )
        for clave, frac, titulo, color in cajas:
            x = w * frac
            # Crear los rectángulos contenedores de los componentes térmicos
            self.create_rectangle(x - m, self.Y_SUP, x + m, self.Y_INF, 
                                  fill=color, outline=t.texto, width=1)
            # Título superior del componente
            self.create_text(x, self.Y_SUP + 15, text=titulo, 
                             fill=t.texto, font=('Arial', 9, 'bold'))
            # Espacio reservado para inyectar los valores dinámicos de temperatura
            self._ids[f't_{clave}'] = self.create_text(
                x, self.Y_SUP + 45, text="--.- °C", 
                fill=t.texto, font=('Arial', 16, 'bold')
            )

        # SOLUCIÓN: Si 'texto_secundario' no existe en tu configuración, usa un color alternativo seguro
        color_nota = getattr(t, 'texto_secundario', '#777777')

        # Dibujar nota explicativa al pie del diagrama
        self.create_text(w // 2, self.ALTO - 12, text=self.NOTA, 
                         fill=color_nota, font=('Arial', 8, 'italic'))

    def _al_redimensionar(self, evento) -> None:
        """Manejador del evento <Configure> para actualizar el tamaño dinámico."""
        self._construir()
        # Si ya había datos cargados antes de cambiar el tamaño, los vuelve a pintar
        if self._ultimo:
            self.actualizar(self._ultimo)

    def actualizar(self, balance: Balance) -> None:
        """Actualiza los textos térmicos en base al último balance del simulador."""
        self._ultimo = balance
        if f't_cpu' in self._ids:
            # Modifica los textos dinámicos guardados en el diccionario de IDs
            self.itemconfig(self._ids['t_cpu'], text=f"{balance.t_cpu:.1f} °C")
            self.itemconfig(self._ids['t_disipador'], text=f"{balance.t_disipador:.1f} °C")
            self.itemconfig(self._ids['t_aire'], text=f"{balance.t_ambiente:.1f} °C")
