# -*- coding: utf-8 -*-
"""
Plantilla imprimible de pasaporte (estilo Colombia) para trabajo escolar.
- Hoja carta vertical, escala 100%.
- Cada pliego = 2 paginas de pasaporte de 88 x 125 mm (tamano real ID-3).
- Linea de doblez punteada al centro, marcas de corte en las esquinas.
- Todo en lineas negras/grises para colorear a mano.
"""
import math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT = "/tmp/claude-0/-home-user-Core/46a8c2c9-9143-56df-8e00-82a83b14f864/scratchpad/Pasaporte_para_imprimir.pdf"

PW, PH = letter                 # 215.9 x 279.4 mm
PAGE_W = 88 * mm                # ancho de una pagina de pasaporte
PAGE_H = 125 * mm               # alto de una pagina de pasaporte
SPREAD_W = 2 * PAGE_W           # pliego abierto
SPREAD_H = PAGE_H

GRAY_FAINT = 0.82               # ondas de fondo
GRAY_SOFT = 0.55                # textos guia
BLACK = 0.0

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("Pasaporte para imprimir - plantilla escolar")


# ----------------------------------------------------------------------
# utilidades de dibujo
# ----------------------------------------------------------------------
def crop_marks(x, y, w, h):
    """Marcas de corte en las 4 esquinas de un rectangulo (x,y = esq. inf. izq.)."""
    L = 4 * mm
    g = 0.8 * mm  # separacion para no invadir el area
    c.setLineWidth(0.4)
    c.setStrokeGray(BLACK)
    for cx, sx in ((x, -1), (x + w, 1)):
        for cy, sy in ((y, -1), (y + h, 1)):
            c.line(cx + sx * g, cy, cx + sx * (g + L), cy)
            c.line(cx, cy + sy * g, cx, cy + sy * (g + L))


def fold_line(x, y, h):
    """Linea de doblez punteada vertical."""
    c.saveState()
    c.setDash(2, 2.5)
    c.setLineWidth(0.4)
    c.setStrokeGray(0.45)
    c.line(x, y + 1.5 * mm, x, y + h - 1.5 * mm)
    c.restoreState()


def guilloche(x, y, w, h, waves=9, amp_mm=2.2, gray=GRAY_FAINT):
    """Ondas suaves de fondo imitando el guilloche de los pasaportes."""
    c.saveState()
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + w, y)
    p.lineTo(x + w, y + h)
    p.lineTo(x, y + h)
    p.close()
    c.clipPath(p, stroke=0, fill=0)
    c.setLineWidth(0.3)
    c.setStrokeGray(gray)
    n = 90
    for i in range(waves):
        yy = y + (i + 0.5) * h / waves
        amp = amp_mm * mm
        ph = i * 0.9
        pts = []
        for k in range(n + 1):
            xx = x + w * k / n
            pts.append((xx, yy + amp * math.sin(2 * math.pi * 2.2 * k / n + ph)))
        pp = c.beginPath()
        pp.moveTo(*pts[0])
        for pt in pts[1:]:
            pp.lineTo(*pt)
        c.drawPath(pp, stroke=1, fill=0)
    c.restoreState()


def dotted_line(x1, y, x2):
    c.saveState()
    c.setDash(0.8, 1.6)
    c.setLineWidth(0.5)
    c.setStrokeGray(0.35)
    c.line(x1, y, x2, y)
    c.restoreState()


def ctext(x, y, txt, size=8, font="Helvetica", gray=BLACK):
    c.setFont(font, size)
    c.setFillGray(gray)
    c.drawCentredString(x, y, txt)


def ltext(x, y, txt, size=8, font="Helvetica", gray=BLACK):
    c.setFont(font, size)
    c.setFillGray(gray)
    c.drawString(x, y, txt)


