import click


@click.command(help="Deselect default last selected thing. " 
                    "Can be used with an argument to deselect everything with "
                    "'all' or 'top', or deselect 1, 2 or 3 levels.")
@click.argument('amount', default='1',
                type=click.Choice(['all', 'top', '1', '2', '3'], 
                                  case_sensitive=False))
def up(amount):
    from dodonacli.source import set_data, get_data

    # Read configs in
    config = get_data.get_configs()
    settings = get_data.get_settings()

    if str(amount).lower().strip() in ('all', 'top'):
        for e in ('exercise_id', 'exercise_name', 'serie_id', 'serie_name', 'serie_token', 'course_id', 'course_name'):
            config[e] = None
        print(
            '\n' * settings['new_lines_above']
            + "Deselected everything."
            + "\n" * settings['new_lines_below']
        )

    elif not isinstance(amount, int) and not amount.isnumeric():
        print(
            '\n' * settings['new_lines_above']
            + "You didn't provide a number or 'all', nothing deselected."
            + "\n" * settings['new_lines_below']
        )

    else:
        levels = int(amount)
        print('\n' * settings['new_lines_above'], end='')
        for _ in range(levels):
            if config.get('exercise_id') is not None:
                config['exercise_id'] = None
                config['exercise_name'] = None
                config['programming_language'] = None
                print("Deselected exercise.")
            elif config.get('serie_id') is not None:
                config['serie_id'] = None
                config['serie_name'] = None
                config['serie_token'] = None
                print("Deselected series.")
            elif config.get('course_id') is not None:
                config['course_id'] = None
                config['course_name'] = None
                print("Deselected course")
            else:
                print("Nothing selected.")
                break
        print('\n' * settings['new_lines_below'], end='')

    set_data.dump_config(config)
