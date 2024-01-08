import json
import os
import random
import rich.status
import time

from datetime import datetime

from . import pretty_print, pretty_console


def dump_config(config):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, '../../config.json')

    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)


def post_solution(content, connection, headers, course_id, exercise_id):
    """
    Post the solution in content to Dodona and print the result
    :param content: str with the solution to post to Dodona
    :param connection: HTTPSConnection object that connects to www.dodona.be
    :param headers: dict with extra info for connection, mainly authorization needed
    :param course_id:
    :param exercise_id:
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
        pretty_console.console.print("\n[i]Patience, young padawan.\n"
                                     "A cooldown, Dodona servers have, to prevent DDOS attacks, hmm, yes.[/]\n")
        return

    elif status != 200:
        print("\nError connection to Dodona: " + str(res.status))
        print("Reason: " + res.reason + '\n')
        return

    # Read out the result
    data = res.read()
    json_data = json.loads(data)

    # The Dodona servers take some time to test the solution, so we ping them every 0.3s for an answer.
    json_data['status'] = "running"

    print()

    waiting = rich.status.Status("Posting your solution, please wait while the servers evaluate your code.",
                                 spinner=select_spinner())
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
            print("Reason: " + res.reason)
            return

        data = res.read()
        json_data = json.loads(data)

    waiting.stop()
    connection.close()

    # Print out the results
    pretty_print.print_result(json.loads(json_data['result']))
    print()


def select_spinner():
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


def save_submission_code(exer_name: str, sub_id: int, sub_code: str):
    file_name = f"{exer_name}_{sub_id}"

    with open(file_name, "w") as code_file:
        code_file.write(sub_code)

    print(f"\nCode from your submission for {exer_name} is now saved in:\n"
          f"\t{exer_name}_{sub_id}\n")
