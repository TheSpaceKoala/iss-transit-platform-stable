import math

import matplotlib.pyplot as plt


def create_transit_image(event, filename):
    closest = min(max(event["closest_pos"], 0), 1)

    y = closest

    x_entry = -math.sqrt(max(0, 1 - y**2))
    x_exit = math.sqrt(max(0, 1 - y**2))

    fig, ax = plt.subplots(figsize=(6, 6))

    circle = plt.Circle((0, 0), 1, fill=False, linewidth=3)
    ax.add_patch(circle)

    ax.plot([x_entry, x_exit], [y, y], linewidth=3)
    ax.scatter([0], [y], s=80)

    ax.text(
        0,
        -1.25,
        f"{event['emoji']} {event['name']} - {event['type']}",
        ha="center",
        fontsize=14,
        weight="bold",
    )

    ax.text(
        0,
        -1.40,
        f"Durata {event['duration_seconds']:.1f}s | massimo {event['closest_pos']:.2f} r",
        ha="center",
        fontsize=11,
    )

    ax.set_aspect("equal")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.5, 1.25)
    ax.axis("off")

    plt.savefig(filename, dpi=160, bbox_inches="tight")
    plt.close(fig)
