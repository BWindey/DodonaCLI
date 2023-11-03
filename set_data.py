import json
import os
import time

from pretty_print import print_result
from pretty_console import console


def dump_config(config):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')

    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)


def post_solution(content, connection, headers, config):
    """
    Post the solution in content to Dodona and print the results
    :param content: str with the solution to post to Dodona
    :param connection: HTTPSConnection object that connects to www.dodona.be
    :param headers: dict with extra info for connection, mainly authorization needed
    :param config: dict with configs from config-file
    """
    # Make dict with info needed to post the solution and dump in in a json object
    payload = {
        "submission": {
            "code": content,
            "course_id": config['course_id'],
            "exercise_id": config['exercise_id']
        }
    }
    json_payload = json.dumps(payload)

    # Connect to Dodona and post the solution
    connection.request("POST", "/submissions.json", json_payload, headers=headers)
    res = connection.getresponse()
    status = res.status
    if status == 422:
        console.print("\n[i]Patience, young padawan.\n"
                      "A cooldown, Dodona servers have, to prevent DDOS attacks, hmm, yes.[/]\n")
    if status != 200:
        print("Error connection to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return

    # Read out the result
    data = res.read()
    json_data = json.loads(data)

    # The Dodona servers take some time to test the solution, so we ping them every 0.3s for an answer.
    json_data['status'] = "running"

    print("Posting your solution, please wait while the servers evaluate your code.\n")
    while json_data['status'] == "running":
        time.sleep(0.3)
        connection.request("GET", "/submissions/" + str(json_data['id']) + ".json", headers=headers)
        res = connection.getresponse()
        if res.status != 200:
            print("Error connection to Dodona: " + str(res.status))
            print("Reason: " + res.reason)
            return

        data = res.read()
        json_data = json.loads(data)

    connection.close()

    # Print out the results
    print_result(json.loads(json_data['result']))
