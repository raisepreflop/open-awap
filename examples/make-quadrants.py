#!/usr/bin/env python3
"""
The quadrant plane of Open AWAP 2.0, as SVG, for the README and the SPEC.

Se generan DOS ficheros —claro y oscuro— desde esta única fuente: GitHub no deja que un SVG herede
el color del tema, así que la alternativa sería mantener dos dibujos a mano y que se separen.

Lo que el dibujo tiene que enseñar, y por qué:
  · los dos ejes, sin ninguna diagonal ni suma: la norma prohíbe combinarlos (§6.1);
  · el eje X con sus SEIS anclas, porque la cobertura es discreta y no un porcentaje continuo;
  · la frontera en 50 con trazo discontinuo: es convencional, no una división natural (§5);
  · un punto de ejemplo CON SU BANDA, que es lo que §5 obliga a mostrar en vez de la cifra sola;
  · los cuatro cuadrantes con el mismo peso visual: Q4 no es el cuadrante del fracaso (§1.5).
"""
import pathlib

CLARO = dict(
    ink="#1f2328", mut="#59636e", linea="#d0d7de", tenue="#f6f8fa",
    acc="#8a6d0b", accsuave="#f0e6c8", papel="#ffffff",
)
OSCURO = dict(
    ink="#e6edf3", mut="#9198a1", linea="#3d444d", tenue="#161b22",
    acc="#d4a72c", accsuave="#3b2f0f", papel="#0d1117",
)

# Lienzo y caja de datos (en coordenadas del SVG).
W, H = 780, 580
X0, X1 = 116, 712          # eje X: cobertura 0 → 100
Y0, Y1 = 462, 96           # eje Y: puntuación 0 → 100 (el SVG crece hacia abajo)
ex = lambda v: X0 + (X1 - X0) * v / 100
ey = lambda v: Y0 + (Y1 - Y0) * v / 100

ANCLAS = [(0, "file"), (20, "manuscript"), (50, "partial draft"), (75, "outline"), (85, "bible"), (100, "premise")]
CUADRANTES = [
    (25, 75, "Q2", "Accredited transformation", "documented human work", "on an unobserved base"),
    (75, 75, "Q1", "Verified authorship", "the only position that admits", "the full claim"),
    (25, 25, "Q3", "Unaccredited", "sealed and scanned only:", "no score"),
    (75, 25, "Q4", "Documented generation", "a recorded process showing", "little human authorship"),
]
# El ejemplo: la obra de examples/certificate.jsonld — entró con manuscrito (cobertura 20) y su MAS
# es 68, banda 60-69. Cae en Q2, que es el caso más común y el que la v1.0 no sabía representar.
EJ_X, EJ_Y, EJ_BANDA = 20, 68, (60, 69)


