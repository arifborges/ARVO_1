from shapely.affinity import translate, rotate
from core.collision import colisao
import random

ROTACOES = [0, 90, 180]

cores = [
    "#ff69c9",
    "#00c8ff",
    "#00ff99",
    "#ffd700",
    "#9b59b6",
    "#ff5733"
]

def gerar_pontos(colocadas, margem):

    pontos = [(0,0)]

    for p in colocadas:

        minx, miny, maxx, maxy = p["poly"].bounds

        pontos.extend([
            (maxx + margem, miny),
            (minx, maxy + margem),
            (maxx + margem, maxy + margem)
        ])

    pontos = sorted(
        pontos,
        key=lambda k: (k[1], k[0])
    )

    return pontos

def nesting(
    polys,
    largura_tecido,
    altura_tecido,
    margem
):

    colocadas = []
    sobras = []

    polys = sorted(
        polys,
        key=lambda p: p["poly"].area,
        reverse=True
    )

    for item in polys:

        nome = item["nome"]
        base_poly = item["poly"]

        encaixou = False

        for rot in ROTACOES:

            poly_rot = rotate(
                base_poly,
                rot,
                origin=(0,0)
            )

            minx, miny, _, _ = poly_rot.bounds

            pontos = gerar_pontos(
                colocadas,
                margem
            )

            for px, py in pontos:

                movido = translate(
                    poly_rot,
                    xoff=px - minx,
                    yoff=py - miny
                )

                bx1, by1, bx2, by2 = movido.bounds

                if (
                    bx1 < 0 or
                    by1 < 0 or
                    bx2 > largura_tecido or
                    by2 > altura_tecido
                ):
                    continue

                if not colisao(
                    movido,
                    colocadas,
                    margem
                ):

                    colocadas.append({
                        "nome": nome,
                        "poly": movido,
                        "cor": random.choice(cores)
                    })

                    encaixou = True
                    break

            if encaixou:
                break

        if not encaixou:
            sobras.append(nome)

    return colocadas, sobras