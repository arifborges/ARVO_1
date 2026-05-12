def calcular_metricas(
    colocadas,
    largura_tecido,
    altura_tecido
):

    area_usada = sum([
        p["poly"].area
        for p in colocadas
    ])

    area_total = (
        largura_tecido *
        altura_tecido
    )

    desperdicio = (
        area_total -
        area_usada
    )

    aproveitamento = (
        area_usada /
        area_total
    ) * 100

    return {
        "area_usada": area_usada,
        "desperdicio": desperdicio,
        "aproveitamento": aproveitamento
    }