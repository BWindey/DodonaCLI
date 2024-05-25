import click


# Function and file have to be called cli_next, as next
# is a Python built-in. The command, however, will still be called
# with 'next', as click provides the 'name=' argument
@click.command(name="next",
               help="WARNING: might overwrite 'boilerplate' file! "
                    "Move to the next type of what you have selected. "
                    "It loops around to the beginning if the current selection "
                    "is at the end of the 'list'. If some boilerplate is attached "
                    "to the next exercise, it will put that in a file.")
@click.option("-r", "--reverse",
              help="Goes to the previous instead of the next.",
              is_flag=True, default=False)
@click.option("-u", "--unsolved",
              help="Find the next unsolved item. "
                   "Currently only available for exercises, not series or courses.",
              is_flag=True, default=False)
def cli_next(reverse, unsolved):
    import http.client
    from dodonacli.source import get_data, set_data

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

    if config.get('exercise_id') is not None:
        config = get_next_exercise(config, settings, connection, headers, reverse, unsolved)

    elif config.get('serie_id') is not None:
        config = get_next_series(config, settings, connection, headers, reverse, unsolved)

    elif config.get('course_id') is not None:
        config = get_next_course(config, settings, connection, headers, reverse, unsolved)

    else:
        print(
            '\n' * settings['new_lines_above']
            + "Can't select a next course when non are selected."
            + '\n' * settings['new_lines_below']
        )
        return

    set_data.dump_config(config)


def get_next_exercise(config, settings, connection, headers, reverse, unsolved):
    from dodonacli.source import get_data, pretty_print

    # Get all exercises of selected series
    exercise_data_json = get_data.exercises_data(
        connection, headers, config['serie_id'], f"/?token={config['serie_token']}" if config['serie_token'] else ""
    )

    # Calculate some needed values
    id_list = [exercise['id'] for exercise in exercise_data_json]
    previous_id = config['exercise_id']
    previous_id_index = id_list.index(int(previous_id))

    exercises_dict = {exercise['id']: {
        'name': exercise['name'],
        'boilerplate': exercise.get('boilerplate') or "",
        'programming_language': exercise.get('programming_language') or None,
        'accepted': exercise.get('accepted') or exercise.get('has_read'),
        'description_url': exercise['description_url']
    } for exercise in exercise_data_json
    }

    # Find the next exercise (loop back to front if it was the last)
    next_id = -1
    if not unsolved:
        next_id = id_list[(previous_id_index + 1 - (2 * reverse)) % len(id_list)]
    else:
        i = 1
        while next_id == -1 and i < len(id_list):
            if not exercises_dict[id_list[(previous_id_index + i * (-1) ** reverse) % len(id_list)]]['accepted']:
                next_id = id_list[(previous_id_index + i * (-1) ** reverse) % len(id_list)]
            i += 1
        if next_id == -1:
            print(
                '\n' * settings['new_lines_above']
                + "You already solved everything, there is no unsolved exercise to go to!"
                + '\n' * settings['new_lines_below']
            )
            return config

    # Store new exercise
    config['exercise_id'] = str(next_id)
    config['exercise_name'] = exercises_dict[next_id]['name']
    if exercises_dict[next_id]['programming_language']:
        config['programming_language'] = exercises_dict[next_id]['programming_language']['name']

    prefixes = make_visual_representation(previous_id, previous_id_index, next_id, id_list)

    pretty_print.print_exercise_data(exercise_data_json, settings, prefixes)

    # Handle potential boilerplate.
    # I decided to not print the boilerplate (as a 'select' would do), it felt too clunky here.
    boilerplate = exercises_dict[next_id]['boilerplate']
    if boilerplate is not None and boilerplate.strip() != "":
        file_extension = exercises_dict[next_id]['programming_language']['extension']
        print(f"Boilerplate code is put in 'boilerplate.{file_extension}'-file" + '\n' * settings['new_lines_below'])
        with open(f"boilerplate.{file_extension}", "w") as boilerplate_file:
            boilerplate_file.write(boilerplate)

    return config


