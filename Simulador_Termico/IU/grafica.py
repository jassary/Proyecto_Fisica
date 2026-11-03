import tkinter as tk

class Grafica(tk.Canvas):
    def __init__(self, master, tema):
        # 1. Inicializamos el Canvas heredado usando super()
        super().__init__(master, bg=tema.panel, highlightthickness=0)
        self.tema = tema
        self._ymax = None
        
        # 2. Inicializamos el diccionario de líneas creando los identificadores del Canvas
        # Creamos las líneas inicialmente vacías (coordenadas 0,0,0,0) para que existan en el Canvas
        self._lineas = {
            'cpu': self.create_line(0, 0, 0, 0, fill=getattr(tema, 'color_cpu', 'red'), width=2),
            'disipador': self.create_line(0, 0, 0, 0, fill=getattr(tema, 'color_disipador', 'blue'), width=2),
            'ambiente': self.create_line(0, 0, 0, 0, fill=getattr(tema, 'color_ambiente', 'green'), width=2)
        }
        
        # 3. Vinculamos el evento de redimensión
        self.bind('<Configure>', lambda e: self._ymax_forzar())

    def _ymax_forzar(self):
        """Fuerza el redibujado de los ejes cuando la ventana cambia de tamaño."""
        if self._ymax is not None:
            self._dibujar_ejes(self._ymax)

    def _calcular_ymax(self, filas):
        """Calcula el valor máximo de temperatura para escalar el gráfico."""
        # Si no hay datos, devolvemos un valor base por defecto (ej. 100 grados)
        if not filas:
            return 100
        # Busca el valor máximo considerando los índices 1, 2 y 3 de tus filas de datos
        max_val = max(max(fila[1], fila[2], fila[3]) for fila in filas)
        return max(max_val, 40) # Asegura un mínimo de escala para que no se vea vacío

    def _dibujar_ejes(self, ymax):
        """Dibuja las líneas de fondo o cuadrícula según la escala actual."""
        self._ymax = ymax
        self.delete('eje') # Borra los ejes anteriores para no encimarlos
        # Aquí puedes añadir líneas de cuadrícula usando self.create_line(..., tags='eje')
        pass

    def _a_pixeles(self, filas, idx, ymax):
        """Transforma los datos físicos de temperatura a coordenadas de píxeles del Canvas."""
        ancho = self.winfo_width()
        alto = self.winfo_height()
        if len(filas) < 2:
            return [0, alto, ancho, alto]

        puntos = []
        for i, fila in enumerate(filas):
            # Coordenada X distribuida proporcionalmente a lo largo del Canvas
            x = (i / (len(filas) - 1)) * ancho
            # Coordenada Y invertida (Tkinter tiene el origen 0,0 arriba a la izquierda)
            y = alto - (fila[idx] / ymax) * alto
            puntos.extend([x, y])
        return puntos

    def actualizar(self, filas):
        """Actualiza las posiciones de las curvas térmicas en pantalla."""
        if not filas:
            return
            
        ymax = self._calcular_ymax(filas)
        if ymax != self._ymax:           # Redibuja ejes SOLO si cambió la escala
            self._dibujar_ejes(ymax)
            
        for idx, nombre in [(1, 'cpu'), (2, 'disipador'), (3, 'ambiente')]:
            puntos = self._a_pixeles(filas, idx, ymax)
            if len(puntos) >= 4: # El Canvas requiere al menos 2 puntos (x1, y1, x2, y2) para mover una línea
                self.coords(self._lineas[nombre], *puntos)   # Solo mueve la línea existente
