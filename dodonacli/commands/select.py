import click
import http.client


@click.command(
    help="Select based on id or name. Depends on current selection. "
         "If nothing is selected, it will try to select a course, "
         "then an exercise-series, then an exercise. "
         "Will not work with invalid id's or names without flag.")
@click.option("--hidden", "-hidden",
              help="Access a hidden series. Only available when trying to select "
                   "exercise series."
                   "\n\nUsage: dodona select --hidden <TOKEN> <SERIES_ID>")
@click.option("--other", "-other",
              help="Select a course that you're not registered for. Only works with "
                   "an id, not a name.",
              is_flag=True, default=False)
@click.argument('thing')
def select(thing, hidden, other):
    from dodonacli.source import set_data, get_data

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
        config = select_course(connection, headers, thing, config, other)

    elif config['serie_id'] is None:
        if hidden:
            config = select_hidden_series(
                connection, headers, thing, hidden, config
            )
        else:
            config = select_series(connection, headers, thing, config)

    elif config['exercise_id'] is None:
        config = select_exercise(connection, headers, thing, config)

    else:
        # You can't select more when everything is already selected
        print("There is already an exercise selected, please remove selection "
              "with --up or -u to select a new exercise first.")

    # Save selections in config file
    set_data.dump_config(config)

    return


def select_course(connection: http.client.HTTPSConnection, headers: dict,
                  thing: str, config: dict, other: bool):
    if not other:
        return select_registered_course(connection, headers, thing, config)
    else:
        return select_unregistered_course(connection, headers, thing, config)


def select_registered_course(connection: http.client.HTTPSConnection,
                             headers: dict, thing: str, config: dict) -> dict:
    from dodonacli.source import pretty_console, get_data

    # Get all registered courses to check if a valid course was selected
    data_courses = get_data.courses_data(connection, headers)
    courses = {str(course['id']): course['name'] for course in data_courses}

    # First try to match on id, else on name
    if thing.isnumeric() and thing in courses:
        config['course_id'] = thing
        config['course_name'] = courses[thing]

        pretty_console.console.print(
            f"\nCourse [bold]\"{courses[thing]}\"[/] selected.\n")
    else:
        for course in courses.items():
            if thing.lower() in course[1].lower():
                config['course_id'] = course[0]
                config['course_name'] = course[1]

                pretty_console.console.print(
                    f"\nCourse [bold]\"{courses[course[0]]}\" [/] selected.\n")

                # We found it, we can stop searching
                break

    # If config_id is still empty, nothing is found:
    if config['course_id'] is None:
        print("\nNot a valid course-id or -name.\n")

    return config


def select_unregistered_course(connection: http.client.HTTPSConnection,
                               headers: dict, thing: str, config: dict) -> dict:
    import json
    from dodonacli.source import pretty_console, get_data

    # Has to be an id, because it's not possible to match against names 
    if not thing.isnumeric():
        print("The selection needs to be an id (all numbers). "
              "It's not possible to match by name.")
        return config

    link = f"/courses/{thing}"
    connection = get_data.handle_connection_request(
        connection, "GET", link, headers)

    res = connection.getresponse()

    if res.status != 200:
        print("Something went wrong trying to select this course.\n"
              "Make sure you have a valid course-id.\n"
              "\tResonse code: " + str(res.status) +
              "\n\tReason: " + str(res.reason))
        return config

    json_data = json.loads(res.read())
    config['course_id'] = thing
    config['course_name'] = json_data['name']

    pretty_console.console.print(
        f"\nCourse [bold]\"{json_data['name']}\"[/] selected.\n")

    return config


def select_series(connection: http.client.HTTPSConnection, headers: dict,
                  thing: str, config: dict):
    from dodonacli.source import pretty_console, get_data

    data_series = get_data.series_data(connection, headers, config['course_id'])

    series = {str(serie['id']): serie['name'] for serie in data_series}

    if thing.isnumeric() and thing in series:
        config['serie_id'] = thing
        config['serie_name'] = series[thing]
        pretty_console.console.print(
            "\nSeries [bold]\"" + series[thing] + "\"[/] selected.\n")
    else:
        for serie in series.items():
            if thing.lower() in serie[1].lower():
                config['serie_id'] = serie[0]
                config['serie_name'] = serie[1]
                pretty_console.console.print(
                    "\nSerie [bold]\"" + series[serie[0]] + "\"[/] selected.\n")
                break
    if config['serie_id'] is None:
        print("\nNot a valid series id or -name!\n")

    return config


def select_hidden_series(connection: http.client.HTTPSConnection, headers: dict,
                         series_id: str, series_token: str, config: dict):
    import json
    from dodonacli.source import pretty_console, get_data

    if not series_id.isnumeric():
        print("Well this won't work without a valid ID "
              "(only numeric characters). Please try again.")
        return config

    link = f"/series/{series_id}?token={series_token}"
    connection = get_data.handle_connection_request(
        connection, "GET", link, headers)

    res = connection.getresponse()

    if res.status != 200:
        print("Something went wrong trying to select the hidden series.\n"
              "Check if you got the right series-id "
              "(seen in /series/<serie_id> in the link you got).\n"
              "\tResponse code: " + str(res.status) +
              "\n\tReason: " + str(res.reason))
        return config

    json_data = json.loads(res.read())
    config['serie_id'] = series_id
    config['serie_name'] = json_data['name']
    config['serie_token'] = series_token

    pretty_console.console.print(
        f"\nSerie [bold]\"{json_data['name']}\"[/] selected.\n")

    return config


def select_exercise(connection: http.client.HTTPSConnection, headers: dict,
                    selection: str, config: dict) -> dict:
    import textwrap
    from dodonacli.source import pretty_console, get_data

    # Token for hidden series
    if config['serie_token'] is None:
        serie_token = ""
    else:
        serie_token = "?token=" + config['serie_token']

    data_exercises = get_data.exercises_data(
        connection, headers, config['serie_id'], serie_token
    )

    selected_exercise = {}

    if selection.isnumeric() and selection in [exercise['id'] for exercise in data_exercises]:
        selected_exercise = [exercise for exercise in data_exercises if exercise['id'] == selection]

    else:
        for exercise in data_exercises:
            if selection.lower() in exercise['name'].lower():
                selected_exercise = exercise
                break

    if selected_exercise == {}:
        print("\nNot a valid exercise-id or -name.\n")
        return config

    # Store selection
    config['exercise_id'] = str(selected_exercise['id'])
    config['exercise_name'] = selected_exercise['name']
    # Programming language may not exist (f.e. for ContentPage)
    programming_language = selected_exercise.get('programming_language')
    if programming_language:
        config['programming_language'] = programming_language['name']

    pretty_console.console.print(f"\nExercise [bold]{selected_exercise['name']}[/] selected.\n")

    boilerplate = selected_exercise.get('boilerplate')
    if boilerplate and boilerplate.strip() != "":
        print("\nBoilerplate code (copy in boilerplate-file):\n")
        print(textwrap.indent(boilerplate, '\t'))
        with open("boilerplate." + programming_language['extension'], "w") as boilerplate_file:
            boilerplate_file.write(boilerplate)

    return config