def page_frame(x, y, inset_mm=4):
    """Doble marco decorativo dentro de una pagina de pasaporte."""
    i1 = inset_mm * mm
    c.setLineWidth(0.7)
    c.setStrokeGray(BLACK)
    c.rect(x + i1, y + i1, PAGE_W - 2 * i1, PAGE_H - 2 * i1)
    c.setLineWidth(0.3)
    c.rect(x + i1 + 1.2 * mm, y + i1 + 1.2 * mm,
           PAGE_W - 2 * i1 - 2.4 * mm, PAGE_H - 2 * i1 - 2.4 * mm)


def page_number(x, y, num):
    ctext(x + PAGE_W / 2, y + 6.2 * mm, str(num), 6, "Helvetica", 0.25)


# ----------------------------------------------------------------------
# paginas del pasaporte (cada funcion dibuja UNA pagina de 88x125)
# ----------------------------------------------------------------------
def pg_blank_label(x, y, label):
    """Cara que queda pegada por dentro (opcional)."""
    ctext(x + PAGE_W / 2, y + PAGE_H / 2, label, 7, "Helvetica-Oblique", 0.6)


def pg_cover_front(x, y):
    # marco doble grueso
    c.setLineWidth(1.1)
    c.setStrokeGray(BLACK)
    c.rect(x + 4 * mm, y + 4 * mm, PAGE_W - 8 * mm, PAGE_H - 8 * mm)
    c.setLineWidth(0.4)
    c.rect(x + 6 * mm, y + 6 * mm, PAGE_W - 12 * mm, PAGE_H - 12 * mm)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 22 * mm, "REPÚBLICA DE COLOMBIA", 10.5, "Helvetica-Bold")
    c.setLineWidth(0.5)
    c.line(cx - 26 * mm, y + PAGE_H - 25.5 * mm, cx + 26 * mm, y + PAGE_H - 25.5 * mm)
    # escudo: circulo guia para dibujar/colorear
    r = 16 * mm
    ey = y + PAGE_H / 2 + 6 * mm
    c.setLineWidth(0.7)
    c.circle(cx, ey, r)
    c.setLineWidth(0.3)
    c.circle(cx, ey, r - 1.5 * mm)
    ctext(cx, ey + 2 * mm, "ESCUDO", 6.5, "Helvetica", GRAY_SOFT)
    ctext(cx, ey - 1.5 * mm, "(dibujar y colorear", 5, "Helvetica-Oblique", GRAY_SOFT)
    ctext(cx, ey - 4.5 * mm, "el escudo nacional)", 5, "Helvetica-Oblique", GRAY_SOFT)
    ctext(cx, y + 34 * mm, "PASAPORTE", 13, "Helvetica-Bold")
    ctext(cx, y + 29 * mm, "PASSPORT", 8, "Helvetica")
    # simbolo de pasaporte electronico (chip)
    chw, chh = 9 * mm, 6.5 * mm
    chx, chy = cx - chw / 2, y + 14 * mm
    c.setLineWidth(0.6)
    c.roundRect(chx, chy, chw, chh, 1.2 * mm)
    c.circle(cx, chy + chh / 2, 1.6 * mm)
    c.line(chx, chy + chh / 2, cx - 1.6 * mm, chy + chh / 2)
    c.line(cx + 1.6 * mm, chy + chh / 2, chx + chw, chy + chh / 2)


def pg_cover_inside(x, y):
    page_frame(x, y)
    guilloche(x + 6 * mm, y + 6 * mm, PAGE_W - 12 * mm, PAGE_H - 12 * mm, waves=7)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 20 * mm, "REPÚBLICA DE COLOMBIA", 8, "Helvetica-Bold")
    lines = [
        "El Gobierno de la República de Colombia",
        "solicita a las autoridades de los países",
        "amigos permitir el libre tránsito al titular",
        "de este pasaporte y prestarle toda la",
        "ayuda y protección que requiera.",
    ]
    yy = y + PAGE_H - 32 * mm
    for ln in lines:
        ctext(cx, yy, ln, 6.5, "Helvetica-Oblique", 0.2)
        yy -= 4 * mm
    ctext(cx, y + 28 * mm, "Este pasaporte contiene 32 páginas", 6, "Helvetica", 0.3)
    ctext(cx, y + 24 * mm, "This passport contains 32 pages", 5.5, "Helvetica-Oblique", 0.45)


