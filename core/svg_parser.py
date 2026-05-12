from svgpathtools import svg2paths
from shapely.geometry import Polygon
from shapely.affinity import translate, scale

def extrair_poligonos_svg(svg_path, escala):

    paths, _ = svg2paths(svg_path)

    polygons = []

    for path in paths:

        pontos = []

        for seg in path:

            pontos.append((
                seg.start.real,
                -seg.start.imag
            ))

        if len(pontos) < 3:
            continue

        try:

            poly = Polygon(pontos)

            if poly.area <= 1:
                continue

            if not poly.is_valid:
                poly = poly.buffer(0)

            minx, miny, _, _ = poly.bounds

            poly = translate(
                poly,
                xoff=-minx,
                yoff=-miny
            )

            poly = scale(
                poly,
                xfact=escala,
                yfact=escala,
                origin=(0,0)
            )

            polygons.append(poly)

        except:
            pass

    return polygons