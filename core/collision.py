def colisao(poly, colocadas, margem):

    for p in colocadas:

        if poly.buffer(margem).intersects(
            p["poly"].buffer(margem)
        ):
            return True

    return False