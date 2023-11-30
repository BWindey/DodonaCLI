import click
import http.client
import textwrap

from dodonacli.source import set_data
from dodonacli.source import pretty_console, get_data


@click.command(help="Select based on id or name. Depends on current selection. If nothing is selected, "
                    "it will try to select a course, then an exercise-series, then an exercise. Will not work "
                    "with invalid id's or names.")
@click.argument('thing')
def select(thing):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    if config['course_id'] is None:
        # Select a course
        data_courses = get_data.courses_data(connection, headers)

        courses = {str(course['id']): course['name'] for course in data_courses}

        # If select is an id, search if it matches id's, else search if it matches a name, then store the id
        if thing.isnumeric() and thing in courses:
            config['course_id'] = thing
            config['course_name'] = courses[thing]
            pretty_console.console.print("\nCourse [bold]" + courses[thing] + "[/] selected.\n")
        else:
            for course in courses.items():
                if thing.lower() in course[1].lower():
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

        if thing.isnumeric() and thing in series:
            config['serie_id'] = thing
            config['serie_name'] = series[thing]
            pretty_console.console.print("\nSeries [bold]\"" + series[thing] + "\"[/] selected.\n")
        else:
            for serie in series.items():
                if thing.lower() in serie[1].lower():
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

        if thing.isnumeric() and thing in exercises:
            config['exercise_id'] = thing
            config['exercise_name'] = exercises[thing]
            pretty_console.console.print("\nExercise [bold]\'" + exercises[thing] + "\"[/] selected.\n")
        else:
            for exercise in exercises.items():
                exercise_id, (exercise_name, number) = exercise
                if thing.lower() in exercise_name.lower():
                    config['exercise_id'] = exercise_id
                    config['exercise_name'] = exercise_name
                    pretty_console.console.print(
                        "\nExercise [bold]\"" + exercises[exercise_id][0] + "\"[/] selected.\n")
                    boilerplate = data_exercises[number].get("boilerplate")
                    if boilerplate is not None and boilerplate.strip() != "":
                        print("\nBoilerplate code (can be found in boilerplate-file):\n")
                        print(textwrap.indent(boilerplate, '\t'))

                        with open("boilerplate", "w") as boilerplate_file:
                            boilerplate_file.write(boilerplate)
                    break

        if config['exercise_id'] is None:
            print("Not a valid exercise id or -name!")

    else:
        # You can't select more when everything is already selected
        print('There is already an exercise selected, '
              'please remove selection with --up or -u to select a new exercise first.')

    # Save selections in config file
    set_data.dump_config(config)
