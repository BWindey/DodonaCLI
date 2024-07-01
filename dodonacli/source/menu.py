"""
Blatenly stolen from https://github.com/cornradio/dumb_menu
And adapted to my needs.
"""
import os
import re

if os.name != 'nt':
    import sys
    import tty
    import termios


    def get_key() -> str:
        return get_key_getch()

else:
    import msvcrt


    def get_key() -> str:
        return get_key_msvcrt()


def get_key_getch() -> str:  # get keypress using getch, msvcrt = windows
    """
    Get pressed key using getch
    :return: pressed key
    """
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)

    try:
        tty.setraw(file_descriptor)
        first_char = sys.stdin.read(1)

        if first_char == '\x1b':    # arrow keys
            sys.stdin.read(1)       # will be '[' charachter for arrow key
            b = sys.stdin.read(1)   # actual ABCD character
            return {'A': 'up', 'B': 'down', 'C': 'right', 'D': 'left'}[b]
        if ord(first_char) in (10, 13):
            return 'enter'
        if first_char == '\x0e':
            return 'down'
        if first_char == '\x10':
            return 'up'
        else:
            # normal keys like abcd 1234
            return first_char
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)


def get_key_msvcrt() -> str:
    """
    Get pressed key using msvcrt
    :return: pressed key
    """
    key = msvcrt.getch()  # get keypress
    if key == b'\x1b':  # Esc key to exit
        return 'esc'
    elif key == b'\r':  # Enter key to select
        return 'enter'
    elif key == b'\x48':  # Up or Down arrow
        return 'up'
    elif key == b'\x50':  # Up or Down arrow
        return 'down'
    else:
        return key.decode('utf-8')


def get_menu_choice(options: list[str], title: str = "", body: str = "", start_index: int = 0) -> int:
    """
    Display a menu, and return the chosen option index
    :param options: list of strings with the options to display
    :param title: title of the menu to display above
    :param body: piece of text to display between the title and the menu
    :param start_index: index to put the '> ' next to in the beginning
    :return: chose option index, as found in the options-list
    """
    selected_index = start_index
    shortcuts = scan_short_cuts(options)
    show_menu(options, selected_index, title)
    key = get_key()

    while key not in shortcuts and key != 'enter':
        if key in ('up', 'down'):  # Up or Down arrow
            selected_index = (selected_index + (1 if key == 'down' else -1) + len(options)) % len(options)
        show_menu(options, selected_index, title, body)
        key = get_key()

    return shortcuts.get(key, selected_index)


def scan_short_cuts(options: list[str]) -> dict[str, int]:
    """
    Build up dictionary with the short-cut key for each option
    :param options: list of strings with the options to display
    :return: dictionary mapping shortcut on index
    """
    shortcuts = {}
    for i, option in enumerate(options):
        match = re.match(r"\[(.*)](.*)", option)
        if match:
            shortcut = match.group(1)
            shortcuts[shortcut] = i

    return shortcuts


def show_menu(options: list[str], selected_index: int, title: str, body: str):
    """
    Print out the actual menu
    :param options: list of strings with the menu-itmes
    :param selected_index: index of where cursor is now
    :param title: title to display above the options
    :param body: piece of text to display between the title and the menu
    """
    if os.name == 'nt':
        os.system("cls")
        result = title + '\n' * (len(title.strip()) > 0) + body + '\n' * (len(body.strip()) > 0)
    else:
        # ANSI escape codes to clear display, is faster than calling 'clear' with os.system
        result = "\033[2J\033[H" + title + '\n' * (len(title.strip()) > 0) + body + '\n' * (len(body.strip()) > 0)

    result += '\n'.join(
        f"{'>' * (selected_index == i)} {option}"
        for i, option in enumerate(options)
    )
    print(result)


# test code
if __name__ == "__main__":
    menu_items = ["[1] Option 1", "[2] Option 2", "[3] Option 3", "[q] Quit"]
    index = get_menu_choice(menu_items)

    if index != -1:
        print(f"You selected option {index + 1}: {menu_items[index]}")
    else:
        print("You exited the menu.")
