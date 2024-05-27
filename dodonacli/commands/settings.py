import click
import os


@click.command(help="Interactive settings-menu to change some settings")
def settings():
    from dodonacli.source import menu, get_data, set_data

    settings_dict = get_data.get_settings()
    anything_changed = False

    menu_items = [
        "[1] Amount of newlines",
        "[2] Force warning",
        "[3] Display after select",
        "[4] Amount of feedback-items",
        "[5] Amount of submissions",
        "[r] Restore to default",
        "[q] Quit (no save)",
        "[s] Save and Quit",
    ]
    menu_actions = [
        set_amount_newlines,
        set_force_warning,
        set_display_after_select,
        set_amount_feedback_items,
        set_amount_submissions
    ]
    selected_index = 0

    while True:
        selected_index = menu.get_menu_choice(menu_items, title="DodonaCLI settings", start_index=selected_index)

        if selected_index == len(menu_items) - 1:
            if anything_changed:
                set_data.dump_settings(settings_dict)
            print("Settings saved")
            break

        elif selected_index == len(menu_items) - 2:
            if anything_changed:
                print("Are you sure you want to quit without saving?")
                answer = input("[y/N]: ")
                if answer.lower().startswith("y"):
                    break
            else:
                break

        elif selected_index == len(menu_items) - 3:
            print("Are you sure you want to restore all the settings to their defaults?")
            answer = input("[y/N]: ")
            if answer.lower().startswith("y"):
                set_data.dump_settings({})
                print("Settings restored to their defaults")
                break

        elif selected_index < len(menu_items) - 3 and menu_actions[selected_index](settings_dict):
            anything_changed = True
            menu_items[selected_index] += " (*)"


def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        # ANSI escape codes to clear display, is faster than calling 'clear' with os.system
        print("\033[2J\033[H", end='')


def set_amount_newlines(settings_dict: dict) -> bool:
    """
    Asks the user for new values for new_lines above/below, and returns if the new values are changed
    :return: if the new value differs from the original
    """
    clear_screen()
    print("Leave field empty if you don't want to change it.")

    settings_to_change = [
        'new_lines_above',
        'new_lines_below'
    ]
    anything_changed = False

    for setting in settings_to_change:
        if ask_about_setting(
                settings_dict, setting,
                lambda x: x.isnumeric() and int(x) > 0, int,
                text="Amount of " + setting.replace("_", " ")
        ):
            anything_changed = True

    return anything_changed


def set_force_warning(settings_dict: dict) -> bool:
    """
    Asks the user for whether to display the force warning message
    :return: if the new value differs from the original
    """
    clear_screen()
    print("Leave field empty if you don't want to change it.")

    return ask_about_setting_boolean(
        settings_dict,
        'paste_force_warning',
        "Print a warning when using the --force flag to display an exercise"
    )


def set_display_after_select(settings_dict: dict) -> bool:
    settings_to_change = [
        'display_series_after_select',
        'display_exercises_after_select',
        'display_exercise_after_select'
    ]
    anything_changed = False

    for setting in settings_to_change:
        if ask_about_setting_boolean(settings_dict, setting):
            anything_changed = True

    return anything_changed


def set_amount_feedback_items(settings_dict: dict) -> bool:
    clear_screen()
    print("Leave field empty if you don't want to change it, set value to -1 for no upper limit")

    settings_to_change = [
        'amount_feedback_context',
        'amount_feedback_tab',
        'amount_feedback_testcase',
        'amount_feedback_test'
    ]
    anything_changed = False

    for setting in settings_to_change:
        if ask_about_setting(
            settings_dict, setting,
            lambda x: x.isnumeric() and (int(x) > 0 or int(x) == -1), int,
            text="Amount of " + setting.split("_")[-1] + "s showed in feedback"
        ):
            anything_changed = True

    return anything_changed


def set_amount_submissions(settings_dict: dict) -> bool:
    clear_screen()
    print("Leave field empty if you don't want to, set value to -1 for no upper limit")

    settings_to_change = [
        'amount_sub_exercise',
        'amount_sub_global'
    ]
    anything_changed = False

    for setting in settings_to_change:
        if ask_about_setting(
            settings_dict, setting,
            lambda x: x.isnumeric() and (int(x) > 0 or int(x) == -1), int,
            text="Amount of submissions showed for " + setting.split("_")[-1]
        ):
            anything_changed = True

    return anything_changed


def ask_about_setting(settings_dict: dict, setting: str, is_valid, setting_type: type, text: str = None,
                      warning: str = "") -> bool:
    """
    Standardized way to ask user for setting
    :param settings_dict: dictionary with the settings
    :param setting: setting to change in the settings dictionary
    :param is_valid: function to check if the new value is valid
    :param setting_type: variable-type for the setting (bool, int, float, ...)
    :param text: custom text to display, by default it uses the setting (capitalized, and '_' -> ' ')
    :param warning: custom text to display when the user enters an invalid new value
    :return: whether the new value of the setting is different from the old
    """
    if text is None:
        text = setting.capitalize().replace("_", " ")

    text += f", currently: {settings_dict[setting]}"

    print("\u00B7 " + text)
    new_value = input("    New value: ")
    while new_value != "" and not is_valid(new_value):
        print(warning)
        new_value = input("New value: ")

    if new_value not in (settings_dict[setting], ""):
        settings_dict['new_lines_above'] = setting_type(new_value)
        return True
    return False


def ask_about_setting_boolean(settings_dict: dict, setting: str, title: str = None, body: str = None) -> bool:
    """
    Standardized way to ask user for boolean setting, using a menu
    :param settings_dict: dictionary with the settings
    :param setting: setting to change in the settings dictionary
    :param title: custom text to display, by default it uses the setting (capitalized, and '_' -> ' ')
    :return: whether the new value of the setting is different from the old
    """
    from dodonacli.source import menu

    if title is None:
        title = setting.capitalize().replace("_", " ")
    if body is None:
        body = f"Currently: {settings_dict[setting]}"

    choice = menu.get_menu_choice(
        ["[t] True", "[f] False"],
        title=title,
        body=body
    )

    choice = choice == 0
    if choice != settings_dict[setting]:
        settings_dict[setting] = choice
        return True

    return False
