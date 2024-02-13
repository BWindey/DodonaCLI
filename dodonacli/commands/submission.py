import click
import http.client

from click_default_group import DefaultGroup

from dodonacli.source import get_data, pretty_print, set_data


@click.group(help="Get submission data. Default = view",
             cls=DefaultGroup, default='view', default_if_no_args=True)
def sub():
    pass


def validate_positive_int(ctx, param, value):
    if value is not None and value < 0:
        raise click.BadParameter('Number should be greater then 0')
    return value


@click.command(help="Load a submission to the prev_submission file, and display more info about it. "
                    "You can specify a number, else it takes the last submission for that exercise.")
@click.argument('number',
                type=int, default=0, callback=validate_positive_int)
def load(number):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    if config['exercise_id']:
        json_all_submissions = get_data.exercise_submissions(config, connection, headers)
    else:
        json_all_submissions = get_data.all_submissions(connection, headers)

    submission = json_all_submissions[-int(number)]

    submission_info = get_data.submission_info(submission['id'], connection, headers, config)
    set_data.save_submission_code(submission_info['exercise_name'], submission_info['id'], submission_info['code'])

    return


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

    if config['exercise_id']:
        json_data = get_data.exercise_submissions(config, connection, headers)
        pretty_print.print_exercise_submissions(json_data)
    else:
        json_data = get_data.all_submissions(connection, headers)
        pretty_print.print_all_submissions(connection, headers, json_data)


sub.add_command(load)
sub.add_command(view)
