import click


from source import interactive_tutorial, get_data, set_data


@click.command(help="Start tutorial")
def tutorial():
    config = get_data.get_configs()
    config = interactive_tutorial.start_tutorial(config)
    set_data.dump_config(config)
