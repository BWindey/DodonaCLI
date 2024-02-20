import click


@click.command(help="Display your current selection. Selected course, series and exercise.")
def status():
    from dodonacli.source import pretty_print, get_data

    # Read configs in
    config = get_data.get_configs()

    pretty_print.print_status(config)
