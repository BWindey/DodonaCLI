import click

from dodonacli.commands import select, status, up, post
from dodonacli.commands import tutorial, submission, display


@click.group(help="A 3rd party Command Line Interface for Dodona. "
                  "Finally you have no need to exit your terminal anymore!\n"
                  "Use --help for more info about flags, or read the README on discord.")
def main():
    """
    A Command Line Interface for Dodona. Finally, you have no need to exit your terminal anymore!
    Use --help for more info about flags, or read the README on discord.
    """
    pass


main.add_command(display.display)
main.add_command(select.select)
main.add_command(status.status)
main.add_command(up.up)
main.add_command(post.post)
main.add_command(tutorial.tutorial)
main.add_command(submission.sub)


if __name__ == "__main__":
    # Main entry-point
    main()

