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
    from dodonacli.source import set_data, get_data, pretty_print, pretty_printer

    # Read configs in
    config = get_data.get_configs()
    settings = get_data.get_settings()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    if config['course_id'] is None:
        if settings['display_series_after_select']:
            config = select_course(
                connection, headers, thing, config,
                {'new_lines_above': settings['new_lines_above'], 'new_lines_below': 1},
                other
            )
            # Print available series
            json_data = get_data.series_data(connection, headers, config['course_id'])
            pretty_print.print_series_data(json_data, {'new_lines_below': settings['new_lines_below']})
        else:
            config = select_course(connection, headers, thing, config, settings, other)

    elif config['serie_id'] is None:
        if settings['display_exercises_after_select']:
            if hidden:
                config = select_hidden_series(
                    connection, headers, thing, hidden, config,
                    {'new_lines_above': settings['new_lines_above'], 'new_lines_below': 1}
                )
            else:
                config = select_series(
                    connection, headers, thing, config,
                    {'new_lines_above': settings['new_lines_above'], 'new_lines_below': 1}
                )
            # Print available exercises
            if config['serie_token'] is None:
                serie_token = ""
            else:
                serie_token = "?token=" + config['serie_token']

            json_data = get_data.exercises_data(connection, headers, config['serie_id'], serie_token)
            pretty_print.print_exercise_data(json_data, {'new_lines_below': settings['new_lines_below']})
        else:
            if hidden:
                config = select_hidden_series(connection, headers, thing, hidden, config, settings)
            else:
                config = select_series(connection, headers, thing, config, settings)

    elif config['exercise_id'] is None:
        if settings['display_exercise_after_select']:
            config = select_exercise(
                connection, headers, thing, config,
                {'new_lines_above': settings['new_lines_above'], 'new_lines_below': 1}
            )
            # Print exercise-description
            json_data = get_data.exercise_data(connection, headers, config['course_id'], config['exercise_id'])
            pretty_print.print_exercise(json_data, config['TOKEN'], {'new_lines_below': settings['new_lines_below']})
        else:
            config = select_exercise(connection, headers, thing, config, settings)

    else:
        # You can't select more when everything is already selected
        pretty_printer.custom_print(
            "There is already an exercise selected.\n"
            "Please remove selection with 'dodona up' before selecting a new exercise.",
            settings
        )
        return

    # Save selections in config file
    set_data.dump_config(config)

    return


def select_course(connection: http.client.HTTPSConnection, headers: dict,
                  thing: str, config: dict, settings: dict, other: bool) -> dict:
    if not other:
        return select_registered_course(connection, headers, thing, config, settings)
    else:
        return select_unregistered_course(connection, headers, thing, config, settings)


def select_registered_course(connection: http.client.HTTPSConnection,
                             headers: dict, course: str, config: dict, settings: dict) -> dict:
    from dodonacli.source import pretty_console, get_data

    # Get all registered courses to check if a valid course was selected
    data_courses = get_data.courses_data(connection, headers)
    courses = {str(course['id']): course['name'] for course in data_courses}

    # First try to match on id, else on name
    if course.isnumeric() and course in courses:
        config['course_id'] = course
        config['course_name'] = courses[course]

        pretty_console.console.print(
            '\n' * settings['new_lines_above']
            + f"Course [bold]\"{courses[course]}\"[/] selected."
            + '\n' * settings['new_lines_below']
        )
    else:
        for course_item in courses.items():
            if course.lower() in course_item[1].lower():
                config['course_id'] = course_item[0]
                config['course_name'] = course_item[1]

                pretty_console.console.print(
                    '\n' * settings['new_lines_above']
                    + f"Course [bold]\"{courses[course_item[0]]}\" [/] selected."
                    + '\n' * settings['new_lines_below']
                )

                # We found it, we can stop searching
                break

    # If config_id is still empty, nothing is found:
    if config['course_id'] is None:
        print(
            '\n' * settings['new_lines_above']
            + "Not a valid course-id or -name."
            + '\n' * settings['new_lines_below']
        )

    return config


def select_unregistered_course(connection: http.client.HTTPSConnection,
                               headers: dict, course_id: str, config: dict, settings: dict) -> dict:
    import json
    from dodonacli.source import pretty_console, get_data

    # Has to be an id, because it's not possible to match against names
    if not course_id.isnumeric():
        print(
            '\n' * settings['new_lines_above']
            + "The selection needs to be an id (all numbers). "
              "It's not possible to match by name."
            + '\n' * settings['new_lines_below']
        )
        return config

    link = f"/courses/{course_id}"
    connection = get_data.handle_connection_request(connection, "GET", link, headers)

    res = connection.getresponse()

    if res.status != 200:
        print(
            '\n' * settings['new_lines_above']
            + "Something went wrong trying to select this course.\n"
              "Make sure you have a valid course-id.\n"
              "\tResonse code: " + str(res.status) +
            "\n\tReason: " + str(res.reason).strip()
            + '\n' * settings['new_lines_below']
        )
        return config

    json_data = json.loads(res.read())
    config['course_id'] = course_id
    config['course_name'] = json_data['name']

    pretty_console.console.print(
        '\n' * settings['new_lines_above']
        + f"Course [bold]\"{json_data['name']}\"[/] selected."
        + '\n' * settings['new_lines_below']
    )

    return config


