import os

from core.settings import get_settings
from core.astronomy import find_events, group_best
from core.i18n import t
from core.messages import build_message, build_photo_caption
from core.telegram_utils import (
    get_telegram_credentials,
    has_telegram_credentials,
    send_telegram,
    send_telegram_photo,
)
from core.graphics import create_transit_image


def execute_transit_run(settings, chat_id=None):
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

    send_telegram(message, chat_id=chat_id)

    grouped_transits = group_best(transits, 60)

    for i, event in enumerate(grouped_transits, 1):
        filename = f"transit_{i}.png"

        try:
            create_transit_image(event, filename, settings)

            caption = build_photo_caption(settings, event)

            send_telegram_photo(filename, caption, chat_id=chat_id)
        finally:
            if os.path.exists(filename):
                os.remove(filename)


def main():
    settings = None

    try:
        settings = get_settings()
        get_telegram_credentials()
        execute_transit_run(settings)

    except Exception as error:
        error_message = t(
            settings,
            "runtime.error",
            error_type=type(error).__name__,
            error=error,
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
