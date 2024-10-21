import click


@click.command(help="Show where to edit settings")
def settings():
    from dodonacli.source import get_data
    import os

    settings_file_path = os.path.join(get_data.get_config_home(), "settings.json")

    print(f"You can edit the settings in {settings_file_path}")

