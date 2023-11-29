import click
import http.client

from dodonacli.source import set_data
from dodonacli.source import get_data


@click.command(help="Post a solution-file to Dodona. "
                    "The file has to be in your current working directory, and this only works "
                    "if there is a selected exercise.")
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
def post(file):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    # Post exercise to Dodona, does not work if there is no exercise selected
    if not config['exercise_id']:
        print("\nNo exercise selected!\n")
    else:
        with open(file, 'r') as infile:
            content = infile.read()
        set_data.post_solution(content, connection, headers, config)

