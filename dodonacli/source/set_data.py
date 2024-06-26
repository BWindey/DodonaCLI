import http.client
import json
import os
import random
import rich.status
import time

from datetime import datetime

from . import pretty_print, get_data, pretty_printer


def dump_config(config: dict):
    """
    Save the config to it's file again.
    :param config: Dictionary containing the configs
    """
    config_home = get_data.get_config_home()
    config_file_path = os.path.join(config_home, "config.json")

    if not os.path.exists(config_home):
        os.makedirs(config_home)

    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)


def dump_settings(settings: dict):
    """
    Save the settings to their file again.
    :param settings: Dictionary containing the settings
    """
    config_home = get_data.get_config_home()
    settings_file_path = os.path.join(config_home, "settings.json")

    if not os.path.exists(config_home):
        os.makedirs(config_home)

    with open(settings_file_path, 'w') as settings_file:
        json.dump(settings, settings_file, indent=4)


def post_solution(content: str, connection: http.client.HTTPSConnection, headers: dict, course_id: str,
                  exercise_id: str, settings):
    """
    Post the solution in content to Dodona and print the result
    :param content: str with the solution to post to Dodona
    :param connection: HTTPSConnection object that connects to www.dodona.be
    :param headers: dict with extra info for connection, mainly authorization needed
    :param course_id:
    :param exercise_id:
    :param settings: dict with settings
    """
    # Make dict with info needed to post the solution and dump it in a json object
    payload = {
        "submission": {
            "code": content,
            "course_id": course_id,
            "exercise_id": exercise_id
        }
    }
    json_payload = json.dumps(payload)

    # Connect to Dodona and post the solution
    connection.request("POST", "/submissions.json", json_payload, headers=headers)
    res = connection.getresponse()
    status = res.status
    if status == 422:
        pretty_printer.custom_print(
            "[i]Patience, young padawan.\n"
            "A cooldown, Dodona servers have, to prevent DDOS attacks, hmm, yes.[/]",
            settings, pretty=True
        )
        return

    elif status != 200:
        pretty_printer.custom_print(
            "Error connection to Dodona: " + str(res.status) + '\n'
            + "Reason: " + res.reason,
            settings, pretty=True
        )
        return

    # Read out the result
    data = res.read()
    json_data = json.loads(data)

    # The Dodona servers take some time to test the solution, so we'll have to keeping asking for an answer.
    json_data['status'] = "running"

    # Spinner animation effect while waiting
    print('\n' * settings['new_lines_above'], end='')

    # Disable the new_lines_above here for the further prints, but need more than just that settings,
    # that's why I don't just make a new dict with only 'new_lines_below' in
    settings['new_lines_above'] = 0

    waiting = rich.status.Status(
        "Posting your solution, please wait while the servers evaluate your code.",
        spinner=select_spinner()
    )
    waiting.start()
    wait_interval = 0

    while json_data['status'] in ("running", "queued"):
        # Aks the servers for the result with an increasing interval, from 1s to 5s, as the website does
        time.sleep(wait_interval)
        if wait_interval < 5:
            wait_interval += 1

        connection.request("GET", "/submissions/" + str(json_data['id']) + ".json", headers=headers)
        res = connection.getresponse()
        if res.status != 200:
            print("Error connection to Dodona: " + str(res.status))
            print("Reason: " + res.reason, end='\n' * settings['new_lines_below'])
            return

        json_data: dict[str, str] = json.loads(res.read())

    waiting.stop()
    connection.close()

    # Print out the results
    pretty_print.print_result(
        json.loads(json_data['result']),
        json_data['url'][:json_data['url'].rfind('.')],
        settings
    )


def select_spinner() -> str:
    """
    Select a random spinner-name from a preselected list with good animations.
    During Christmas season (11th of Decembre - 8th of January) it always returns the same Christmas spinner.
    :return: Name of Rich spinner
    """
    selection_spinners = ['arrow', 'balloon', 'balloon2', 'bouncingBar', 'boxBounce', 'boxBounce2', 'circle',
                          'circleHalves', 'circleQuarters', 'clock', 'dots2', 'dots3', 'dots4', 'dots5', 'dots6',
                          'dots7', 'dots8', 'dots8Bit', 'dots9', 'dots10', 'dots11', 'dots12', 'dqpb', 'flip',
                          'hamburger', 'layer', 'line', 'line2', 'moon', 'pipe', 'point', 'runner', 'simpleDots',
                          'simpleDotsScrolling', 'squareCorners']

    christmas_spinner = 'christmas'

    # Get the current date
    current_date = datetime.now().date()

    # Define the Christmas season range
    christmas_start = datetime(current_date.year, 12, 11).date()
    christmas_end = datetime(current_date.year, 1, 8).date()

    # Check if the current date is within the Christmas season range
    is_christmas_season = not christmas_start > current_date > christmas_end

    if is_christmas_season:
        return christmas_spinner

    return random.choice(selection_spinners)


def save_to_file(name: str, submission_id: int, content: str, settings: dict, extension: str = ""):
    """
    Save code to a file in the users current working directory.
    The resulting file name: {name}_{id}{extension}
    :param name: Name of the file
    :param submission_id: ID to add to the name of file
    :param content: Content to save in the file
    :param settings: dict with settings
    :param extension: Optional file-extension, has to include the '.'
    """
    name = name.replace(' ', '-')
    file_name = f"{name}_{submission_id}{extension}"

    with open(file_name, "w") as code_file:
        code_file.write(content)

    pretty_printer.custom_print(
        f"Code from your submission for {name} is now saved in:\n"
        f"\t{name}_{submission_id}{extension}",
        settings, pretty=True
    )
