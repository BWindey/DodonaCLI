import json
import os


def select_course(course):
    print('selecting course ' + course)
    return


def select_serie(serie):
    print('selecting serie ' + serie)
    return


def select_exercise(exercise):
    print('selecting exercise ' + exercise)
    return


def dump_config(config):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')

    with open(config_file_path, 'w') as config_file:
        json.dump(config, config_file)


def post_solution(content, connection, headers, config):
    payload = {
        "submission": {
            "code": content,
            "course_id": config['course_id'],
            "exercise_id": config['exercise_id']
        }
    }
    json_payload = json.dumps(payload)

    connection.request("POST", "/submissions.json", json_payload, headers=headers)
    res = connection.getresponse()
    if res.status != 200:
        print("Error connection to Dodona: " + str(res.status))
        print("Reason: " + res.reason)
        return

    print(res.read().decode())
    return
