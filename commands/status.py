import click

from source import get_data, pretty_print


@click.command(help="Display your current selection. Selected course, series and exercise.")
def status():
    # Read configs in
    config = get_data.get_configs()

    pretty_print.print_status(config)
