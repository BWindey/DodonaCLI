import click


from dodonacli.source import set_data
from dodonacli.source import get_data, interactive_tutorial


@click.command(help="Start tutorial")
def tutorial():
    config = get_data.get_configs()
    config = interactive_tutorial.start_tutorial(config)
    set_data.dump_config(config)
