"""
This file will contain everything needed to provide a tutorial to first-time users.
It uses "The Coder's Apprentice" featured course on Dodona.
"""
import http.client
import json
import os

import dodonacli.source.get_data
from . import pretty_print, pretty_console, set_data


def start_tutorial(config: dict):
    """
    Runs the tutorial and asks for API token if it wasn't present yet.
    :param config: dict
    :return: config: dict
    """
    # Clear screen for tutorial
    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        "Welcome to the Dodona CLI,\n"
        "this tutorial will show you everything you need to interact\n"
        "with Dodona from your terminal.\n"
    )
    input(" <Enter to continue>")

    # Clear previously selected configs
    config['serie_id'], config['serie_name'] = None, None
    config['exercise_name'], config['exercise_name'] = None, None

    if "TOKEN" not in config:
        os.system('cls' if os.name == 'nt' else 'clear')
        pretty_console.console.print(
            "Before we begin, we'll need an API-token to authorize your\n"
            "connection with Dodona.\n"
            "You can find it on your profile page on https://dodona.be\n"
        )
        config = dodonacli.source.get_data.get_api_token(config)

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


def tutorial_handle_connection(config: dict, connection: http.client.HTTPSConnection):
    res = connection.getresponse()
    status = res.status

    if status != 200:
        if status == 401:
            print("Authorization didn't work, "
                  "please re-enter your API-token and make sure it's correct.")
            config = dodonacli.source.get_data.get_api_token(config)
            set_data.dump_config(config)

        else:
            pretty_console.console.print("Error connecting to Dodona: " + str(status))
            pretty_console.console.print("Reason: " + res.reason)

        pretty_console.console.print(
            "Tutorial will terminate due to error, "
            "you can start again with `dodona tutorial`"
        )
        exit(-1)

    data = res.read()
    connection.close()

    return json.loads(data)


def tutorial_select_course(config: dict, connection: http.client.HTTPSConnection,
                           headers: dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "Use the command `dodona display` to show the available courses."
    )

    command = input("$ ")

    while command.rstrip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/courses?tab=featured", headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_courses_data(json_data, "Featured courses")

    pretty_console.console.print(
        "\nSelect now \"The Coder's Apprenctice\" with `dodona select` + the courses id,"
        "\nor (distinct part of) the courses name"
    )
    command = input("$ ")

    while not command.lstrip().startswith("dodona select"):
        print("\tThat was not the right command, please try again")
        command = input("$ ")

    dod, sel, course = command.split()
    if (len(command.split()) < 3 or
            course != "296" and course.lower() not in "The Coder's Apprentice".lower()):
        pretty_console.console.print(
            "\t[red]Watch out[/], you used a wrong id or name to select"
            "\"The Coder's Apprentice\"!\n"
            "\tThe tutorial will continue as if you selected it right,"
            "but pay attention next time."
        )

    config['course_id'] = 296
    config['course_name'] = "The Coder's Apprentice"

    pretty_console.console.print(
        "The course is now selected, let's continue with selecting an exercise-series.\n"
    )
    input(" <Enter to continue>")

    return config


