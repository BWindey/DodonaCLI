import click

from source import handle_flags, get_data


@click.command(help="Display current selection")
def status():
    # Read configs in
    config = get_data.get_configs()

    handle_flags.handle_status(config)
