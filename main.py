#!/bin/env python3
import click

from commands import display


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


if __name__ == "__main__":
    # Main entry-point
    main()
