from core.settings import get_settings
from core.telegram_commands import build_telegram_command_menu
from core.telegram_utils import set_telegram_commands


def main():
    set_telegram_commands(build_telegram_command_menu(get_settings()))


if __name__ == "__main__":
    main()
