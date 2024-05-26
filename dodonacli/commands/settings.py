import click
import os


@click.command(help="Interactive settings-menu to change some settings")
def settings():
    from dodonacli.source import menu, get_data

    settings_dict = get_data.get_settings()
    anything_changed = False

    menu_items = [
        "[1] Amount of newlines",
        "[2] Force warning",
        "[3] Display after select",
        "[4] Amount of feedback-items",
        "[5] Amount of submissions",
        "[s] Save and quit",
        "[q] Quit (no save)",
    ]

    selected_index = menu.get_menu_choice(menu_items)

    if selected_index == 0:
        anything_changed = set_amount_newlines(settings_dict)


def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        # ANSI escape codes to clear display, is faster than calling 'clear' with os.system
        print("\033[2J\033[H")


def set_amount_newlines(settings_dict: dict) -> bool:
    """
    Asks the user for new values for new_lines above/below, and returns if the new values are changed
    :param settings_dict:
    :return:
    """
    clear_screen()
    print("Leave field empty if you don't want to change it.")

    print("Amount of newlines above each print, currently: " + settings_dict['new_lines_above'] + "")
    new_lines_above = input("New value: ")
    while new_lines_above != "" and (not new_lines_above.isnumeric() or int(new_lines_above) < 0):
        print("An amount has to be a positive integer!")
        new_lines_above = input("New value: ")

    print("Amount of newlines below each print, currently: " + settings_dict['new_lines_below'] + "")
    new_lines_below = input("New value: ")
    while new_lines_below != "" and (not new_lines_below.isnumeric() or int(new_lines_below) < 0):
        print("An amount has to be a positive integer!")
        new_lines_below = input("New value: ")

    anything_changed = False
    if new_lines_above not in (settings_dict['new_lines_above'], ""):
        settings_dict['new_lines_above'] = int(new_lines_above)
        anything_changed = True

    if new_lines_below not in (settings_dict['new_lines_below'], ""):
        settings_dict['new_lines_below'] = int(new_lines_below)
        anything_changed = False

    return anything_changed
