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
                   "and when a serie is selected, you can select an exercise. When using a name instead of an id, "
                   "the first occurence of that name will be chosen.")
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
    A Command Line Interface for Dodona. Finally, you have no need to exit your terminal anymore!
    Use --help for more info about flags, or read the README on discord.
    """
    # Read configs in
    config = get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    # Start up the connection to Dodona's sandbox (for downloading files and viewing exercise-descriptions)
    sandbox_connection = http.client.HTTPSConnection("sandbox.dodona.be")
    sandbox_headers = {"Autorization": config['TOKEN']}

    # Handle all the different flags
    if display:
        # Display flag changes behaviour depending on the values in the config-dictionary.
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
            # Print exercise-description
            json_data = exercise_data(connection, headers, config['course_id'], config['exercise_id'])
            print_exercise(json_data, sandbox_connection, sandbox_headers)

    elif select:
        if config['course_id'] is None:
            # Select a course
            data_courses = courses_data(connection, headers)

            courses = {str(course['id']): course['name'] for course in data_courses}

            # If select is an id, search if it matches id's, else search if it matches a name, then store the id
            if select.isnumeric() and select in courses:
                config['course_id'] = select
                console.print("Course [bold]" + courses[select] + "[/] selected.")
            else:
                for course in courses.items():
                    if select.lower() in course[1].lower():
                        config['course_id'] = course[0]
                        console.print("\nCourse [bold]\"" + courses[course[0]] + "\"[/] selected.")
                        break
            if config['course_id'] is None:
                print("\nNot a valid course id or -name!\n")

        elif config['serie_id'] is None:
            # Select a series
            data_series = series_data(connection, headers, config['course_id'])

            series = {str(serie['id']): serie['name'] for serie in data_series}

            if select.isnumeric() and select in series:
                config['serie_id'] = select
                console.print("\nSeries [bold]\"" + series[select] + "\"[/] selected.\n")
            else:
                for serie in series.items():
                    if select.lower() in serie[1].lower():
                        config['serie_id'] = serie[0]
                        console.print("\nSerie [bold]\"" + series[serie[0]] + "\"[/] selected.\n")
                        break
            if config['serie_id'] is None:
                print("\nNot a valid series id or -name!\n")

        elif config['exercise_id'] is None:
            # Select an exercise
            data_exercises = exercises_data(connection, headers, config['serie_id'])

            exercises = {str(exercise['id']): (exercise['name'], i) for i, exercise in enumerate(data_exercises)}

            if select.isnumeric() and select in exercises:
                config['exercise_id'] = select
                console.print("\nExercise [bold]\'" + exercises[select] + "\"[/] selected.\n")
            else:
                for exercise in exercises.items():
                    exercise_id, (exercise_name, number) = exercise
                    if select.lower() in exercise_name.lower():
                        config['exercise_id'] = exercise_id
                        console.print("\nExercise [bold]\"" + exercises[exercise_id][0] + "\"[/] selected.\n")
                        boilerplate = data_exercises[number].get("boilerplate")
                        if boilerplate is not None and boilerplate.strip() != "":
                            print("\nBoilerplate code (can be found in boilerplate-file):\n")
                            print(textwrap.indent(boilerplate, '\t'))

                            with open("boilerplate", "w") as boilerplate_file:
                                boilerplate_file.write(boilerplate)
                        break
            if config['exercise_id'] is None:
                print("Not a valid exercise id!")

        else:
            # You can't select more when everything is already selected
            print('There is already an exercise selected, '
                  'please remove selection with --up or -u to select a new exercise first.')

        # Save selections in config file
        dump_config(config)

    elif post:
        # Post exercise to Dodona, does not work if there is no exercise selected
        if not config['exercise_id']:
            print("No exercise selected!")
        else:
            with open(post, 'r') as infile:
                content = infile.read()
            post_solution(content, connection, headers, config)

    elif up:
        # Deselect last selection
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
        # Save selections in config file
        dump_config(config)

    elif uptop:
        # Deselect everything
        config['exercise_id'] = None
        config['serie_id'] = None
        config['course_id'] = None
        print('At the top.')
        # Save selections in config file
        dump_config(config)

    elif status:
        # Print out current selection
        print(f"Status:\n"
              f"\tCourse: {config['course_id']}\n"
              f"\tSerie: {config['serie_id']}\n"
              f"\tExercise: {config['exercise_id']}\n")
        return

    else:
        # No flags specified, print command summary
        print(main.help)


if __name__ == "__main__":
    # Main entry-point
    main()
