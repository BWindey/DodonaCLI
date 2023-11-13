import click
import http.client

from source import handle_flags, get_data


@click.command(help="select something")
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

    handle_flags.handle_select(thing, config, connection, headers)
