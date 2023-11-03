import json
import os

from set_data import dump_config


def courses_data(connection, headers):
    """
    Get registred courses of user
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :return: json object with info about available courses
    """
    connection.request("GET", "/courses.json?tab=my", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print('Error connecting to dodona: ' + str(res.status))
        print(res.reason)
        return
    data = res.read()
    connection.close()

    json_data = json.loads(data)

    return json_data


def series_data(connection, headers, course_id):
    """
    Get all exercise-series of course
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param course_id: int id of the course to find series from
    :return: json object with info about available series
    """
    connection.request("GET", "/courses/" + course_id + "/series.json", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print("Error connecting to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return
    data = res.read()
    connection.close()

    return json.loads(data)


def exercises_data(connection, headers, series_id):
    """
    Get all exercises of exercise-serie
    :param connection: HTTPSConnection object to the main Dodona page
    :param headers: Dict with extra info, mainly autorization needed
    :param series_id: int id of exercise-series
    :return: json object with info about available exercises
    """
    connection.request("GET", "/series/" + series_id + "/activities.json", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print("Error connection to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return
    data = res.read()
    connection.close()

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
    connection.request("GET", "/courses/" + course_id + "/activities/" + exercise_id + ".json", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print("Error connection to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return
    data = res.read()
    json_data = json.loads(data)
    connection.close()

    return json_data


def get_configs():
    """
    Get config data from config.json
    :return: json object with config data
    """
    # Get path of the config-file. This is a bit more complicated because this file exists at the same directory as
    # the python files, but the command may be executed from anywhere with the apropriate alias set.
    # Thus, first te path to the directory of the python files is retrieved, then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')

    # First try to open, if unable to open, create new config-file and ask user for a token
    try:
        with open(config_file_path, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}
        TOKEN = input('\033[1;91mAPI-Token not found!\033[0m Enter your code here: ')
        config["TOKEN"] = TOKEN
        config["course_id"] = None
        config["serie_id"] = None
        config["exercise_id"] = None
        # Save configs
        dump_config(config)

    return config
