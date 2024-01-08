import click
import http.client

from dodonacli.source import get_data, pretty_print, set_data


# Function and file have to be called cli_next, as next
# is a Python built-in. The command, however, will still be called
# with 'next', as click provides the 'name=' argument
@click.command(name="next",
               help="WARING: might overwrite 'boilerplate' file! "
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
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    if config.get('exercise_id') is not None:
        config = get_next_exercise(config, connection, headers, reverse, unsolved)

    elif config.get('serie_id') is not None:
        print("\nThis isn't implemented yet (for series and courses)."
              "\nI wanted to get the 'next' command already available if you have exams in the coming period.\n")

    elif config.get('course_id') is not None:
        print("\nThis isn't implemented yet (for series and courses)."
              "\nI wanted to get the 'next' command already available if you have exams in the coming period.\n")

    else:
        print("\nCan't select a next course when non are selected.\n")
        return

    set_data.dump_config(config)


def get_next_exercise(config, connection, headers, reverse, unsolved):
    # Get all exercises of selected series
    exercise_data_json = get_data.exercises_data(
        connection, headers, config['serie_id'], config['serie_token'] or ""
    )

    # Calculate some needed values
    id_list = [exercise['id'] for exercise in exercise_data_json]
    previous_id = config['exercise_id']
    last_id_index = id_list.index(int(previous_id))

    exercises_dict = {exercise['id']: {
        'name': exercise['name'],
        'boilerplate': exercise['boilerplate'] or "",
        'accepted': exercise['accepted'],
        'description_url': exercise['description_url']
    } for exercise in exercise_data_json
    }

    # Find the next exercise (loop back to front if it was the last)
    next_id = -1
    if not unsolved:
        next_id = id_list[(last_id_index + 1 - (2 * reverse)) % len(id_list)]
    else:
        i = 1
        while next_id == -1 and i < len(id_list):
            if not exercises_dict[id_list[(last_id_index + i * (-1) ** reverse) % len(id_list)]]['accepted']:
                next_id = id_list[(last_id_index + i * (-1) ** reverse) % len(id_list)]
            i += 1
        if next_id == -1:
            print("\nYou already solved everything, there is no unsolved exercise to go to!\n")
            return config

    # Store new exercise
    config['exercise_id'] = str(next_id)
    config['exercise_name'] = exercises_dict[next_id]['name']

    next_id_index = id_list.index(int(next_id))

    # Visual arrow representation of the jump:
    prefixes = {}
    if next_id_index > last_id_index:
        prefixes[str(next_id)] = "   \u2570\u2B9E\t"
        prefixes[str(previous_id)] = "   \u256D\u2500\t"
        for e in id_list[last_id_index + 1:next_id_index]:
            prefixes[str(e)] = "   \u2502\t"
    else:
        prefixes[str(next_id)] = "   \u256D\u2B9E\t"
        prefixes[str(previous_id)] = "   \u2570\u2500\t"
        for e in id_list[next_id_index + 1:last_id_index]:
            prefixes[str(e)] = "   \u2502\t"

    pretty_print.print_exercise_data(exercise_data_json, prefixes)

    # Handle potential boilerplate.
    # I decided to not print the boilerplate, it felt too clunky.
    boilerplate = exercises_dict[next_id]['boilerplate']
    if boilerplate is not None and boilerplate.strip() != "":
        print("\nBoilerplate code is put in 'boilerplate'-file\n")
        with open("boilerplate", "w") as boilerplate_file:
            boilerplate_file.write(boilerplate)

    return config
