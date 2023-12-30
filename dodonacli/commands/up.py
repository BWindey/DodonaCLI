import click

from dodonacli.source import set_data
from dodonacli.source import get_data


@click.command(help="Deselect default last selected thing." 
                    "Can be used with an argument to deselect everything with "
                    "'all' or 'top', or deselect 1, 2 or 3 levels.")
@click.argument('amount', default='1',
                type=click.Choice(['all', 'top', '1', '2', '3'], 
                                  case_sensitive=False))
def up(amount):
    # Read configs in
    config = get_data.get_configs()

    if str(amount).lower().strip() in ('all', 'top'):
        for e in ('exercise_id', 'exercise_name', 'serie_id', 'serie_name', 'course_id', 'course_name'):
            config[e] = None
        print("\nDeselected everything.\n")

    elif not isinstance(amount, int) and not amount.isnumeric():
        print("You didn't provide a number or 'all', nothing deselected.")

    else:
        levels = int(amount)
        print()
        for _ in range(levels):
            if config.get('exercise_id') is not None:
                config['exercise_id'] = None
                config['exercise_name'] = None
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
        print()

    set_data.dump_config(config)
