import textwrap

from . import pretty_print, get_data, set_data
from . import pretty_console


def handle_display(config, connection, headers):
    # Display flag changes behaviour depending on the values in the config-dictionary.
    if config['course_id'] is None:
        # Print available courses
        json_data = get_data.courses_data(connection, headers)
        pretty_print.print_courses_data(json_data)

    elif config['serie_id'] is None:
        # Print available series
        json_data = get_data.series_data(connection, headers, config['course_id'])
        pretty_print.print_series_data(json_data)

    elif config['exercise_id'] is None:
        # Print available exercises
        json_data = get_data.exercises_data(connection, headers, config['serie_id'])
        pretty_print.print_exercise_data(json_data)

    else:
        # Print exercise-description
        json_data = get_data.exercise_data(connection, headers, config['course_id'], config['exercise_id'])
        pretty_print.print_exercise(json_data)


def handle_select(select, config, connection, headers):
    if config['course_id'] is None:
        # Select a course
        data_courses = get_data.courses_data(connection, headers)

        courses = {str(course['id']): course['name'] for course in data_courses}

        # If select is an id, search if it matches id's, else search if it matches a name, then store the id
        if select.isnumeric() and select in courses:
            config['course_id'] = select
            config['course_name'] = courses[select]
            pretty_console.console.print("\nCourse [bold]" + courses[select] + "[/] selected.\n")
        else:
            for course in courses.items():
                if select.lower() in course[1].lower():
                    config['course_id'] = course[0]
                    config['course_name'] = course[1]
                    pretty_console.console.print("\nCourse [bold]\"" + courses[course[0]] + "\"[/] selected.\n")
                    break
        if config['course_id'] is None:
            print("\nNot a valid course id or -name!\n")

    elif config['serie_id'] is None:
        # Select a series
        data_series = get_data.series_data(connection, headers, config['course_id'])

        series = {str(serie['id']): serie['name'] for serie in data_series}

        if select.isnumeric() and select in series:
            config['serie_id'] = select
            config['serie_name'] = series[select]
            pretty_console.console.print("\nSeries [bold]\"" + series[select] + "\"[/] selected.\n")
        else:
            for serie in series.items():
                if select.lower() in serie[1].lower():
                    config['serie_id'] = serie[0]
                    config['serie_name'] = serie[1]
                    pretty_console.console.print("\nSerie [bold]\"" + series[serie[0]] + "\"[/] selected.\n")
                    break
        if config['serie_id'] is None:
            print("\nNot a valid series id or -name!\n")

    elif config['exercise_id'] is None:
        # Select an exercise
        data_exercises = get_data.exercises_data(connection, headers, config['serie_id'])

        exercises = {str(exercise['id']): (exercise['name'], i) for i, exercise in enumerate(data_exercises)}

        if select.isnumeric() and select in exercises:
            config['exercise_id'] = select
            config['exercise_name'] = exercises[select]
            pretty_console.console.print("\nExercise [bold]\'" + exercises[select] + "\"[/] selected.\n")
        else:
            for exercise in exercises.items():
                exercise_id, (exercise_name, number) = exercise
                if select.lower() in exercise_name.lower():
                    config['exercise_id'] = exercise_id
                    config['exercise_name'] = exercise_name
                    pretty_console.console.print("\nExercise [bold]\"" + exercises[exercise_id][0] + "\"[/] selected.\n")
                    boilerplate = data_exercises[number].get("boilerplate")
                    if boilerplate is not None and boilerplate.strip() != "":
                        print("\nBoilerplate code (can be found in boilerplate-file):\n")
                        print(textwrap.indent(boilerplate, '\t'))

                        with open("../boilerplate", "w") as boilerplate_file:
                            boilerplate_file.write(boilerplate)
                    break

        if config['exercise_id'] is None:
            print("Not a valid exercise id!")

    else:
        # You can't select more when everything is already selected
        print('There is already an exercise selected, '
              'please remove selection with --up or -u to select a new exercise first.')

    # Save selections in config file
    set_data.dump_config(config)


def handle_post(post, config, connection, headers):
    # Post exercise to Dodona, does not work if there is no exercise selected
    if not config['exercise_id']:
        print("No exercise selected!")
    else:
        with open(post, 'r') as infile:
            content = infile.read()
        set_data.post_solution(content, connection, headers, config)


def handle_up(config):
    # Deselect last selection
    if config['exercise_id']:
        config['exercise_id'] = None
        config['exercise_name'] = None
        print('Deselected exercise.')
    elif config['serie_id']:
        config['serie_id'] = None
        config['serie_name'] = None
        print('Deselected serie.')
    elif config['course_id']:
        config['course_id'] = None
        config['course_name'] = None
        print('Deselected course.')
    else:
        print('Already at the top.')
    # Save selections in config file
    set_data.dump_config(config)


def handle_uptop(config):
    # Deselect everything
    config['exercise_id'] = None
    config['exercise_name'] = None
    config['serie_id'] = None
    config['serie_name'] = None
    config['course_id'] = None
    config['course_name'] = None
    print('At the top.')
    # Save selections in config file
    set_data.dump_config(config)


def handle_status(config):
    # Print out current selection
    pretty_print.print_status(config)
