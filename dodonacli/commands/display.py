import click
import http.client

from dodonacli.source import pretty_print, get_data


@click.command(help="Display info based on the current selection. It will always display what you can select next, "
                    "or an exercise description if you have selected up to an exercise.")
@click.option("-force", "--force",
              help="Force display (with possible mistakes) the exercise (-series) description to display.",
              is_flag=True, default=False)
def display(force):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    # Display flag changes behaviour depending on the values in the config-dictionary.
    if config['course_id'] is None:
        # Print available courses
        json_data = get_data.courses_data(connection, headers)
        pretty_print.print_courses_data(json_data)

    elif config['serie_id'] is None:
        # Print available series
        json_data = get_data.series_data(connection, headers, config['course_id'])
        pretty_print.print_series_data(json_data, force)

    elif config['exercise_id'] is None:
        # Print available exercises
        if config['serie_token'] is None:
            serie_token = ""
        else:
            serie_token = "?token=" + config['serie_token']

        json_data = get_data.exercises_data(connection, headers, config['serie_id'], serie_token)
        pretty_print.print_exercise_data(json_data)

    else:
        # Print exercise-description
        json_data = get_data.exercise_data(connection, headers, config['course_id'], config['exercise_id'])
        pretty_print.print_exercise(json_data, config['TOKEN'], force)
