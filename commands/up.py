import click

from source import handle_flags, get_data


@click.command(help="Deselect something")
@click.argument('amount', default='1')
def up(amount):
    # Read configs in
    config = get_data.get_configs()

    if amount.strip() == '1':
        handle_flags.handle_up(config)
    elif amount.strip() == '2':
        handle_flags.handle_up(config)
        handle_flags.handle_up(config)
    else:
        handle_flags.handle_uptop(config)
