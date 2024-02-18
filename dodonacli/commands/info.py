import click

from click_default_group import DefaultGroup
from packaging.version import parse
from pkg_info import get_pkg_info
from rich.markdown import Markdown

from dodonacli.source import pretty_console


@click.group(help="Info about version, update-availability and GitHub page.",
             cls=DefaultGroup, default='version', default_if_no_args=True)
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    dodonacli_version = get_dodonacli_version()

    pretty_console.console.print(
        f"DodonaCLI {dodonacli_version}"
    )


@click.command(help='Checks if there is a new update available for DodonaCLI.')
def check_update():
    dodonacli_version = get_dodonacli_version()

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
    changelog_raw = """
- Added **info** command:
    - Subcommand 'version' to display your current DodonaCLI version. Versions use the YYYY.M.D format.
    - Subcommand 'check-update' lets you know if there is an update available.
    - Subcommand 'github' gives a link to DodonaCLI’s GitHub page.
    - Subcommand 'changelog' shows a changelog for the latest downloaded version.

- Added syntax-check option to **post** command:
  - Use '-c' or '--check' to check syntax. This uses other commandline utilities like shellcheck, javac or python
  - Currently implemented for:
    - Bash
    - Java
    - JavaScript
    - Python

- Added CHANGELOG.md

As always, use the "--help" flag after every command and sub-command to learn more.
    """
    md = Markdown(changelog_raw)
    pretty_console.console.print(md)


def get_dodonacli_version():
    return "2024.02.18.1"


info.add_command(version)
info.add_command(check_update)
info.add_command(github)
info.add_command(changelog)