def tutorial_select_series(config: dict, connection: http.client.HTTPSConnection,
                           headers: dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "Use the command `dodona display` to show the available exercise-series."
    )
    command = input("$ ")

    while command.strip() != "dodona display":
        print("\nThat was not the right command, please try again")
        command = input("$ ")

    connection.request(
        "GET", "/courses/" + str(config['course_id']) + '/series',
        headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    # To prevent the screen being blasted with a lot of text,
    # only print out the first 6 exercise series
    pretty_print.print_series_data(json_data[:6])

    pretty_console.console.print(
        "Select now \"2. Using Python\" with `dodona select` + the series' id,"
        "\nor (distinct part of) the series' name."
    )
    command = input("$ ")

    while not command.lstrip().startswith("dodona select"):
        print("\nThat was not the right command, please try again")
        command = input("$ ")

    dod, sel, series = command.split()
    if (len(command.split()) < 3
            or series != "2592" and series.lower() not in "2. Using Python".lower()):
        pretty_console.console.print(
            "\tWatch out, you used a wrong id or name to select \"2. Using Python\"!\n"
            "\tThe tutorial will continue as if you selected it right,"
            "but pay attention next time."
        )

    config['serie_id'] = 2592
    config['serie_name'] = "2. Using Python"

    pretty_console.console.print(
        "\nWith the exercise-series now selected, it's time to introcude `dodona status`, "
        "give it a try!"
    )
    command = input("$ ")

    while not command.strip() == "dodona status":
        print("\tThat was not the right command, please try again")
        command = input("$ ")

    pretty_print.print_status(config)
    print("Fantastic, let's move on to selecting an exercise.\n")
    input(" <Enter to continue>")

    return config


def tutorial_select_exercise(config: dict, connection: http.client.HTTPSConnection,
                             headers: dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "Use the command `dodona display` to show the available exercises."
    )
    command = input("$ ")

    while command.strip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request(
        "GET",
        "/series/" + str(config['serie_id']) + '/activities',
        headers=headers
    )
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_exercise_data(json_data)

    pretty_console.console.print(
        "Select now \"Hello, World!\" with `dodona select` + the series' id,\n"
        "or (distinct part of) the series' name."
    )
    command = input("$ ")

    while not command.lstrip().startswith("dodona select"):
        print("That was not the right command, please try again")
        command = input("$ ")

    dod, sel, exercise = command.split()
    if (len(command.split()) < 3
            or exercise != "1399231809" and exercise.lower() not in "Hello, World!".lower()):
        pretty_console.console.print(
            "\tWatch out, you used a wrong id or name to select \"2. Using Python\"!\n"
            "\tThe tutorial will continue as if you selected it right, "
            "but pay attention next time."
        )

    config['exercise_id'] = 1399231809
    config['exercise_name'] = "Hello, World!"

    # This exercise has boilerplate code
    with open('boilerplate.py', 'w') as boilerplate:
        boilerplate.write(json_data[5]['boilerplate'])

    pretty_console.console.print(
        "This exercise has some boilerplate code attached to it,\n"
        "here is its content:\n|\t"
        + json_data[5]['boilerplate'].strip()
        + "\nNormally, this file will be saved to your disk, "
          "with the file-extension of the programming-language of the exercise.\n"
    )

    pretty_console.console.print(
        "The exercise is now selected, let's move on to viewing an exercise description.\n"
    )
    input(" <Enter to continue>")

    return config


def tutorial_view_exercise(config: dict, connection: http.client.HTTPSConnection,
                           headers: dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "Use the command `dodona display` to show the description of the exercise."
    )
    command = input("$ ")

    while command.strip() != "dodona display":
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request(
        "GET",
        f"/courses/{str(config['course_id'])}"
        + f"/series/{str(config['serie_id'])}"
        + f"/activities/{str(config['exercise_id'])}",
        headers=headers)

    json_data = tutorial_handle_connection(config, connection)
    pretty_print.print_exercise(json_data, config['TOKEN'])

    input(" <Enter to continue>")


def tutorial_post_exercise(config: dict, connection: http.client.HTTPSConnection,
                           headers: dict):
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "Now you can post the solution. You don't need to write any code for this exercise, \n"
        "as it is already writtin in the 'boilerplate.py'-file.\n"
        "You can post it with the command `dodona post <SOLUTION_FILE_NAME>`.\n"
        "Replace <SOLUTION_FILE_NAME> with the correct file-name, in this case 'boilerplate.py'."
    )
    command = input("$ ")

    while command.strip() != "dodona post boilerplate.py":
        print("That was not the right command, please try again")
        command = input("$ ")

    set_data.post_solution(
        "print( \"Hello, world!\" )",
        connection, headers, config['course_id'], config['exercise_id']
    )

    pretty_console.console.print(
        "Nice, programmed that like a pro.\n"
        "You're nearly done with this tutorial, I want to show you one last thing. \n"
    )
    input(" <Enter to continue>")


def tutorial_conclude(config: dict) -> dict:
    os.system('cls' if os.name == 'nt' else 'clear')
    pretty_console.console.print(
        "It's time deselect everything. You can do this with the "
        "'up' command + a selection from [1|2|3|all|top].\n"
        "The numbers specify the amount of levels you'll deselect, while all/top deselects "
        "everything at once."
    )

    command = input("$ ")

    # Parse input
    while not command.rstrip().startswith("dodona up"):
        print("That wasn't the right command, please try again.")
        command = input("$ ")

    # Deselect everything (except the token)
    all_configs = list(config.keys())
    all_configs.remove("TOKEN")

    for conf in all_configs:
        config[conf] = None

    # Print the right message
    amount = command.replace("dodona up", "").strip()
    print()
    if amount in ("all", "top", "3"):
        print("Deselected everything")
    elif amount.isnumeric():
        print("Deselected everything to save on time. Normally this would "
              "deselect " + amount + " levels")
    else:
        print("You didn't enter a valid amount, but I'll let it slip now.\n"
              "Deselected everything.")

    # End of tutorial
    pretty_console.console.print(
        "\nRemember you can always use `dodona \[subcommand\] --help` to get "
        "help with all the subcommands.\n"
        "Additionally there is a manual-page you can download "
        "from https://www.github.com/BWindey/DodonaCLI .\n"
        "I would strongly encourage you to read through the README there as well."
    )

    return config