def svg(c: dict) -> str:
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'font-family="ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif" '
      f'role="img" aria-label="The four quadrants of Open AWAP 2.0: coverage of the record on the X axis, '
      f'authorship in what was observed on the Y axis, boundary at 50 on both axes.">')
    a(f'<rect width="{W}" height="{H}" fill="{c["papel"]}"/>')

    # Título y subtítulo
    a(f'<text x="{X0}" y="38" font-size="17" font-weight="600" fill="{c["ink"]}">The four quadrants</text>')
    a(f'<text x="{X0}" y="58" font-size="12.5" fill="{c["mut"]}">Two measures over different windows. '
      f'They are never summed, averaged or reduced to one number.</text>')

    # Las cuatro celdas, del mismo peso
    for cx, cy, *_ in CUADRANTES:
        x = ex(cx - 25) if cx == 25 else ex(50)
        y = ey(100) if cy == 75 else ey(50)
        a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{(ex(50) - ex(0)):.1f}" height="{(ey(50) - ey(100)):.1f}" '
          f'fill="{c["tenue"]}" stroke="{c["linea"]}" stroke-width="1"/>')

    # Frontera convencional en 50
    a(f'<line x1="{ex(50):.1f}" y1="{ey(0):.1f}" x2="{ex(50):.1f}" y2="{ey(100):.1f}" '
      f'stroke="{c["linea"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    a(f'<line x1="{ex(0):.1f}" y1="{ey(50):.1f}" x2="{ex(100):.1f}" y2="{ey(50):.1f}" '
      f'stroke="{c["linea"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')

    # Etiquetas de los cuadrantes, ARRIBA de su celda: el centro se deja libre para los puntos.
    for cx, cy, sigla, nombre, l1, l2 in CUADRANTES:
        x = ex(cx)
        techo = ey(100) if cy == 75 else ey(50)
        a(f'<text x="{x:.1f}" y="{techo + 26:.1f}" font-size="15" font-weight="700" fill="{c["ink"]}" text-anchor="middle">{sigla}</text>')
        a(f'<text x="{x:.1f}" y="{techo + 45:.1f}" font-size="12.5" font-weight="600" fill="{c["ink"]}" text-anchor="middle">{nombre}</text>')
        a(f'<text x="{x:.1f}" y="{techo + 63:.1f}" font-size="11" fill="{c["mut"]}" text-anchor="middle">{l1}</text>')
        a(f'<text x="{x:.1f}" y="{techo + 78:.1f}" font-size="11" fill="{c["mut"]}" text-anchor="middle">{l2}</text>')

    # Ejes
    a(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{c["ink"]}" stroke-width="1.5"/>')
    a(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{c["ink"]}" stroke-width="1.5"/>')

    # Eje X: las seis anclas (la cobertura es discreta)
    for v, et in ANCLAS:
        x = ex(v)
        a(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y0 + 6}" stroke="{c["ink"]}" stroke-width="1.5"/>')
        a(f'<text x="{x:.1f}" y="{Y0 + 21}" font-size="11.5" fill="{c["ink"]}" text-anchor="middle">{v}</text>')
        a(f'<text x="{x:.1f}" y="{Y0 + 35}" font-size="10.5" fill="{c["mut"]}" text-anchor="middle">{et}</text>')
    a(f'<text x="{(X0 + X1) / 2:.1f}" y="{Y0 + 60}" font-size="12.5" font-weight="600" fill="{c["ink"]}" text-anchor="middle">'
      f'Coverage of the record  ·  X axis  ·  fixed at entry, never recomputed</text>')

    # Eje Y: 0, 50, 100
    for v in (0, 50, 100):
        y = ey(v)
        a(f'<line x1="{X0 - 6}" y1="{y:.1f}" x2="{X0}" y2="{y:.1f}" stroke="{c["ink"]}" stroke-width="1.5"/>')
        a(f'<text x="{X0 - 12}" y="{y + 4:.1f}" font-size="11.5" fill="{c["ink"]}" text-anchor="end">{v}</text>')
    a(f'<text transform="translate({X0 - 52} {(Y0 + Y1) / 2:.1f}) rotate(-90)" font-size="12.5" font-weight="600" '
      f'fill="{c["ink"]}" text-anchor="middle">Authorship in what was observed  ·  Y axis</text>')
    a(f'<text transform="translate({X0 - 36} {(Y0 + Y1) / 2:.1f}) rotate(-90)" font-size="11" '
      f'fill="{c["mut"]}" text-anchor="middle">HAS on the origin track, MAS on transformation</text>')

    # El ejemplo, con su banda: nunca la cifra sola
    bx, by0, by1 = ex(EJ_X), ey(EJ_BANDA[0]), ey(EJ_BANDA[1])
    a(f'<rect x="{bx - 26:.1f}" y="{by1:.1f}" width="52" height="{by0 - by1:.1f}" fill="{c["accsuave"]}" '
      f'stroke="{c["acc"]}" stroke-width="1"/>')
    a(f'<circle cx="{bx:.1f}" cy="{ey(EJ_Y):.1f}" r="5.5" fill="{c["acc"]}"/>')
    a(f'<text x="{bx + 34:.1f}" y="{ey(EJ_Y) + 1:.1f}" font-size="11.5" font-weight="600" fill="{c["ink"]}">68 · band 60-69</text>')
    a(f'<text x="{bx - 26:.1f}" y="{by0 + 15:.1f}" font-size="10.5" fill="{c["mut"]}">example: entered with a finished manuscript</text>')

    # Pie: lo que la frontera NO es. En dos líneas, que quepan en el lienzo.
    a(f'<text x="{X0}" y="{H - 30}" font-size="11" fill="{c["mut"]}">'
      f'The boundary at 50 is conventional: a work at 51 and a work at 49 are not different in kind.</text>')
    a(f'<text x="{X0}" y="{H - 14}" font-size="11" fill="{c["mut"]}">'
      f'Show the point and its band, never the line as if it separated natural categories.</text>')
    a("</svg>")
    return "\n".join(p) + "\n"


destino = pathlib.Path(__file__).resolve().parent
for nombre, colores in (("quadrants-light.svg", CLARO), ("quadrants-dark.svg", OSCURO)):
    (destino / nombre).write_text(svg(colores), encoding="utf-8")
    print("escrito", destino / nombre)
