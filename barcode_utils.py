import matplotlib.pyplot as plt

def draw_barcode(key):
    fig, ax = plt.subplots(figsize=(6, 2))

    for i, bit in enumerate(key):
        color = "black" if bit == "1" else "white"
        ax.bar(i, 1, color=color, edgecolor="black")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Visualisasi Barcode Kunci B-ENC")

    return fig
