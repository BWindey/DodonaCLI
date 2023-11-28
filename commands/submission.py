import os

try:
    import click
    import http.client

    from click_default_group import DefaultGroup

except ImportError as e:
    answer = input("There were unmet dependencies: \n"
                   + str(e)
                   + '\nDo you want to install them automatically? [y/n]: ')
    if not answer.lower().startswith('y'):
        exit("Exited due to unmet dependencies")
    os.system('pip install -r' + os.path.dirname(__file__)[:-8] + 'requirements.txt')

    import click
    import http.client

    from click_default_group import DefaultGroup


from source import get_data, pretty_print


@click.group(help="Get submission data. Default = view",
             cls=DefaultGroup, default='view', default_if_no_args=True)
def sub():
    pass


@click.command(help="Load submission data")
@click.option("-l", "--load", type=int, default=-1,
              help="NOT WORKY YET Load a submission to the prev_submission file, and display more info about it. "
                   "You can specify a number, else it takes the last submission for that exercise.")
def load():
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
