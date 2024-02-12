import click
import os
import tomli

from click_default_group import DefaultGroup

from dodonacli.source import pretty_console


@click.group(help="Info about version, update-availability and GitHub page.",
             cls=DefaultGroup, default='version', default_if_no_args=True)
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    # Get the path of the toml-file.
    # This is a bit more complicated because this file exists in the same directory as
    # the python files, but the command may be executed from anywhere with the appropriate alias set.
    # Thus, first the path to the directory of the python files is retrieved; then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    toml_file_path = os.path.join(script_directory, '../../pyproject.toml')

    with open(toml_file_path, 'rb') as toml_file:
        toml_dict = tomli.load(toml_file)

    dodonacli_version = toml_dict['project']['version']

    pretty_console.console.print(
        f"DodonaCLI {dodonacli_version}"
    )


info.add_command(version)