def field(x, y, w, label_es, label_en, value=""):
    """Campo con etiqueta bilingue pequena y linea punteada para escribir."""
    ltext(x, y + 2.6 * mm, label_es + " / " + label_en, 4.3, "Helvetica", 0.35)
    if value:
        ltext(x, y - 0.6 * mm, value, 6.5, "Helvetica-Bold")
        dotted_line(x + c.stringWidth(value, "Helvetica-Bold", 6.5) + 2 * mm,
                    y - 0.8 * mm, x + w)
    else:
        dotted_line(x, y - 0.8 * mm, x + w)


def pg_data(x, y):
    """Pagina de datos con foto, campos y zona MRZ."""
    page_frame(x, y, inset_mm=3)
    inx, iny = x + 5 * mm, y + 5 * mm
    inw = PAGE_W - 10 * mm
    guilloche(x + 4.5 * mm, y + 30 * mm, PAGE_W - 9 * mm, PAGE_H - 36 * mm,
              waves=8, amp_mm=1.8, gray=0.88)
    cx = x + PAGE_W / 2
    # encabezado
    ctext(cx, y + PAGE_H - 11 * mm, "REPÚBLICA DE COLOMBIA", 7.5, "Helvetica-Bold")
    ctext(cx, y + PAGE_H - 15 * mm, "PASAPORTE / PASSPORT", 6, "Helvetica")
    c.setLineWidth(0.4)
    c.line(inx, y + PAGE_H - 17 * mm, inx + inw, y + PAGE_H - 17 * mm)
    # tipo / codigo / numero
    ty = y + PAGE_H - 23.5 * mm
    field(inx, ty, 12 * mm, "Tipo", "Type", "P")
    field(inx + 15 * mm, ty, 14 * mm, "País", "Country", "COL")
    field(inx + 33 * mm, ty, inw - 33 * mm, "Pasaporte N.", "Passport No.")
    # foto 30 x 40 mm
    fw, fh = 30 * mm, 40 * mm
    fx, fy = inx, y + PAGE_H - 27 * mm - fh
    c.setLineWidth(0.6)
    c.rect(fx, fy, fw, fh)
    # silueta guia dentro de la foto
    c.saveState()
    c.setLineWidth(0.35)
    c.setStrokeGray(0.6)
    hx, hy = fx + fw / 2, fy + fh * 0.62
    c.ellipse(hx - 6.5 * mm, hy - 8 * mm, hx + 6.5 * mm, hy + 8 * mm)  # cabeza
    p = c.beginPath()  # hombros
    p.moveTo(fx + 4 * mm, fy + 2 * mm)
    p.curveTo(fx + 8 * mm, fy + 12 * mm, fx + fw - 8 * mm, fy + 12 * mm,
              fx + fw - 4 * mm, fy + 2 * mm)
    c.drawPath(p)
    c.restoreState()
    ctext(fx + fw / 2, fy - 3 * mm, "FOTO 3 x 4 cm", 4.5, "Helvetica", 0.4)
    # campos a la derecha de la foto
    dx = fx + fw + 4 * mm
    dw = inx + inw - dx
    fy2 = y + PAGE_H - 31 * mm
    step = 8 * mm
    field(dx, fy2 - 0 * step, dw, "Apellidos", "Surname")
    field(dx, fy2 - 1 * step, dw, "Nombres", "Given names")
    field(dx, fy2 - 2 * step, dw, "Nacionalidad", "Nationality", "COLOMBIANA")
    field(dx, fy2 - 3 * step, dw, "Fecha de nacimiento", "Date of birth")
    field(dx, fy2 - 4 * step, 16 * mm, "Sexo", "Sex")
    field(dx + 20 * mm, fy2 - 4 * step, dw - 20 * mm, "Lugar de nacimiento", "Place of birth")
    # campos de ancho completo bajo la foto
    by = fy - 10 * mm
    field(inx, by, 38 * mm, "Fecha de expedición", "Date of issue")
    field(inx + 42 * mm, by, inw - 42 * mm, "Fecha de vencimiento", "Date of expiry")
    by2 = by - 9 * mm
    field(inx, by2, 38 * mm, "Autoridad", "Authority", "CANCILLERÍA")
    field(inx + 42 * mm, by2, inw - 42 * mm, "Firma del titular", "Holder's signature")
    # zona MRZ (codigo de lectura mecanica)
    mz_h = 14 * mm
    c.setLineWidth(0.4)
    c.setStrokeGray(BLACK)
    c.line(x + 4 * mm, y + 4 * mm + mz_h, x + PAGE_W - 4 * mm, y + 4 * mm + mz_h)
    c.setFont("Courier-Bold", 7.2)
    c.setFillGray(0.35)
    l1 = "P<COLAPELLIDO<<NOMBRE<<<<<<<<<<<<<<<<<<<<<<<<"
    l2 = "AB1234567<8COL0000000M0000000<<<<<<<<<<<<<<02"
    c.drawString(x + 5 * mm, y + 12.5 * mm, l1)
    c.drawString(x + 5 * mm, y + 7.5 * mm, l2)


