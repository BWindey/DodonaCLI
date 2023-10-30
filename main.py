#!/bin/env python3
import click
import http.client
import os

from get_data import *
from set_data import *

selected = {'course_id': None, 'serie_id': None, 'exercise_id': None}


@click.command(help="A Command Line Interface for Dodona. Finally you have no need to exit your terminal anymore!\n"
                    "Use --help for more info about flags, or read the README on discord.",
               context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--display', '-d', is_flag=True,
              help="Display info based on what is already selected. If no course is yet selected, it gives a list of "
                   "courses to select from, if no serie or exercise is selected, idem")
@click.option('--select', '-s',
              help="Select based on name or id. Depends on where in the structure you are. With nothing yet selected, "
                   "this tries to select a course. When a course is selected, you can select a series of exercises, "
                   "and when a serie is selected, you can select an exercise.")
@click.option('--up', '-u', is_flag=True,
              help="Go up in the structure by one level depending on where you are. "
                   "Exercise -> serie, serie -> course, course -> top. Use --up-top to immediatly go to the top.")
@click.option('--uptop', is_flag=True,
              help="Go immediatly to the top of the structure.")
def main(display, select, up, uptop):
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

    if display:
        json_data = courses_data(connection, headers)
        courses = []
        for course in json_data:
            courses.append((str(course['id']), course['name'], course['teacher']))
        max_course_id_length = max(len(e[0]) for e in courses)
        max_course_name_length = max(len(e[1]) for e in courses)
        courses = sorted(courses, key=lambda x: x[1])

        print('\033[4;94mYour courses:\033[0m')
        for e in courses:
            print(f'{e[0].ljust(max_course_id_length)}: \033[1m{e[1].ljust(max_course_name_length)}\033[0m\tby {e[2]}')

        return

    if select:
        if selected['course_id'] is not None:
            select_course()
            return
        if selected['serie_id'] is not None:
            select_serie()
            return
        if selected['exercise_id'] is not None:
            select_exercise()
            return
        print('There is already an exercise selected, '
              'please remove selection with --up or -u to select a new exercise first.')
        return

    if up:
        if selected['exercise_id']:
            selected['exercise_id'] = None
            print('Deselected exercise.')
        elif selected['serie_id']:
            selected['serie_id'] = None
            print('Deselected serie.')
        elif selected['course_id']:
            selected['course_id'] = None
            print('Deselected course.')
        else:
            print('Already at the top.')
        return

    if uptop:
        selected['exercise_id'] = None
        selected['serie_id'] = None
        selected['course_id'] = None
        print('At the top.')
        return

    else:
        print(main.help)


if __name__ == "__main__":
    main()
