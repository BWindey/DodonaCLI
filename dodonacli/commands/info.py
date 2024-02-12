import click

from click_default_group import DefaultGroup
from packaging.version import parse
from pkg_info import get_pkg_info

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
    dodonacli_version = "2023.12.7"

    pkg = get_pkg_info('DodonaCLI')

    if parse(pkg.version) > parse(dodonacli_version):
        pretty_console.console.print(
            f"There is a new version available: {pkg.version}.\n"
            f"You can update your old version ({dodonacli_version}) with"
            "\n\tpip install --upgrade DodonaCLI"
        )
    else:
        print("Your DodonaCLI is up-to-date.")


info.add_command(version)
info.add_command(check_update)
