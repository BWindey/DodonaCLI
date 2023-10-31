import json
import os

from set_data import dump_config


def courses_data(connection, headers):
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
    connection.request("GET", "/courses/" + course_id + "/series.json", headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print("Error connecting to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return
    data = res.read()
    connection.close()

    return json.loads(data)


def get_configs():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')

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
        dump_config(config)

    return config
