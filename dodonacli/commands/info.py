import click


@click.group(help="Info about shell-completion, changelog, version, "
                  "update-availability and GitHub page.")
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    from dodonacli.source import pretty_console

    pretty_console.console.print("DodonaCLI " + get_dodonacli_version())


@click.command(help='Checks if there is a new update available for DodonaCLI.')
def check_update():
    from packaging.version import parse
    from pkg_info import get_pkg_info
    from dodonacli.source import pretty_console

    dodonacli_version = get_dodonacli_version()

    pkg = get_pkg_info('DodonaCLI')

    if parse(pkg.version) > parse(dodonacli_version):
        pretty_console.console.print(
            f"\nThere is a new version available: {pkg.version}.\n"
            f"You can update your old version ({dodonacli_version}) with"
            "\n  'pip install --upgrade DodonaCLI'\n"
        )
    else:
        print("\nYour DodonaCLI is up-to-date.\n")


@click.command(help='Tab completion, very handy for fast use')
def completion():
    from dodonacli.source import pretty_console

    pretty_console.console.print(
        "\nThere are 2 ways of doing tab-completion: \n"
        "   - using Click's default tab-completion for bash/zsh/fish\n"
        "   - using DodonaCLI's custom script for bash only\n"
        "\nThe reason there is a custom script, is because the default completion lacks "
        "a bit here and there.\n"
        "The default option is easier to use, and doesn't need a redownload after an update.\n\n"
        "To install the default completion:\n"
        "   Follow this short tutorial:\n"
        "       https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion\n"
        "   Replace every occurence of 'foo-bar' with 'dodona'\n"
        "   Do notice that you can choose how you name the file, and where you put it.\n\n"
        "To install the custom script for bash:\n"
        "   Go to DodonaCLI's GitHub: https://www.github.com/BWindey/DodonaCLI\n"
        "   And download 'dodonacli_completion_script.sh' (at top-level of project structure)\n"
        "   Now add 'source <PATH TO SCRIPT>' to your '.bashrc',\n"
        "   where you fill in the path to the downloaded script."
        "\n\n"
        "For both ways you'll have to either [u yellow]restart your terminal[/], "
        "or re-'source' your .bashrc/.fishrc/...\n"
        "Happy tabbing!\n"
    )


@click.command(help="Link to the GitHub page of DodonaCLI. "
                    "Can be handy for the README page, manpages, Issues (bug reports) and pull requests.")
def github():
    from dodonacli.source import pretty_console

    pretty_console.console.print("\nhttps://www.github.com/BWindey/DodonaCLI\n")


@click.command(help='Changelog for the latest version.')
def changelog():
    from rich.markdown import Markdown
    from dodonacli.source import pretty_console

    changelog_raw = (
        "\n"
        "\t- Reworked tutorial to be more user-friendly, and look a bit better\n"
        "\t- Tweaked some message-endings here and there to be more consistent\n"
        "\t\n"
        "\tAs always, you can use the '--help' flag after every command and sub-command to learn more.\n"
        "\tHappy coding!\n"
    )
    md = Markdown(changelog_raw)
    pretty_console.console.print(md)


@click.command(help='Man-pages for DodonaCLI, very professional')
def man_page():
    from dodonacli.source import pretty_console

    pretty_console.console.print(
        "\n"
        "To install a man-page for DodonaCLI, you can download it from GitHub:\n"
        "  https://www.github.com/BWindey/DodonaCLI\n"
        "The man-page files are located under the 'man-page' directory.\n"
        "Download the .gz version (gzip-compressed), "
        "the other one is not useful unless you want to see how man-pages are written.\n\n"
        "Now run the command 'manpath' in your terminal, this should print a list of "
        "paths, seperated by a ':'\n"
        "Now move the downloaded file to one of those paths.\n"
        "I personally put it onder '~/.local/share/man/man1/'\n"
        "[u yellow]Note[/] that te manual-entry is for 'dodonacli', not 'dodona'\n"
    )


def get_dodonacli_version():
    from importlib import metadata
    return metadata.version(__package__.split('.')[0])


info.add_command(changelog)
info.add_command(check_update)
info.add_command(completion)
info.add_command(github)
info.add_command(man_page)
info.add_command(version)
