"""Interfaz gráfica (Tkinter, viene con Python: no hay que instalar nada).

Estilo: fondo negro con grilla, títulos neón, tarjetas oscuras con brillo y etiquetas de colores.
Todo se dibuja sobre un único Canvas que se redibuja completo en cada evento, así el diseño
no depende de los widgets de Windows.

No tiene lógica de simulación: usa el motor (M6) y las estadísticas (M7) igual que main.py.
"""
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from simulador.carga import ErrorCarga, cargar_archivo, validar_procesos
from simulador.config import MAX_PROCESOS, MEMORIA_SO, MEMORIA_USUARIO
from simulador.estadisticas import calcular_estadisticas
from simulador.motor import Eventos, Simulador
from simulador.planificador import Gantt
from simulador.proceso import Proceso

# ---------- paleta ----------
FONDO = '#050608'
GRILLA = '#11141a'
TARJETA = '#0c0e13'
BORDE = '#22262f'
TEXTO = '#e8eaf0'
TENUE = '#7d8494'
NEON = '#2ee6c8'          # turquesa del título
LILA = '#8b7cff'
NARANJA = '#ff8a3d'
VERDE = '#3ddc97'
ROJO = '#ff5f6d'
COLORES_PROCESO = ['#2ee6c8', '#8b7cff', '#ff8a3d', '#ff5fa2', '#4aa8ff',
                   '#ffd166', '#3ddc97', '#ff6b6b', '#b6f35b', '#5ce1ff']

TITULO = ('Segoe UI', 26, 'bold')
SUBTITULO = ('Segoe UI Semibold', 12)
NORMAL = ('Segoe UI', 11)
MONO = ('Consolas', 11)
MONO_CHICO = ('Consolas', 9)
GRANDE = ('Segoe UI', 30, 'bold')


def color_de(pid: int) -> str:
    return COLORES_PROCESO[(pid - 1) % len(COLORES_PROCESO)]


