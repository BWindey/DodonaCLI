#!/bin/env python3
import click
import http.client

from get_data import *
from set_data import *


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
@click.option('--status', is_flag=True,
              help="Shows selected course, selected serie and selected exercise.")
def main(display, select, up, uptop, status):
    """
    A Command Line Interface for Dodona. Finally you have no need to exit your terminal anymore!
    Use --help for more info about flags, or read the README on discord.
    """
    config = get_configs()
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
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

    elif select:
        if config['course_id'] is None:
            config['course_id'] = select
            select_course(select)
        elif config['serie_id'] is None:
            config['serie_id'] = select
            select_serie(select)
        elif config['exercise_id'] is None:
            config['exercise_id'] = select
            select_exercise(select)
        else:
            print('There is already an exercise selected, '
                  'please remove selection with --up or -u to select a new exercise first.')
        dump_config(config)

    elif up:
        if config['exercise_id']:
            config['exercise_id'] = None
            print('Deselected exercise.')
        elif config['serie_id']:
            config['serie_id'] = None
            print('Deselected serie.')
        elif config['course_id']:
            config['course_id'] = None
            print('Deselected course.')
        else:
            print('Already at the top.')
        dump_config(config)

    elif uptop:
        config['exercise_id'] = None
        config['serie_id'] = None
        config['course_id'] = None
        print('At the top.')
        dump_config(config)

    elif status:
        print(f"Status:\n"
              f"\tCourse: {config['course_id']}\n"
              f"\tSerie: {config['serie_id']}\n"
              f"\tExercise: {config['exercise_id']}\n")
        return

    else:
        print(main.help)


if __name__ == "__main__":
    main()
