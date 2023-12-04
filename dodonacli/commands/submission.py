import click
import http.client

from click_default_group import DefaultGroup

from dodonacli.source import pretty_print, get_data


@click.group(help="Get submission data. Default = view",
             cls=DefaultGroup, default='view', default_if_no_args=True)
def sub():
    pass


@click.command(help="NOT WORKY YET Load a submission to the prev_submission file, and display more info about it. "
                    "You can specify a number, else it takes the last submission for that exercise.")
def load():
    print("Sorry, still working on this!")
    pass


@click.command(help="View subimmision data")
def view():
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


sub.add_command(load)
sub.add_command(view)
