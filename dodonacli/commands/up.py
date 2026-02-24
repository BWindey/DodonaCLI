import click


@click.command(
    help="Deselect default last selected thing. "
    "Can be used with an argument to deselect everything with "
    "'all' or 'top', or deselect 1, 2 or 3 levels."
)
@click.argument(
    'amount', default='1',
    type=click.Choice(['all', 'top', '1', '2', '3'], case_sensitive=False)
)
def up(amount):
    from dodonacli.source import set_data, get_data
    from dodonacli.source.pretty_printer import custom_print

    # Read configs in
    config = get_data.get_configs()
    settings = get_data.get_settings()

    # Click handles all the edge cases, we can just assume it's a valid string
    if amount in ('all', 'top'):
        keys_to_remove = (
            "course_id", "course_name",
            "serie_id", "serie_name",
            "exercise_id", "exercise_name",
            "serie_token", "programming_language"
        )
        for e in keys_to_remove:
            config[e] = None

        custom_print("Deselected everything.", settings)

    else:
        levels = int(amount)
        string_to_print = ""
        for _ in range(levels):
            if config.get('exercise_id') is not None:
                config['exercise_id'] = None
                config['exercise_name'] = None
                config['programming_language'] = None
                string_to_print += "Deselected exercise.\n"
            elif config.get('serie_id') is not None:
                config['serie_id'] = None
                config['serie_name'] = None
                config['serie_token'] = None
                string_to_print += "Deselected series.\n"
            elif config.get('course_id') is not None:
                config['course_id'] = None
                config['course_name'] = None
                string_to_print += "Deselected course.\n"
            else:
                string_to_print += "Nothing selected.\n"
                break
        custom_print(string_to_print, settings, end='')

    set_data.dump_config(config)
