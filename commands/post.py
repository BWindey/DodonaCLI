import click
import http.client

from source import handle_flags, get_data


@click.command(help="Post the contents of a file to Dodona as a solution of the current selected exercise."
                    "Only works if there is a selected exercise.")
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

    handle_flags.handle_post(file, config, connection, headers)
