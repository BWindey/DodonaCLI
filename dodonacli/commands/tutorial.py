import click


@click.command(help="Start tutorial")
def tutorial():
    from dodonacli.source import set_data, get_data, interactive_tutorial

    config = get_data.get_configs()
    settings = get_data.get_settings()
    config = interactive_tutorial.start_tutorial(config, settings)
    set_data.dump_config(config)
