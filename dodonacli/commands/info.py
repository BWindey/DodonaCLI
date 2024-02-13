import click
import os

from click_default_group import DefaultGroup
from packaging.version import parse
from pkg_info import get_pkg_info
from rich.markdown import Markdown

from dodonacli.source import get_data, pretty_console


@click.group(help="Info about version, update-availability and GitHub page.",
             cls=DefaultGroup, default='version', default_if_no_args=True)
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    dodonacli_version = get_data.get_dodonacli_version()

    pretty_console.console.print(
        f"DodonaCLI {dodonacli_version}"
    )


@click.command(help='Checks if there is a new update available for DodonaCLI.')
def check_update():
    dodonacli_version = get_data.get_dodonacli_version()

    pkg = get_pkg_info('DodonaCLI')

    if parse(pkg.version) > parse(dodonacli_version):
        pretty_console.console.print(
            f"There is a new version available: {pkg.version}.\n"
            f"You can update your old version ({dodonacli_version}) with"
            "\n\tpip install --upgrade DodonaCLI"
        )
    else:
        print("Your DodonaCLI is up-to-date.")


@click.command(help='Link to the GitHub page of DodonaCLI. Can be handy for the README page, Issues (bug reports) and '
                    'pull requests.')
def github():
    pretty_console.console.print("https://www.github.com/BWindey/DodonaCLI")


@click.command(help='Changelog for the latest version.')
def changelog():
    # Get the path of the toml-file.
    # This is a bit more complicated because this file exists in the same directory as
    # the python files, but the command may be executed from anywhere with the appropriate alias set.
    # Thus, first the path to the directory of the python files is retrieved; then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    changelog_path = os.path.join(script_directory, '../../CHANGELOG.md')

    with open(changelog_path, 'r') as changelog_file:
        md = Markdown(changelog_file.read())

    pretty_console.console.print(md)


info.add_command(version)
info.add_command(check_update)
info.add_command(github)
info.add_command(changelog)
