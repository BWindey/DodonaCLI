#!/bin/env python3
import click
import http.client
import os

from courses import *


@click.command(help="A Command Line Interface for Dodona. Finally you have no need to exit your terminal anymore!\n"
                    "Use --help for more info about flags, or read the README on discord.",
               context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--show_courses', '-c',
              help="Show Dodona courses, takes in argument\n"
                   "'m': 'my', \n"
                   "'i': 'institution', \n"
                   "'f': 'featured', \n"
                   "'a': 'all'")
@click.option('--select', '-s',
              help="Select based on name or id. Depends on where in the structure you are. With nothing yet selected, "
                   "this tries to select a course. When a course is selected, you can select a series of exercises, "
                   "and when a serie is selected, you can select an exercise.")
@click.option('--up', '-u', is_flag=True,
              help="Go up in the structure by one level depending on where you are. "
                   "Exercise -> serie, serie -> course, course -> top. Use --up-top to immediatly go to the top.")
@click.option('--uptop', is_flag=True, help="Go immediatly to the top of the structure.")
def main(show_courses, select, up, uptop):
    """
    A Command Line Interface for Dodona. Finally you have no need to exit your terminal anymore!
    Use --help for more info about flags, or read the README on discord.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_directory, 'token')
    try:
        token_file = open(token_path, 'r')
        TOKEN = token_file.read().rstrip('\n')
    except FileNotFoundError:
        TOKEN = input('\033[1;91mToken file not found!\033[0m If it already exists, '
                      'move it to the same directory as the dodonaCLI script, '
                      'else enter your code here: ')
        token_file = open(token_path, 'w')
        token_file.write(TOKEN)
        print('\033[1;92mToken saved.\033[0m\n')
    token_file.close()

    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": TOKEN
    }

    if show_courses:
        show_the_courses(connection, headers, show_courses)

    else:
        print(main.help)


if __name__ == "__main__":
    main()