def pg_observaciones(x, y, num):
    page_frame(x, y)
    guilloche(x + 6 * mm, y + 10 * mm, PAGE_W - 12 * mm, PAGE_H - 26 * mm, waves=8)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 13 * mm, "OBSERVACIONES", 8, "Helvetica-Bold")
    ctext(cx, y + PAGE_H - 17 * mm, "OBSERVATIONS", 6, "Helvetica", 0.4)
    yy = y + PAGE_H - 28 * mm
    while yy > y + 14 * mm:
        dotted_line(x + 9 * mm, yy, x + PAGE_W - 9 * mm)
        yy -= 8 * mm
    page_number(x, y, num)


def pg_visa(x, y, num):
    page_frame(x, y)
    guilloche(x + 6 * mm, y + 10 * mm, PAGE_W - 12 * mm, PAGE_H - 26 * mm,
              waves=10, amp_mm=2.6)
    cx = x + PAGE_W / 2
    # emblema central tenue para colorear
    c.saveState()
    c.setLineWidth(0.35)
    c.setStrokeGray(0.7)
    cyy = y + PAGE_H / 2
    c.circle(cx, cyy, 18 * mm)
    c.circle(cx, cyy, 14.5 * mm)
    for k in range(12):
        a = k * math.pi / 6
        c.line(cx + 14.5 * mm * math.cos(a), cyy + 14.5 * mm * math.sin(a),
               cx + 18 * mm * math.cos(a), cyy + 18 * mm * math.sin(a))
    c.restoreState()
    ctext(cx, y + PAGE_H - 13 * mm, "VISAS", 8.5, "Helvetica-Bold")
    ctext(cx, y + PAGE_H - 17 * mm, "VISAS", 6, "Helvetica-Oblique", 0.4)
    # esquinas guia para pegar sellos/visas
    c.setLineWidth(0.4)
    c.setStrokeGray(0.5)
    for sx in (x + 10 * mm, x + PAGE_W - 10 * mm):
        for sy in (y + 14 * mm, y + PAGE_H - 22 * mm):
            dx = 3 * mm if sx < cx else -3 * mm
            dy = 3 * mm if sy < cyy else -3 * mm
            c.line(sx, sy, sx + dx, sy)
            c.line(sx, sy, sx, sy + dy)
    page_number(x, y, num)


def pg_anotaciones(x, y, num):
    page_frame(x, y)
    guilloche(x + 6 * mm, y + 10 * mm, PAGE_W - 12 * mm, PAGE_H - 26 * mm, waves=8)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 13 * mm, "ANOTACIONES", 8, "Helvetica-Bold")
    ctext(cx, y + PAGE_H - 17 * mm, "ENDORSEMENTS", 6, "Helvetica", 0.4)
    yy = y + PAGE_H - 28 * mm
    while yy > y + 14 * mm:
        dotted_line(x + 9 * mm, yy, x + PAGE_W - 9 * mm)
        yy -= 8 * mm
    page_number(x, y, num)


