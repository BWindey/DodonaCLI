import click
import os

from dodonacli.source import pretty_console


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def one():
    print("you have selected menu option one") # Simulate function output.
    input("Press Enter to Continue\n")
    clear_screen()


def reset_to_default():
    pass


def done():
    print("Goodbye")
    sys.exit()


@click.command(help="Some user settings")
def settings():
    clear_screen()

    menu_items = {
        '1': one,
        'reset': reset_to_default,
        'done': done
    }

    while True:
        pretty_console.console.print(
            '\n'.join(key + ': ' + value.replace('_', ' ') for key, value in menu_items.items())
        )
        selection = input("Setting: ")
        if selection in menu_items:
            selected_value = menu_items[selection]  # Gets the function name
            selected_value()


if __name__ == "__main__":
    settings()
