import click

from dodonacli.source import pretty_print, get_data


@click.command(help="Display your current selection. Selected course, series and exercise.")
def status():
    # Read configs in
    config = get_data.get_configs()

    pretty_print.print_status(config)
