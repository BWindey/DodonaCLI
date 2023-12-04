import json
import os

from . import set_data, interactive_tutorial


def handle_connection(connection):
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


def courses_data(connection, headers):
    """
    Get registred courses of user
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :return: json object with info about available courses
    """
    connection.request("GET", "/courses?tab=my", headers=headers)
    data = handle_connection(connection)

    return json.loads(data)


def series_data(connection, headers, course_id):
    """
    Get all exercise-series of course
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param course_id: int id of the course to find series from
    :return: json object with info about available series
    """
    connection.request("GET", "/courses/" + course_id + "/series", headers=headers)
    data = handle_connection(connection)

    return json.loads(data)


def exercises_data(connection, headers, series_id):
    """
    Get all exercises of exercise-serie
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param series_id: int id of exercise-series
    :return: json object with info about available exercises
    """
    connection.request("GET", "/series/" + series_id + "/activities", headers=headers)
    data = handle_connection(connection)

    return json.loads(data)


def exercise_data(connection, headers, course_id, exercise_id):
    """
    Get exercise-info for selected exercise
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param course_id: int id of course
    :param exercise_id: int id of exercise
    :return: json object with info about exercise
    """
    connection.request("GET", "/courses/" + course_id + "/activities/" + exercise_id, headers=headers)
    data = handle_connection(connection)

    return json.loads(data)


def exercise_submissions(config, connection, headers):
    course_id = config['course_id']
    series_id = config['serie_id']
    exercise_id = config['exercise_id']

    connection.request("GET", f"/courses/{course_id}/series/{series_id}/activities/{exercise_id}/submissions",
                       headers=headers)
    data = handle_connection(connection)

    return json.loads(data)


def get_configs():
    """
    Get config data from config.json
    :return: json object with config data
    """
    # Get path of the config-file. This is a bit more complicated because this file exists at the same directory as
    # the python files, but the command may be executed from anywhere with the apropriate alias set.
    # Thus, first te path to the directory of the python files is retrieved, then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, '../../config.json')

    # First try to open, if unable to open, create new config-file and ask user for a token
    try:
        with open(config_file_path, "r") as file:
            config = json.load(file)

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
