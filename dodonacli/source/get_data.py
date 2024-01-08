import datetime
import http.client
import json
import os
import socket

from . import set_data, interactive_tutorial


def handle_connection_request(connection: http.client.HTTPSConnection, connection_type: str,
                              link: str, headers: dict) -> http.client.HTTPSConnection:
    try:
        connection.request(connection_type, link, headers=headers)

    except socket.gaierror:
        print("Something went wrong trying to connect to Dodona. This is probably an internet connection problem.")
        exit(2)

    return connection


def handle_connection_response(connection: http.client.HTTPSConnection) -> bytes:
    """
    Handle response from Dodona connection
    Terminates program if there was a problem with the connection
    :param connection: HTTPSConnection object that has had a request
    :return: data
    """
    res = connection.getresponse()
    status = res.status
    if status != 200:
        print("Error connecting to Dodona: " + str(status))
        print("Reason: " + res.reason)
        exit(-1)

    data = res.read()
    connection.close()

    return data


def courses_data(connection: http.client.HTTPSConnection, headers: dict):
    """
    Get registered courses of user
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :return: json object with info about available courses
    """
    connection = handle_connection_request(connection, "GET", "/courses?tab=my", headers)
    data = handle_connection_response(connection)

    return json.loads(data)


def series_data(connection: http.client.HTTPSConnection, headers: dict, course_id: str):
    """
    Get all exercise-series of course
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param course_id: int id of the course to find series from
    :return: json object with info about available series
    """
    connection = handle_connection_request(connection, "GET", "/courses/" + course_id + "/series", headers=headers)
    data = handle_connection_response(connection)

    return json.loads(data)


def exercises_data(connection: http.client.HTTPSConnection, headers: dict, series_id: str, serie_token: str = ""):
    """
    Get all exercises of exercise-serie
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param series_id: int id of exercise-series
    :param serie_token: Token of a hidden series
    :return: json object with info about available exercises
    """
    connection = handle_connection_request(
        connection,
        "GET",
        "/series/" + series_id + "/activities" + serie_token,
        headers=headers
    )
    data = handle_connection_response(connection)

    return json.loads(data)


def exercise_data(connection: http.client.HTTPSConnection, headers: dict, course_id: str, exercise_id: str):
    """
    Get exercise-info for selected exercise
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param course_id: int id of course
    :param exercise_id: int id of exercise
    :return: json object with info about exercise
    """
    connection = handle_connection_request(
        connection, "GET",
        "/courses/" + course_id + "/activities/" + exercise_id,
        headers=headers
    )
    data = handle_connection_response(connection)

    return json.loads(data)


def exercise_submissions(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    course_id = config['course_id']
    series_id = config['serie_id']
    exercise_id = config['exercise_id']

    connection = handle_connection_request(
        connection,
        "GET",
        f"/courses/{course_id}/series/{series_id}/activities/{exercise_id}/submissions",
        headers=headers
    )
    data = handle_connection_response(connection)

    return json.loads(data)


def all_submissions(connection: http.client.HTTPSConnection, headers: dict):
    connection = handle_connection_request(
        connection,
        "GET",
        "/submissions",
        headers=headers
    )
    data = handle_connection_response(connection)

    return json.loads(data)


def submission_info(sub_id: int, connection: http.client.HTTPSConnection, headers: dict, config):
    connection = handle_connection_request(
        connection,
        "GET",
        f"/submissions/{sub_id}",
        headers=headers
    )
    data = handle_connection_response(connection)
    json_data = json.loads(data)

    exercise_id = json_data['exercise'].split('/')[-1].replace('.json', '')

    exercise = exercise_data(connection, headers, config['course_id'], exercise_id)

    json_data['exercise_name'] = exercise['name']

    return json_data


def get_configs():
    """
    Get config data from config.json
    :return: json object with config data
    """
    # Get the path of the config-file.
    # This is a bit more complicated because this file exists in the same directory as
    # the python files, but the command may be executed from anywhere with the appropriate alias set.
    # Thus, first the path to the directory of the python files is retrieved; then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, '../../config.json')

    # First try to open, if unable to open, create a new config-file and ask user for a token
    try:
        with open(config_file_path, "r") as file:
            config = json.load(file)

            config = validate_config(config)

    except FileNotFoundError:
        # Create config dictionary
        config = {e: None
                  for e in ["course_id", "course_name", "serie_id", "serie_name", "exercise_id", "exercise_name"]}

        print("\nThis may be your first time using DodonaCLI, do you wish to follow a short tutorial?")
        answer = input("(yes/no): ")

        if answer.lower().startswith("yes"):
            config = interactive_tutorial.start_tutorial(config)
        else:
            TOKEN = input('API-Token not found! Enter your code here: ')
            config["TOKEN"] = TOKEN

        # Save configs
        set_data.dump_config(config)

        exit(0)

    return config


def validate_config(config: dict):
    """
    Checks whether the config file contains all the necessary keys.
    This is needed when an update introduces new keys.
    :param config: Dictionary with the content of config.json
    :return: Updated config dictionary
    """
    keys_to_check = (
        "course_id", "course_name",
        "serie_id", "serie_name",
        "exercise_id", "exercise_name",
        "serie_token"
    )
    for key in keys_to_check:
        if key not in config:
            config[key] = None

    if "TOKEN" not in config:
        print("API token not found.")
        config = get_api_token(config)

    if "date_update_checked" not in config:
        config['date_update_checked'] = datetime.datetime.now().strftime("%Y-%m-%d")

    return config


def get_api_token(config: dict):
    """
    Asks the user for an API token and saves it
    :param config: Dictionary with the content of config.json
    :return: Updated config dictionary
    """
    config['TOKEN'] = input("Paste your API-token here: ")
    set_data.dump_config(config)

    return config