def pg_emergencia(x, y, num):
    page_frame(x, y)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 13 * mm, "EN CASO DE EMERGENCIA", 7.5, "Helvetica-Bold")
    ctext(cx, y + PAGE_H - 17 * mm, "IN CASE OF EMERGENCY", 5.5, "Helvetica", 0.4)
    yy = y + PAGE_H - 30 * mm
    for es, en in [("Nombre", "Name"), ("Dirección", "Address"),
                   ("Teléfono", "Telephone"), ("Ciudad y país", "City and country")]:
        field(x + 9 * mm, yy, PAGE_W - 18 * mm, es, en)
        yy -= 11 * mm
    ctext(cx, y + 22 * mm, "El titular debe firmar la página de datos.", 5.5,
          "Helvetica-Oblique", 0.4)
    page_number(x, y, num)


def pg_recomendaciones(x, y):
    page_frame(x, y)
    guilloche(x + 6 * mm, y + 6 * mm, PAGE_W - 12 * mm, PAGE_H - 12 * mm, waves=7)
    cx = x + PAGE_W / 2
    ctext(cx, y + PAGE_H - 16 * mm, "RECOMENDACIONES", 7.5, "Helvetica-Bold")
    lines = [
        "1. Este pasaporte es un documento de",
        "identidad y de viaje. Consérvelo en",
        "buen estado y en lugar seguro.",
        "",
        "2. En caso de pérdida o robo, informe",
        "de inmediato a la autoridad competente.",
        "",
        "3. No haga anotaciones ni alteraciones",
        "en este documento.",
    ]
    yy = y + PAGE_H - 26 * mm
    for ln in lines:
        if ln:
            ctext(cx, yy, ln, 6, "Helvetica", 0.2)
        yy -= 4.2 * mm


def pg_cover_back(x, y):
    c.setLineWidth(1.1)
    c.setStrokeGray(BLACK)
    c.rect(x + 4 * mm, y + 4 * mm, PAGE_W - 8 * mm, PAGE_H - 8 * mm)
    c.setLineWidth(0.4)
    c.rect(x + 6 * mm, y + 6 * mm, PAGE_W - 12 * mm, PAGE_H - 12 * mm)
    cx = x + PAGE_W / 2
    # adorno central sencillo
    c.setLineWidth(0.5)
    c.circle(cx, y + PAGE_H / 2, 8 * mm)
    c.circle(cx, y + PAGE_H / 2, 6.5 * mm)


# ----------------------------------------------------------------------
# armado de pliegos y hojas
# ----------------------------------------------------------------------
def draw_spread(x, y, left_fn, right_fn, sheet_label):
    """Dibuja un pliego: pagina izquierda + derecha, marcas de corte y doblez."""
    crop_marks(x, y, SPREAD_W, SPREAD_H)
    left_fn(x, y)
    right_fn(x + PAGE_W, y)
    fold_line(x + PAGE_W, y, SPREAD_H)
    ltext(x, y + SPREAD_H + 2.2 * mm, sheet_label, 6, "Helvetica", 0.45)


MARGIN_X = (PW - SPREAD_W) / 2
GAP = 8 * mm
TOP_Y = PH - 14 * mm - SPREAD_H
BOT_Y = TOP_Y - GAP - SPREAD_H

# ---- pagina 1: instrucciones -----------------------------------------
cx = PW / 2
ctext(cx, PH - 22 * mm, "PASAPORTE PARA IMPRIMIR, RECORTAR Y ARMAR", 14, "Helvetica-Bold")
ctext(cx, PH - 28 * mm, "Plantilla escolar - estilo República de Colombia - tamaño real: 88 x 125 mm por página",
      8.5, "Helvetica", 0.3)