def mezclar(c1: str, c2: str, a: float) -> str:
    """Mezcla dos colores hex: a=0 -> c1, a=1 -> c2. Sirve para simular transparencia y brillo."""
    r1, g1, b1 = (int(c1[i:i + 2], 16) for i in (1, 3, 5))
    r2, g2, b2 = (int(c2[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % (round(r1 + (r2 - r1) * a), round(g1 + (g2 - g1) * a), round(b1 + (b2 - b1) * a))


def carpeta_app() -> Path:
    """Carpeta del programa: junto al .exe si está empaquetado, o la raíz del proyecto."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


class Lienzo(tk.Canvas):
    """Canvas con primitivas del estilo: rectángulos redondeados, brillo, píldoras, botones."""

    def rect_redondeado(self, x1, y1, x2, y2, r=12, **kw):
        r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
        puntos = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
                  x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(puntos, smooth=True, **kw)

    def brillo(self, x1, y1, x2, y2, color, r=12, capas=6, intensidad=0.35):
        """Halo alrededor de un rectángulo: varios contornos que se van apagando hacia el fondo."""
        for i in range(capas, 0, -1):
            a = 1 - intensidad * (1 - i / (capas + 1)) ** 2
            self.rect_redondeado(x1 - i * 2, y1 - i * 2, x2 + i * 2, y2 + i * 2, r + i * 2,
                                 fill='', outline=mezclar(color, FONDO, a), width=2)

    def tarjeta(self, x1, y1, x2, y2, titulo='', acento=LILA, brilla=False):
        if brilla:
            self.brillo(x1, y1, x2, y2, acento)
        self.rect_redondeado(x1 + 3, y1 + 5, x2 + 3, y2 + 5, fill='#020203', outline='')   # sombra
        self.rect_redondeado(x1, y1, x2, y2, fill=TARJETA,
                             outline=mezclar(acento, BORDE, 0.55 if brilla else 0.8), width=1)
        if titulo:
            self.create_oval(x1 + 16, y1 + 17, x1 + 22, y1 + 23, fill=acento, outline='')
            self.create_text(x1 + 30, y1 + 20, text=titulo.upper(), anchor='w', fill=acento, font=MONO_CHICO)

    def texto_neon(self, x, y, texto, color=NEON, font=TITULO, anchor='nw'):
        for d, a in ((3, 0.85), (2, 0.75), (1, 0.6)):
            for dx, dy in ((-d, 0), (d, 0), (0, -d), (0, d)):
                self.create_text(x + dx, y + dy, text=texto, fill=mezclar(color, FONDO, a), font=font, anchor=anchor)
        self.create_text(x, y, text=texto, fill=color, font=font, anchor=anchor)

    def pildora(self, x, y, texto, color, font=MONO_CHICO, relleno=0.88) -> int:
        """Etiqueta con borde de color (como los badges del video). Devuelve el ancho."""
        ancho = len(texto) * 7 + 18
        self.rect_redondeado(x, y, x + ancho, y + 22, r=11, fill=mezclar(color, TARJETA, relleno), outline=color)
        self.create_text(x + ancho / 2, y + 11, text=texto, fill=color, font=font)
        return ancho

    def boton(self, x, y, texto, accion, color=NEON, habilitado=True, ancho=None):
        ancho = ancho or len(texto) * 9 + 36
        # Tk separa los tags por espacios: "Abrir CSV" serían dos tags y el clic no se conectaría
        tag = 'boton-' + ''.join(ch for ch in texto if ch.isalnum())
        borde = color if habilitado else BORDE
        if habilitado:
            self.brillo(x, y, x + ancho, y + 38, color, r=19, capas=4, intensidad=0.25)
        self.rect_redondeado(x, y, x + ancho, y + 38, r=19, fill=mezclar(borde, TARJETA, 0.85),
                             outline=borde, width=1, tags=tag)
        self.create_text(x + ancho / 2, y + 19, text=texto, fill=color if habilitado else TENUE,
                         font=SUBTITULO, tags=tag)
        if habilitado:
            self.tag_bind(tag, '<Button-1>', lambda _e: accion())
            self.tag_bind(tag, '<Enter>', lambda _e: self.config(cursor='hand2'))
            self.tag_bind(tag, '<Leave>', lambda _e: self.config(cursor=''))
        return ancho


class App:
    def __init__(self, raiz: tk.Tk, ruta_inicial: str | None = None):
        self.raiz = raiz
        raiz.title('Simulador de Memoria y Procesos — MVT · Best-Fit · SRTF')
        raiz.configure(bg=FONDO)
        raiz.geometry('1280x820')
        raiz.minsize(1180, 780)
        self.lienzo = Lienzo(raiz, bg=FONDO, highlightthickness=0)
        self.lienzo.pack(fill='both', expand=True)
        self.lienzo.bind('<Configure>', lambda _e: self.dibujar())
        raiz.bind('<Return>', lambda _e: self.siguiente())
        raiz.bind('<space>', lambda _e: self.siguiente())

        self.procesos = []
        self.sim = None
        self.inst = None
        self.estadisticas = None
        self.nombre_carga = ''

        ejemplo = carpeta_app() / 'datos' / 'procesos-ejemplo.csv'
        if ruta_inicial:
            self.abrir(ruta_inicial)
        elif ejemplo.exists():
            self.abrir(str(ejemplo))

    # ---------- acciones ----------
    def abrir(self, ruta: str | None = None):
        if ruta is None:
            ruta = filedialog.askopenfilename(title='Abrir procesos', initialdir=carpeta_app() / 'datos',
                                              filetypes=[('Archivos CSV', '*.csv'), ('Todos', '*.*')])
            if not ruta:
                return
        try:
            self.iniciar(cargar_archivo(ruta), Path(ruta).name)
        except (ErrorCarga, OSError) as e:
            messagebox.showerror('No se pudo cargar el archivo', str(e))

    def iniciar(self, procesos, nombre):
        self.procesos = procesos
        self.nombre_carga = nombre
        self.sim = Simulador(procesos)
        self.estadisticas = None
        self.inst = None
        self.siguiente()

    def reiniciar(self):
        if self.procesos:
            for p in self.procesos:
                p.__init__(p.id, p.tamano, p.arribo, p.irrupcion)
            self.iniciar(self.procesos, self.nombre_carga)

    def siguiente(self):
        """Avanza hasta el próximo evento (arribo o terminación) y se frena, como pide la consigna."""
        if self.sim is None or self.estadisticas is not None:
            return
        while not self.sim.finalizada:
            inst, hay_evento = self.sim.paso()
            if hay_evento:
                self.inst = inst
                break
        else:
            self.inst = self.sim.instantanea(Eventos(terminados=self.sim.terminados_en_este_instante))
            self.estadisticas = calcular_estadisticas(self.procesos, self.sim.t)
        self.dibujar()

    def carga_manual(self):
        DialogoCarga(self.raiz, lambda procesos: self.iniciar(procesos, 'carga manual'))

    # ---------- dibujo ----------
    def dibujar(self):
        c = self.lienzo
        c.delete('all')
        W, H = c.winfo_width(), c.winfo_height()
        if W < 50:
            return
        for x in range(0, W, 48):
            c.create_line(x, 0, x, H, fill=GRILLA)
        for y in range(0, H, 48):
            c.create_line(0, y, W, y, fill=GRILLA)

        c.texto_neon(32, 22, 'SIMULADOR · MVT + SRTF')
        c.create_text(34, 72, text=f'BEST-FIT · 450K USUARIO · MULTIPROGRAMACIÓN 5'
                                   + (f'   ·   {self.nombre_carga}' if self.nombre_carga else ''),
                      anchor='nw', fill=TENUE, font=MONO_CHICO)

        if self.inst is None:
            c.tarjeta(32, 110, W - 32, H - 100, 'sin datos', LILA)
            c.create_text(W / 2, H / 2 - 40, text='Abrí un archivo CSV o cargá los procesos a mano',
                          fill=TEXTO, font=SUBTITULO)
        else:
            self.dibujar_simulacion(W, H)
        self.dibujar_botones(W, H)

    def dibujar_simulacion(self, W, H):
        c, inst = self.lienzo, self.inst
        izq_ancho = 520
        x_der = 32 + izq_ancho + 20

        # reloj + eventos
        c.tarjeta(32, 110, 32 + izq_ancho, 250, 'instante', NEON, brilla=True)
        c.texto_neon(52, 138, f't = {inst.t}', NEON, GRANDE)
        x = 52
        ev = inst.eventos
        for pid in ev.arribos:
            x += c.pildora(x, 210, f'ARRIBO P{pid}', VERDE) + 8
        for pid in ev.terminados:
            x += c.pildora(x, 210, f'TERMINÓ P{pid}', LILA) + 8
        if ev.desalojado is not None:
            x += c.pildora(x, 210, f'P{ev.desalojado} DESALOJADO', NARANJA) + 8
        if self.estadisticas:
            c.pildora(x, 210, 'FIN DE LA SIMULACIÓN', NEON)

        # CPU
        cx = 300
        if inst.cpu:
            col = color_de(inst.cpu['id'])
            c.brillo(cx, 140, cx + 230, 196, col, capas=5)
            c.rect_redondeado(cx, 140, cx + 230, 196, fill=mezclar(col, TARJETA, 0.85), outline=col)
            c.create_text(cx + 18, 168, text=f"CPU  ▸  P{inst.cpu['id']}", anchor='w', fill=col, font=SUBTITULO)
            c.create_text(cx + 212, 168, text=f"rest {inst.cpu['restante']}", anchor='e', fill=TEXTO, font=MONO)
        else:
            c.rect_redondeado(cx, 140, cx + 230, 196, fill=TARJETA, outline=BORDE)
            c.create_text(cx + 115, 168, text='CPU  ·  ociosa', fill=TENUE, font=SUBTITULO)

        # memoria
        self.dibujar_memoria(32, 266, 32 + izq_ancho, H - 250)

        # colas o informe
        if self.estadisticas:
            self.dibujar_informe(x_der, 110, W - 32, H - 250)
        else:
            self.dibujar_colas(x_der, 110, W - 32, H - 250)

        # gantt
        self.dibujar_gantt(32, H - 234, W - 32, H - 100)

    def dibujar_memoria(self, x1, y1, x2, y2):
        c, inst = self.lienzo, self.inst
        c.tarjeta(x1, y1, x2, y2, 'memoria · particiones', LILA)
        libre = sum(p['tamano'] for p in inst.particiones if p['proceso_id'] is None)
        c.create_text(x2 - 18, y1 + 20, text=f'libre {libre}K', anchor='e', fill=TENUE, font=MONO_CHICO)

        # barra de memoria 0..550K
        bx1, bx2, by = x1 + 20, x2 - 20, y1 + 44
        total = MEMORIA_SO + MEMORIA_USUARIO
        escala = (bx2 - bx1) / total
        so_fin = bx1 + MEMORIA_SO * escala
        c.rect_redondeado(bx1, by, so_fin - 2, by + 46, r=6, fill='#1a1d24', outline=BORDE)
        c.create_text((bx1 + so_fin) / 2, by + 23, text='SO', fill=TENUE, font=MONO_CHICO)
        for p in inst.particiones:
            px1 = bx1 + p['inicio'] * escala
            px2 = bx1 + (p['inicio'] + p['tamano']) * escala - 2
            if p['proceso_id'] is None:
                c.rect_redondeado(px1, by, px2, by + 46, r=6, fill=TARJETA, outline=BORDE, dash=(3, 3))
                etiqueta, col = f"{p['tamano']}K", TENUE
            else:
                col = color_de(p['proceso_id'])
                c.rect_redondeado(px1, by, px2, by + 46, r=6, fill=mezclar(col, TARJETA, 0.7), outline=col)
                etiqueta = f"P{p['proceso_id']}"
            if px2 - px1 > 26:
                c.create_text((px1 + px2) / 2, by + 23, text=etiqueta, fill=col if p['proceso_id'] else TENUE,
                              font=MONO_CHICO)
        for k in (0, 100, 200, 300, 400, 550):
            c.create_text(bx1 + k * escala, by + 58, text=str(k), fill=TENUE, font=MONO_CHICO)

        # tabla de particiones
        ty = by + 84
        columnas = [('ID', 0), ('INICIO', 60), ('TAMAÑO', 150), ('PROCESO', 250), ('FRAG. INT.', 360)]
        for nombre, dx in columnas:
            c.create_text(x1 + 24 + dx, ty, text=nombre, anchor='w', fill=TENUE, font=MONO_CHICO)
        c.create_line(x1 + 20, ty + 12, x2 - 20, ty + 12, fill=BORDE)
        filas = [('SO', 0, MEMORIA_SO, 'reservado', '-', TENUE)]
        for p in inst.particiones:
            ocupada = p['proceso_id'] is not None
            filas.append((p['id'], p['inicio'], f"{p['tamano']}K", f"P{p['proceso_id']}" if ocupada else 'libre',
                          p['frag_interna'] if ocupada else '-', color_de(p['proceso_id']) if ocupada else TENUE))
        for i, (*valores, col) in enumerate(filas):
            y = ty + 30 + i * 24
            if y > y2 - 14:
                break
            for (_, dx), v in zip(columnas, valores):
                c.create_text(x1 + 24 + dx, y, text=str(v), anchor='w',
                              fill=col if dx == 250 else TEXTO, font=MONO)

    def dibujar_colas(self, x1, y1, x2, y2):
        c, inst = self.lienzo, self.inst
        c.tarjeta(x1, y1, x2, y2, 'colas de procesos', NARANJA)
        filas = [
            ('LISTOS', 'ordenados por SRTF', inst.listos, VERDE),
            ('LISTOS / SUSPENDIDOS', 'sin memoria, esperan un hueco', inst.suspendidos, NARANJA),
            ('NUEVOS', 'llegaron, esperan cupo (máx. 5)', inst.nuevos, LILA),
        ]
        alto = (y2 - y1 - 120) / 3
        for i, (nombre, ayuda, lista, col) in enumerate(filas):
            y = y1 + 46 + i * alto
            c.create_text(x1 + 24, y, text=nombre, anchor='w', fill=col, font=SUBTITULO)
            c.create_text(x2 - 24, y, text=ayuda, anchor='e', fill=TENUE, font=MONO_CHICO)
            x = x1 + 24
            if not lista:
                c.create_text(x, y + 34, text='— vacía —', anchor='w', fill=TENUE, font=MONO)
            for p in lista:
                if x + 120 > x2 - 20:
                    break
                pc = color_de(p['id'])
                c.rect_redondeado(x, y + 16, x + 112, y + 58, r=10, fill=mezclar(pc, TARJETA, 0.86), outline=pc)
                c.create_text(x + 12, y + 30, text=f"P{p['id']}", anchor='w', fill=pc, font=SUBTITULO)
                c.create_text(x + 100, y + 30, text=f"{p['tamano']}K", anchor='e', fill=TEXTO, font=MONO_CHICO)
                c.create_text(x + 12, y + 47, text=f"restante {p['restante']}", anchor='w', fill=TENUE, font=MONO_CHICO)
                x += 122

        # terminados
        y = y2 - 52
        c.create_line(x1 + 20, y - 14, x2 - 20, y - 14, fill=BORDE)
        c.create_text(x1 + 24, y + 11, text='TERMINADOS', anchor='w', fill=TENUE, font=MONO_CHICO)
        x = x1 + 120
        for pid in inst.terminados:
            x += c.pildora(x, y, f'P{pid}', color_de(pid)) + 6
        if not inst.terminados:
            c.create_text(x, y + 11, text='ninguno todavía', anchor='w', fill=TENUE, font=MONO_CHICO)

    def dibujar_informe(self, x1, y1, x2, y2):
        c, est = self.lienzo, self.estadisticas
        c.tarjeta(x1, y1, x2, y2, 'informe final', VERDE, brilla=True)
        columnas = [('PROCESO', 0), ('ARRIBO', 110), ('IRRUPCIÓN', 210), ('FIN', 330), ('TR', 420), ('TE', 500)]
        ty = y1 + 54
        for nombre, dx in columnas:
            c.create_text(x1 + 28 + dx, ty, text=nombre, anchor='w', fill=TENUE, font=MONO_CHICO)
        c.create_line(x1 + 20, ty + 12, x2 - 20, ty + 12, fill=BORDE)
        for i, f in enumerate(est.por_proceso):
            y = ty + 32 + i * 24
            valores = [f"P{f['id']}", f['arribo'], f['irrupcion'], f['fin'], f['tr'], f['te']]
            for (_, dx), v in zip(columnas, valores):
                c.create_text(x1 + 28 + dx, y, text=str(v), anchor='w',
                              fill=color_de(f['id']) if dx == 0 else TEXTO, font=MONO)

        # tarjetitas con los promedios
        y = y2 - 110
        ancho = (x2 - x1 - 40 - 2 * 16) / 3
        datos = [('RETORNO PROMEDIO', f'{est.promedio_tr:.2f}', NEON),
                 ('ESPERA PROMEDIO', f'{est.promedio_te:.2f}', LILA),
                 ('RENDIMIENTO', f'{est.rendimiento:.2f}', NARANJA)]
        for i, (nombre, valor, col) in enumerate(datos):
            bx = x1 + 20 + i * (ancho + 16)
            c.rect_redondeado(bx, y, bx + ancho, y + 88, fill=mezclar(col, TARJETA, 0.9), outline=mezclar(col, BORDE, 0.4))
            c.create_text(bx + 16, y + 20, text=nombre, anchor='w', fill=TENUE, font=MONO_CHICO)
            c.texto_neon(bx + 16, y + 34, valor, col, ('Segoe UI', 22, 'bold'))
        c.create_text(x2 - 24, y - 14, text='rendimiento = procesos terminados / tiempo total',
                      anchor='e', fill=TENUE, font=MONO_CHICO)

    def dibujar_gantt(self, x1, y1, x2, y2):
        c = self.lienzo
        c.tarjeta(x1, y1, x2, y2, 'diagrama de gantt · cpu', NEON)
        # sólo hasta el instante mostrado: el tick t ya se ejecutó en el motor, pero la foto es de antes
        hasta_ahora = Gantt()
        hasta_ahora.ticks = self.sim.gantt.ticks[:self.inst.t]
        tramos = hasta_ahora.tramos()
        hasta = max(self.inst.t, 1)
        gx1, gx2, gy = x1 + 24, x2 - 24, y1 + 44
        escala = (gx2 - gx1) / max(hasta, 12)
        for tr in tramos:
            tx1, tx2 = gx1 + tr.desde * escala, gx1 + tr.hasta * escala - 2
            if tr.proceso_id is None:
                c.rect_redondeado(tx1, gy, tx2, gy + 40, r=6, fill=TARJETA, outline=BORDE, dash=(3, 3))
                etiqueta, col = '—', TENUE
            else:
                col = color_de(tr.proceso_id)
                c.rect_redondeado(tx1, gy, tx2, gy + 40, r=6, fill=mezclar(col, TARJETA, 0.7), outline=col)
                etiqueta = f'P{tr.proceso_id}'
            if tx2 - tx1 > 22:
                c.create_text((tx1 + tx2) / 2, gy + 20, text=etiqueta, fill=col, font=MONO_CHICO)
        marcas = sorted({0, *(tr.hasta for tr in tramos)})
        for t in marcas:
            c.create_text(gx1 + t * escala, gy + 54, text=str(t), fill=TENUE, font=MONO_CHICO)

    def dibujar_botones(self, W, H):
        c = self.lienzo
        y = H - 70
        x = 32
        x += c.boton(x, y, 'Abrir CSV', self.abrir, LILA) + 14
        x += c.boton(x, y, 'Carga manual', self.carga_manual, LILA) + 14
        x += c.boton(x, y, 'Reiniciar', self.reiniciar, NARANJA, habilitado=self.sim is not None) + 14
        activo = self.sim is not None and self.estadisticas is None
        c.boton(W - 32 - 260, y, 'Siguiente evento  ▶', self.siguiente, NEON, habilitado=activo, ancho=260)
        c.create_text(W - 32 - 280, y + 19, text='Enter', anchor='e', fill=TENUE, font=MONO_CHICO)


class DialogoCarga:
    """Ventana para cargar hasta 10 procesos a mano. Las filas vacías se ignoran."""

    def __init__(self, padre: tk.Tk, al_aceptar):
        self.al_aceptar = al_aceptar
        self.v = tk.Toplevel(padre, bg=TARJETA, padx=24, pady=20)
        self.v.title('Carga manual de procesos')
        self.v.transient(padre)
        self.v.grab_set()
        self.v.resizable(False, False)

        tk.Label(self.v, text='CARGA MANUAL', bg=TARJETA, fg=NEON, font=('Segoe UI', 16, 'bold')).grid(
            row=0, column=0, columnspan=4, sticky='w')
        tk.Label(self.v, text=f'Hasta {MAX_PROCESOS} procesos · tamaño 1 a {MEMORIA_USUARIO}K · '
                              'las filas vacías se ignoran', bg=TARJETA, fg=TENUE, font=MONO_CHICO).grid(
            row=1, column=0, columnspan=4, sticky='w', pady=(0, 12))
        for col, nombre in enumerate(('PROCESO', 'TAMAÑO (K)', 'ARRIBO', 'IRRUPCIÓN')):
            tk.Label(self.v, text=nombre, bg=TARJETA, fg=TENUE, font=MONO_CHICO).grid(row=2, column=col, padx=6)

        self.campos = []
        for i in range(MAX_PROCESOS):
            tk.Label(self.v, text=f'P{i + 1}', bg=TARJETA, fg=color_de(i + 1), font=SUBTITULO).grid(row=3 + i, column=0)
            fila = []
            for col in range(3):
                e = tk.Entry(self.v, width=10, bg='#14171e', fg=TEXTO, insertbackground=NEON, relief='flat',
                             font=MONO, justify='center', highlightthickness=1,
                             highlightbackground=BORDE, highlightcolor=NEON)
                e.grid(row=3 + i, column=col + 1, padx=6, pady=3, ipady=4)
                fila.append(e)
            self.campos.append(fila)
        self.campos[0][0].focus_set()

        tk.Button(self.v, text='Simular', command=self.aceptar, bg=mezclar(NEON, TARJETA, 0.8), fg=NEON,
                  activebackground=mezclar(NEON, TARJETA, 0.6), activeforeground=TEXTO, relief='flat',
                  font=SUBTITULO, padx=18, pady=6, cursor='hand2').grid(
            row=4 + MAX_PROCESOS, column=0, columnspan=4, pady=(16, 0), sticky='e')
        self.v.bind('<Return>', lambda _e: self.aceptar())

    def aceptar(self):
        filas = []
        try:
            for i, fila in enumerate(self.campos):
                textos = [e.get().strip() for e in fila]
                if not any(textos):
                    continue
                if not all(textos):
                    raise ErrorCarga(f'Proceso {i + 1}: faltan datos.')
                try:
                    tamano, arribo, irrupcion = (int(t) for t in textos)
                except ValueError:
                    raise ErrorCarga(f'Proceso {i + 1}: todos los datos tienen que ser números enteros.') from None
                filas.append({'id': i + 1, 'tamano': tamano, 'arribo': arribo, 'irrupcion': irrupcion})
            errores = validar_procesos(filas)
            if errores:
                raise ErrorCarga('\n'.join(errores))
        except ErrorCarga as e:
            messagebox.showerror('Datos inválidos', str(e), parent=self.v)
            return
        self.v.destroy()
        self.al_aceptar([Proceso(f['id'], f['tamano'], f['arribo'], f['irrupcion']) for f in filas])


def ejecutar(ruta_inicial: str | None = None):
    raiz = tk.Tk()
    App(raiz, ruta_inicial)
    raiz.mainloop()
