"""
Blatenly stolen from https://github.com/cornradio/dumb_menu
And adapted to my needs.
"""
import os
import re


def get_key():  # get keypress using getch, msvcrt = windows
    try:
        import getch

        first_char = getch.getch()
        if first_char == '\x1b':  # arrow keys
            a = getch.getch()
            b = getch.getch()
            return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[a + b]
        if ord(first_char) == 10:
            return 'enter'
        if ord(first_char) == 32:
            return 'space'
        else:
            # normal keys like abcd 1234
            return first_char

    except ImportError:
        try:
            import msvcrt

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
        except ImportError:
            print("Failed to get input, both getch (Unix) and msvcrt (Windows) don't get imported")
            exit(1)


def get_menu_choice(options: list[str]):
    """
    Display a menu, and return the chosen option index
    :param options: list of strings with the options to display
    :return: chose option index, as found in the options-list
    """
    selected_index = 0
    shortcuts = scan_short_cuts(options)
    show_menu(options, selected_index)
    key = get_key()

    while key not in shortcuts and key != 'enter':
        show_menu(options, selected_index)
        key = get_key()
        if key in ('up', 'down'):  # Up or Down arrow
            selected_index = (selected_index + (1 if key == 'down' else -1) + len(options)) % len(options)
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


def show_menu(options: list[str], selected_index: int):
    """
    Print out the actual menu
    :param options: list of strings with the menu-itmes
    :param selected_index: index of where cursor is now
    """
    if os.name == 'nt':
        os.system("cls")
        result = ""
    else:
        # ANSI escape codes to clear display, is faster than calling 'clear' with os.system
        result = "\033[2J\033[H"

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