ins = [
    ("IMPRESIÓN", [
        "Imprime las 4 hojas siguientes en papel carta, escala 100% (tamaño real).",
        'En el cuadro de impresión elige "Tamaño real" o "Escala 100%". NO uses "Ajustar a la página".',
        "Si puedes, usa papel un poco grueso (120-180 g) para las cubiertas.",
    ]),
    ("RECORTE Y DOBLEZ", [
        "Recorta cada pliego siguiendo las marcas de las esquinas (líneas continuas).",
        "Dobla cada pliego por la línea punteada del centro, con lo impreso hacia AFUERA.",
        "Cada pliego doblado queda del tamaño final del pasaporte: 88 x 125 mm.",
    ]),
    ("ARMADO", [
        "Pega las caras en blanco que quedan por dentro de cada pliego (pegante en barra).",
        "Apila los pliegos en el orden indicado (Hoja 1, 2, 3...) con el doblez hacia la izquierda.",
        "Une todo por el lomo (lado del doblez): grapa, cose o pega. ¡Listo el pasaporte!",
    ]),
    ("PARA TERMINAR A MANO", [
        "Dibuja y colorea el escudo en la portada (guía circular).",
        "Pega o dibuja la foto en el recuadro de la página de datos y llena los campos.",
        "Colorea suavemente los fondos de ondas imitando los colores reales (vinotinto la portada).",
    ]),
]
yy = PH - 40 * mm
for title, items in ins:
    ltext(20 * mm, yy, title, 10, "Helvetica-Bold")
    yy -= 6 * mm
    for it in items:
        ltext(24 * mm, yy, u"• " + it, 8.5, "Helvetica", 0.15)
        yy -= 5.2 * mm
    yy -= 3.5 * mm

ltext(20 * mm, yy - 2 * mm,
      "Orden de armado: Hoja 1 (cubierta) - Hoja 2 - Hoja 3 - Hoja 4 - Hoja 5 - Hoja 6 - Hoja 7 - Hoja 8 (contracubierta).",
      8, "Helvetica-Oblique", 0.3)
c.showPage()

# ---- hojas con pliegos ------------------------------------------------
# Cada pliego doblado es una "hoja" del cuadernillo:
#   cara frontal = mitad DERECHA, cara posterior = mitad IZQUIERDA.
def L(fn, *args):
    return lambda x, y: fn(x, y, *args)

spreads = [
    ("HOJA 1 - Cubierta: portada (frente) + mensaje interior (atrás)",
     pg_cover_inside, pg_cover_front),
    ("HOJA 2 - Página de datos (frente) + Observaciones (atrás)",
     L(pg_observaciones, 2), pg_data),
    ("HOJA 3 - Visas (páginas 3 y 4)",
     L(pg_visa, 4), L(pg_visa, 3)),
    ("HOJA 4 - Visas (páginas 5 y 6)",
     L(pg_visa, 6), L(pg_visa, 5)),
    ("HOJA 5 - Visas (páginas 7 y 8)",
     L(pg_visa, 8), L(pg_visa, 7)),
    ("HOJA 6 - Visas (páginas 9 y 10)",
     L(pg_visa, 10), L(pg_visa, 9)),
    ("HOJA 7 - Anotaciones (frente) + Emergencia (atrás)",
     L(pg_emergencia, 12), L(pg_anotaciones, 11)),
    ("HOJA 8 - Contracubierta: recomendaciones (frente) + tapa trasera (atrás)",
     pg_cover_back, pg_recomendaciones),
]

for i in range(0, len(spreads), 2):
    lbl1, l1f, r1f = spreads[i]
    draw_spread(MARGIN_X, TOP_Y, l1f, r1f, lbl1)
    if i + 1 < len(spreads):
        lbl2, l2f, r2f = spreads[i + 1]
        draw_spread(MARGIN_X, BOT_Y, l2f, r2f, lbl2)
    ctext(PW / 2, 8 * mm,
          "Imprimir al 100% (tamaño real) - papel carta - página de pasaporte: 88 x 125 mm",
          6.5, "Helvetica", 0.5)
    c.showPage()

c.save()
print("OK ->", OUT)
