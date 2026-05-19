import math

import matplotlib.pyplot as plt

from core.i18n import body_label, localized_event_type, t


def create_transit_image(event, filename, settings=None):
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
        (
            f"{event['emoji']} {body_label(settings, event['name'])} - "
            f"{localized_event_type(settings, event['type'])}"
        ),
        ha="center",
        fontsize=14,
        weight="bold",
    )

    ax.text(
        0,
        -1.40,
        t(
            settings,
            "graphics.duration_line",
            duration=f"{event['duration_seconds']:.1f}",
            closest=f"{event['closest_pos']:.2f}",
        ),
        ha="center",
        fontsize=11,
    )

    ax.set_aspect("equal")
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.5, 1.25)
    ax.axis("off")

    plt.savefig(filename, dpi=160, bbox_inches="tight")
    plt.close(fig)
