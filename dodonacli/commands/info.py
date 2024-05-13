import click
from click_default_group import DefaultGroup


@click.group(help="Info about shell-completion, changelog, version, update-availability and GitHub page.",
             cls=DefaultGroup, default='version', default_if_no_args=True)
def info():
    pass


@click.command(help='Display the current version of DodonaCLI. The versioning system '
                    'uses a YYYY.M.D format.')
def version():
    from dodonacli.source import pretty_console
    dodonacli_version = get_dodonacli_version()

    pretty_console.console.print(
        f"DodonaCLI {dodonacli_version}"
    )


@click.command(help='Checks if there is a new update available for DodonaCLI.')
def check_update():
    from packaging.version import parse
    from pkg_info import get_pkg_info
    from dodonacli.source import pretty_console

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


@click.command(help='Bash completion script for you to source in your .bashrc. '
                    'This is a manual script. '
                    'With the optimesed imports, you can also use the completion provided by the Click library '
                    'for bash, zsh and fish. '
                    'Read more about this at https://click.palletsprojects.com/en/8.1.x/shell-completion/')
def completion():
    print(
        """
# Bash completion script for DodonaCLI, needs to be sourced to work
# Used https://www.gnu.org/software/gnuastro/manual/html_node/Bash-TAB-completion-tutorial.html to help create this

# $1 = name of command -> dodona
# $2 = current word being completed
# $3 = word before word being completed

_dodona(){
    if [ "$3" == "sub" ]; then
        COMPREPLY=( $(compgen -W "load display --help" -- "$2")  )

    elif [ "$3" == "display" ]; then
        COMPREPLY=( $(compgen -W "--force --help" -- "$2") )

    elif [ "$3" == "info" ]; then
        COMPREPLY=( $(compgen -W "version changelog completion github check-update" -- "$2"))

    elif [ "$3" == "select" ]; then
        COMPREPLY=( $(compgen -W "--other --hidden --help" -- "$2") )

    elif [ "$3" == "next" ]; then
        COMPREPLY=( $(compgen -W "--reverse --unsolved --help" -- "$2") )

    elif [ "$3" == "dodona" ]; then
        COMPREPLY=( $(compgen -W "display info next post select status sub tutorial up --help" -- "$2") )

    elif [ "$3" == "post" ]; then
        COMPREPLY=( $(compgen -f -- "$2" | grep -vF ".swp") $(compgen -W "--help --use-link -l -c --check" -- "$2" ))

    elif [[ "$3" =~ ^-[lc]+$ ]] || [ "$3" == "--use-link" ] || [ "$3" == "--check" ]; then
        COMPREPLY=( $(compgen -f -- "$2") )

    elif [ "$3" == "up" ]; then
        COMPREPLY=( $(compgen -W "all top 1 2 3" -- "$2") )

    else
        COMPREPLY=( $(compgen -W "--help") )
    fi
}

complete -F _dodona dodona
        """
    )


@click.command(help='Link to the GitHub page of DodonaCLI. Can be handy for the README page, manpages,'
                    ' Issues (bug reports) and pull requests.')
def github():
    from dodonacli.source import pretty_console

    pretty_console.console.print("https://www.github.com/BWindey/DodonaCLI")


@click.command(help='Changelog for the latest version.')
def changelog():
    from rich.markdown import Markdown
    from dodonacli.source import pretty_console

    changelog_raw = """
- Working on rendering feedback. Please report any troubles you have. 
I may not be able to solve them, but I can definitly hide them =D
This is not a full implementation, you should only be able to see which tabs were wrong and wich were correct.

As always, you can use the "--help" flag after every command and sub-command to learn more.
Happy coding!
    """
    md = Markdown(changelog_raw)
    pretty_console.console.print(md)


def get_dodonacli_version():
    from importlib import metadata
    return metadata.version(__package__.split('.')[0])


info.add_command(version)
info.add_command(check_update)
info.add_command(completion)
info.add_command(github)
info.add_command(changelog)