def select_series(connection: http.client.HTTPSConnection, headers: dict,
                  thing: str, config: dict, settings: dict):
    from dodonacli.source import pretty_console, get_data

    data_series = get_data.series_data(connection, headers, config['course_id'])

    series = {str(serie['id']): serie['name'] for serie in data_series}

    if thing.isnumeric() and thing in series:
        config['serie_id'] = thing
        config['serie_name'] = series[thing]
        pretty_console.console.print(
            '\n' * settings['new_lines_above']
            + f"Series [bold]\"{series[thing]}\"[/] selected."
            + '\n' * settings['new_lines_below']
        )
    else:
        for serie in series.items():
            if thing.lower() in serie[1].lower():
                config['serie_id'] = serie[0]
                config['serie_name'] = serie[1]
                pretty_console.console.print(
                    '\n' * settings['new_lines_above']
                    + f"Series [bold]\"{series[serie[0]]}\"[/] selected."
                    + '\n' * settings['new_lines_below']
                )
                break
    if config['serie_id'] is None:
        print(
            '\n' * settings['new_lines_above']
            + "Not a valid series id or -name!"
            + '\n' * settings['new_lines_below']
        )

    return config


def select_hidden_series(connection: http.client.HTTPSConnection, headers: dict,
                         series_id: str, series_token: str, config: dict, settings: dict):
    import json
    from dodonacli.source import pretty_console, get_data

    if not series_id.isnumeric():
        print(
            '\n' * settings['new_lines_above']
            + "Well, this won't work without a valid series-ID (only numeric characters). Please try again."
            + '\n' * settings['new_lines_below']
        )
        return config

    link = f"/series/{series_id}?token={series_token}"
    connection = get_data.handle_connection_request(
        connection, "GET", link, headers)

    res = connection.getresponse()

    if res.status != 200:
        print(
            '\n' * settings['new_lines_above']
            + "Something went wrong trying to select the hidden series.\n"
              "Check if you got the right series-id "
              "(seen in /series/<serie_id> in the link you got).\n"
              "\tResponse code: " + str(res.status)
            + "\n\tReason: " + str(res.reason).strip()
            + '\n' * settings['new_lines_below']
        )
        return config

    json_data = json.loads(res.read())
    config['serie_id'] = series_id
    config['serie_name'] = json_data['name']
    config['serie_token'] = series_token

    pretty_console.console.print(
        '\n' * settings['new_lines_above']
        + f"Series [bold]\"{json_data['name']}\"[/] selected."
        + '\n' * settings['new_lines_below']
    )

    return config


def select_exercise(connection: http.client.HTTPSConnection, headers: dict,
                    selection: str, config: dict, settings: dict) -> dict:
    import textwrap
    from dodonacli.source import pretty_console, get_data

    # Token for hidden series
    if config['serie_token'] is None:
        serie_token = ""
    else:
        serie_token = "?token=" + config['serie_token']

    data_exercises = get_data.exercises_data(connection, headers, config['serie_id'], serie_token)

    selected_exercise = {}

    if selection.isnumeric() and int(selection) in (exercise['id'] for exercise in data_exercises):
        selected_exercise = [exercise for exercise in data_exercises if exercise['id'] == int(selection)][0]

    else:
        for exercise in data_exercises:
            if selection.lower() in exercise['name'].lower():
                selected_exercise = exercise
                break

    if selected_exercise == {}:
        print(
            '\n' * settings['new_lines_above']
            + "Not a valid exercise-id or -name."
            + '\n' * settings['new_lines_below']
        )
        return config

    # Store selection
    config['exercise_id'] = str(selected_exercise['id'])
    config['exercise_name'] = selected_exercise['name']
    # Programming language may not exist (f.e. for ContentPage)
    programming_language = selected_exercise.get('programming_language')
    if programming_language:
        config['programming_language'] = programming_language['name']

    pretty_console.console.print(
        '\n' * settings['new_lines_above']
        + f"Exercise [bold]{selected_exercise['name']}[/] selected."
    )

    boilerplate = selected_exercise.get('boilerplate')
    if boilerplate and boilerplate.strip() != "":
        print("\nBoilerplate code (copy in boilerplate-file):\n")
        print(textwrap.indent(boilerplate.rstrip(), '\t'))
        with open("boilerplate." + programming_language['extension'], "w") as boilerplate_file:
            boilerplate_file.write(boilerplate)

    print('\n' * settings['new_lines_below'], end='')

    return config