def get_next_series(config, settings, connection, headers, reverse, unsolved):
    if config['serie_token']:
        print(
            '\n' * settings['new_lines_below']
            + "Sorry, you can't use 'next' when inside a hidden series."
            + '\n' * settings['new_lines_below']
        )
        return config

    # Only import when we need it, speeds things up
    from dodonacli.source import get_data, pretty_print

    # Get all series of selected course
    series_data_json = get_data.series_data(
        connection, headers, config['course_id']
    )

    # Take only necessary info from the large json
    # Series have an order, so sort them so the order is guarenteed
    series_list = [
        {'id': series['id'], 'name': series['name'], 'order': series['order']}
        for series in series_data_json
    ]
    series_list.sort(key=lambda x: x['order'])

    # Using the sorted list here to keep ensuring the same order
    id_list = [series['id'] for series in series_list]
    previous_id = config['serie_id']
    previous_id_index = id_list.index(int(previous_id))

    # Find the next series (loop back to front if it was the last)
    # If series ever get a solved/unsolved status support in API, this can get
    # the same logic found in get_next_exercise()
    if unsolved:
        print(
            '\n' * settings['new_lines_above']
            + "Unsolved flag not supported yet for series and courses."
            + '\n' * settings['new_lines_below']
        )
    next_id = id_list[(previous_id_index + 1 - (2 * reverse)) % len(id_list)]

    # Store new series
    config['serie_id'] = str(next_id)
    config['serie_name'] = [
        series['name'] for series in series_list if series['id'] == next_id
    ][0]

    prefixes = make_visual_representation(previous_id, previous_id_index, next_id, id_list)
    pretty_print.print_series_data(series_data_json, settings, prefixes=prefixes)

    return config


def get_next_course(config, settings, connection, headers, reverse, unsolved):
    from dodonacli.source import get_data, pretty_print, pretty_printer

    # Get all registred courses
    course_data_json = get_data.courses_data(connection, headers)

    id_list = [course['id'] for course in course_data_json]
    previous_id = config['course_id']
    previous_id_index = id_list.index(int(previous_id))

    # Find the next course (loop back to front if it was the last)
    # If courses get more data that indicates if it's completely solved,
    # then this will get the same logic found in get_next_exercise()
    if unsolved:
        pretty_printer.custom_print(
            "Unsolved flag not supported yet for series and courses.",
            {'new_lines_above': settings['new_lines_above']}
        )

    next_id = id_list[(previous_id_index + 1 - (2 * reverse)) % len(id_list)]

    # Store new course
    config['course_id'] = str(next_id)
    config['course_name'] = [
        course['name'] for course in course_data_json if course['id'] == next_id
    ][0]

    prefixes = make_visual_representation(previous_id, previous_id_index, next_id, id_list)
    pretty_print.print_courses_data(
        course_data_json, {'new_lines_below': settings['new_lines_below']}, prefixes=prefixes
    )

    return config


def make_visual_representation(previous_id, previous_id_index, next_id, id_list) -> dict:
    next_id_index = id_list.index(int(next_id))

    # Visual arrow representation of the jump:
    prefixes = {}
    if next_id_index > previous_id_index:
        prefixes[str(next_id)] = "   \u2570\u2B9E\t"
        prefixes[str(previous_id)] = "   \u256D\u2500\t"
        for e in id_list[previous_id_index + 1:next_id_index]:
            prefixes[str(e)] = "   \u2502\t"
    else:
        prefixes[str(next_id)] = "   \u256D\u2B9E\t"
        prefixes[str(previous_id)] = "   \u2570\u2500\t"
        for e in id_list[next_id_index + 1:previous_id_index]:
            prefixes[str(e)] = "   \u2502\t"

    return prefixes
