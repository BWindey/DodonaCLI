#!/bin/env python3
import click
import http.client

from get_data import *
from pretty_print import *
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
@click.option('--post', '-p', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
              help="Post the contents of a file to Dodona as a solution of the current selected exercise."
                   "Only works if there is a selected exercise.")
@click.option('--up', '-u', is_flag=True,
              help="Go up in the structure by one level depending on where you are. "
                   "Exercise -> serie, serie -> course, course -> top. Use --up-top to immediatly go to the top.")
@click.option('--uptop', is_flag=True,
              help="Go immediatly to the top of the structure.")
@click.option('--status', is_flag=True,
              help="Shows selected course, selected serie and selected exercise.")
def main(display, select, post, up, uptop, status):
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

    sandbox_connection = http.client.HTTPSConnection("sandbox.dodona.be")
    sandbox_headers = {"Autorization": config['TOKEN']}

    if display:
        if config['course_id'] is None:
            # Print available courses
            json_data = courses_data(connection, headers)
            print_courses_data(json_data)

        elif config['serie_id'] is None:
            # Print available series
            json_data = series_data(connection, headers, config['course_id'])
            print_series_data(json_data)

        elif config['exercise_id'] is None:
            # Print available exercises
            json_data = exercises_data(connection, headers, config['serie_id'])
            print_exercise_data(json_data)

        else:
            json_data = exercise_data(connection, headers, config['course_id'], config['exercise_id'])
            print_exercise(json_data, sandbox_connection, sandbox_headers)

    elif select:
        if not select.isNumeric():
            print("I'm sorry, only ID's are allowed. This will improve later.")
            return

        if config['course_id'] is None:
            # Select a course
            course_ids = set(str(course['id']) for course in courses_data(connection, headers))
            if select in course_ids:
                config['course_id'] = select
                select_course(select)
            else:
                print("Not a valid course id!")

        elif config['serie_id'] is None:
            # Select a series
            if select in set(str(series['id']) for series in series_data(connection, headers, config['course_id'])):
                config['serie_id'] = select
                select_serie(select)
            else:
                print("Not a valid series id!")

        elif config['exercise_id'] is None:
            # Select an exercise
            if select in set(str(exercise['id']) for exercise in exercises_data(connection, headers, config['serie_id'])):
                config['exercise_id'] = select
                select_exercise(select)
            else:
                print("Not a valid exercise id!")
        else:
            print('There is already an exercise selected, '
                  'please remove selection with --up or -u to select a new exercise first.')
        dump_config(config)

    elif post:
        if not config['exercise_id']:
            print("No exercise selected!")
        else:
            with open(post, 'r') as infile:
                content = infile.read()
                post_solution(content, connection, headers, config)

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
