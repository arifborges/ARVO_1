import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def desenhar_layout(
    colocadas,
    largura_tecido,
    altura_tecido
):

    fig, ax = plt.subplots(
        figsize=(16,9)
    )

    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")

    tecido = patches.Rectangle(
        (0,0),
        largura_tecido,
        altura_tecido,
        fill=False,
        edgecolor="white",
        linewidth=2
    )

    ax.add_patch(tecido)

    for item in colocadas:

        poly = item["poly"]

        coords = np.array(
            poly.exterior.coords
        )

        patch = patches.Polygon(
            coords,
            closed=True,
            facecolor=item["cor"],
            edgecolor="white",
            linewidth=1.2,
            alpha=0.85
        )

        ax.add_patch(patch)

        centro = poly.centroid

        ax.text(
            centro.x,
            centro.y,
            item["nome"],
            ha="center",
            va="center",
            fontsize=7,
            color="white"
        )

    ax.set_xlim(0, largura_tecido)
    ax.set_ylim(0, altura_tecido)
    ax.set_aspect("equal")

    return fig