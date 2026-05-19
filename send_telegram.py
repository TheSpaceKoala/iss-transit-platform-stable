import os

from core.settings import get_settings
from core.astronomy import find_events, group_best
from core.messages import build_message
from core.telegram_utils import (
    get_telegram_credentials,
    has_telegram_credentials,
    send_telegram,
    send_telegram_photo,
)
from core.graphics import create_transit_image


def main():
    try:
        settings = get_settings()
        get_telegram_credentials()

        transits, close_approaches, stats, diagnostics = find_events(
            settings
        )

        message = build_message(
            settings,
            transits,
            close_approaches,
            stats,
            diagnostics,
        )

        send_telegram(message)

        grouped_transits = group_best(transits, 60)

        for i, event in enumerate(grouped_transits, 1):
            filename = f"transit_{i}.png"

            try:
                create_transit_image(event, filename)

                caption = (
                    f"{event['satellite_emoji']} "
                    f"{event['satellite_name']} → "
                    f"{event['emoji']} {event['name']} | "
                    f"{event['type']} | "
                    f"{event['duration_seconds']:.1f} s"
                )

                send_telegram_photo(filename, caption)
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

    except Exception as error:
        error_message = (
            "🚨 ISS Transit Bot\n\n"
            "Errore durante l'esecuzione.\n\n"
            f"Dettaglio:\n{type(error).__name__}: {error}"
        )

        if has_telegram_credentials():
            try:
                send_telegram(error_message)
            except Exception as telegram_error:
                print(
                    "Impossibile inviare la notifica di errore su Telegram: "
                    f"{type(telegram_error).__name__}: {telegram_error}"
                )
                print(error_message)
        else:
            print(error_message)

        raise


if __name__ == "__main__":
    main()
