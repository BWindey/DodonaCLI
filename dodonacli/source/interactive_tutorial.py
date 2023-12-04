"""
This file will contain everything needed to provide a tutorial to first-time users.
It uses "The Coder's Apprentice" featured course on Dodona.
"""
import http.client
import json
import os

from . import pretty_print, pretty_console, set_data


def start_tutorial(config: dict):
    """
    Runs the tutorial and asks for API token if it wasn't present yet.
    :param config: dict
    :return: config: dict
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nWelcome to the Dodona CLI, "
          "this tutorial will show you everything you need to interact with Dodona from your terminal.")

    config['serie_id'], config['serie_name'], config['exercise_id'], config['exercise_name'] = None, None, None, None

    if "TOKEN" not in config:
        pretty_console.console.print(
            "\n\nBefore we begin, we'll need an API-token to authorize your connection with Dodona. "
            "You can find it on your profile page on https://dodona.be")

        config = tutorial_get_api_token(config)

    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    config = tutorial_select_course(config, connection, headers)
    config = tutorial_select_series(config, connection, headers)
    config = tutorial_select_exercise(config, connection, headers)
    tutorial_view_exercise(config, connection, headers)
    tutorial_post_exercise(config, connection, headers)

    config = tutorial_conclude(config)

    return config


def tutorial_get_api_token(config: dict):
    config['TOKEN'] = input("Paste your API-token here: ")
    set_data.dump_config(config)

    return config


def tutorial_handle_connection(config: dict, connection: http.client.HTTPSConnection):
    res = connection.getresponse()
    status = res.status

    if status != 200:
        if status == 401:
            print("Authorization didn't work, please re-enter your API-token and make sure it's correct.")
            config = tutorial_get_api_token(config)
            set_data.dump_config(config)

        else:
            pretty_console.console.print("Error connecting to Dodona: " + str(status))
            pretty_console.console.print("Reason: " + res.reason)

        pretty_console.console.print("Tutorial will terminate due to error, you can start again with `dodona tutorial`")
        exit(-1)

    data = res.read()
    connection.close()

    return json.loads(data)


def tutorial_select_course(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    pretty_console.console.print("\n\n\nUse the command `dodona display` to show the available courses.")

    command = input("$ ")

    while command.rstrip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/courses?tab=featured", headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_courses_data(json_data, "Featured courses")

    pretty_console.console.print("Select now \"The Coder's Apprenctice\" with `dodona select` + "
                                 "the courses id, or (distinct part of) the courses name")
    command = input("$ ")

    while not command.rstrip().startswith("dodona select"):
        print("That was not the right command, please try again")
        command = input("$ ")

    if (len(command.split()) < 3 or
            command.split()[2] != "296" and command.split()[2].lower() not in "The Coder's Apprentice".lower()):
        pretty_console.console.print(
            "Watch out, you used a wrong id or name to select \"The Coder's Apprentice\"!\n"
            "The tutorial will continue as if you selected it right, but pay attention next time."
        )

    config['course_id'] = 296
    config['course_name'] = "The Coder's Apprentice"

    pretty_console.console.print("\nThe course is now selected, use `dodona status` to view your selection:")
    command = input("$ ")

    while not command.rstrip() == "dodona status":
        print("That was not the right command, please try again")
        command = input("$ ")

    pretty_print.print_status(config)
    print("Fantastic, let's move on to selecting an exercise series.")

    return config


def tutorial_select_series(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    pretty_console.console.print("\n\n\nUse the command `dodona display` to show the available exercise-series. ")

    command = input("$ ")

    while command.rstrip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/courses/" + str(config['course_id']) + '/series', headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    # To prevent the screen being blasted with a lot of text, only print out the first 6 exercise series
    pretty_print.print_series_data(json_data[:6])

    pretty_console.console.print("Select now \"2. Using Python\" with `dodona select` + "
                                 "the series' id, or (distinct part of) the series' name")
    command = input("$ ")

    while not command.rstrip().startswith("dodona select"):
        print("That was not the right command, please try again")
        command = input("$ ")

    if (len(command.split()) < 3
            or command.split()[2] != "2592" and command.split()[2].lower() not in "2. Using Python".lower()):
        pretty_console.console.print(
            "Watch out, you used a wrong id or name to select \"2. Using Python\"!\n"
            "The tutorial will continue as if you selected it right, but pay attention next time."
        )

    config['serie_id'] = 2592
    config['serie_name'] = "2. Using Python"

    pretty_console.console.print("\nThe exercise-series is now selected, use `dodona status` to view your selection:")
    command = input("$ ")

    while not command.rstrip() == "dodona status":
        print("That was not the right command, please try again")
        command = input("$ ")

    pretty_print.print_status(config)
    print("Fantastic, let's move on to selecting an exercise.")

    return config


def tutorial_select_exercise(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    pretty_console.console.print("\n\n\nUse the command `dodona display` to show the available exercises. ")

    command = input("$ ")

    while command.rstrip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/series/" + str(config['serie_id']) + '/activities', headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_exercise_data(json_data)

    pretty_console.console.print("Select now \"Hello, World!\" with `dodona select` + "
                                 "the series' id, or (distinct part of) the series' name")
    command = input("$ ")

    while not command.rstrip().startswith("dodona select"):
        print("That was not the right command, please try again")
        command = input("$ ")

    if (len(command.split()) < 3 or
            command.split()[2] != "1399231809" and command.split()[2].lower() not in "Hello, World!".lower()):
        pretty_console.console.print(
            "Watch out, you used a wrong id or name to select \"2. Using Python\"!\n"
            "The tutorial will continue as if you selected it right, but pay attention next time."
        )

    config['exercise_id'] = 1399231809
    config['exercise_name'] = "Hello, World!"

    # This exercise has boilerplate code
    with open('boilerplate', 'w') as boilerplate:
        boilerplate.write(json_data[5]['boilerplate'])
    print(
        "\nThis exercise has some boilerplate code attached to it, you can view it in the boilerplate file, or here:\n"
        " |\t" + json_data[5]['boilerplate']
    )

    pretty_console.console.print("\nThe exercise is now selected, use `dodona status` to view your selection:")
    command = input("$ ")

    while not command.rstrip() == "dodona status":
        print("That was not the right command, please try again")
        command = input("$ ")

    pretty_print.print_status(config)
    print("Fantastic, let's move on to viewing an exercise description.")

    return config


def tutorial_view_exercise(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    pretty_console.console.print("\n\n\nUse the command `dodona display` to show the description of the exercise. ")

    command = input("$ ")

    while command.rstrip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/courses/" + str(config['course_id'])
                       + "/series/" + str(config['serie_id'])
                       + '/activities/' + str(config['exercise_id']),
                       headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_exercise(json_data, config['TOKEN'])


def tutorial_post_exercise(config: dict, connection: http.client.HTTPSConnection, headers: dict):
    pretty_console.console.print(
        "\n\n\nNow you can post the solution. You don't need to write any code for it, as it is already writtin in "
        "the 'boilerplate'-file. You can post it by writing `dodona post <SOLUTION_FILE_NAME>`."
        "Replace <SOLUTION_FILE_NAME> with the correct file-name, in this case 'boilerplate'.")

    command = input("$ ")

    while command.rstrip() != "dodona post boilerplate":
        print("That was not the right command, please try again")
        command = input("$ ")

    with open('boilerplate', 'r') as solution_file:
        set_data.post_solution(solution_file.read(), connection, headers, config)


def tutorial_conclude(config: dict):
    pretty_console.console.print(
        "\nAlmost done, now deselect everything with `dodona uptop` and you're ready to use DodonaCLI."
        "\nRemember you can always use `dodona --help` to view all available commands and flags.")

    command = input("$ ")

    while command.rstrip() != "dodona uptop":
        print("That was not the right command, please try again")
        command = input("$ ")

    for e in ('exercise_id', 'exercise_name', 'serie_id', 'serie_name', 'course_id', 'course_name'):
        config[e] = None

    return config
