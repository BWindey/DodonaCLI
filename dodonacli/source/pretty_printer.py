from . import pretty_console


def custom_print(text: str, settings: dict, pretty: bool = False):
    """
    Prints out the text with the amount of newlines specified in settings
    :param text: text to print
    :param settings: dict with settings
    :param pretty: whether to use the pretty_console print, or the standard Python print
    """
    if pretty:
        printer = pretty_console.console.print
    else:
        printer = print

    printer(
        '\n' * settings.get('new_lines_above', 0)
        + text
        + '\n' * settings.get('new_lines_below', 0)
    )
