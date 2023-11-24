import click
import http.client

from source import get_data, pretty_print


@click.command(help="Display up to your 10 lasts submissions for the current selected exercise.")
@click.option("-l", "--load", type=int, default=-1,
              help="NOT WORKY YET Load a submission to the prev_submission file, and display more info about it. "
                   "You can specify a number, else it takes the last submission for that exercise.")
def sub(load):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    if load:
        if config['exercise_id']:
            json_data = get_data.exercise_submissions(config, connection, headers)
            pretty_print.print_submissions(json_data)

        else:
            print("Nothing to display yet.")
