import seaborn as sns


def style_figure(fig, ax):
    fig.patch.set_facecolor("none")
    ax.set_facecolor("#121924")
    ax.tick_params(colors="#E4F1D1", labelcolor="#E4F1D1")
    ax.spines["bottom"].set_color("#4B4B4B")
    ax.spines["top"].set_color("#4B4B4B")
    ax.spines["left"].set_color("#4B4B4B")
    ax.spines["right"].set_color("#4B4B4B")
    ax.title.set_color("#B4DE8B")
    ax.xaxis.label.set_color("#A8D5A2")
    ax.yaxis.label.set_color("#A8D5A2")
    ax.grid(color="#2F3C4A", linestyle="--", linewidth=0.7, alpha=0.4)
    sns.set_palette(["#00C25A", "#82C462", "#B4DE8B", "#3B7235"])
    fig.tight_layout(pad=1.1)
