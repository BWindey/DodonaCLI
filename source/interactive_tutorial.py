"""
This file will contain everything needed to provide a tutorial to first-time users.
"""
import http.client
import json

from . import set_data
from . import pretty_print


def start_tutorial(config):
    print("Welcome to DodonaCLI, "
          "this tutorial will show you everything you need to interact with Dodona from your terminal.")

    if "TOKEN" not in config:
        print("\nBefore we begin, we'll need an API-token to authorize your connection with Dodona. "
              "You can find it on your profile page on https://dodona.be\n")

        config = tutorial_get_api_token(config)

    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    config = tutorial_select_course(config, connection, headers)

    return config


def tutorial_get_api_token(config):
    config['TOKEN'] = input("Paste your API-token here: ")
    set_data.dump_config(config)

    return config


def tutorial_handle_connection(config, connection):
    res = connection.getresponse()
    status = res.status

    if status != 200:
        if status == 401:
            print("Authorization didn't work, please re-enter your API-token and make sure it's correct.")
            config = tutorial_get_api_token(config)
            set_data.dump_config(config)

        else:
            print("Error connecting to Dodona: " + str(status))
            print("Reason: " + res.reason)

        print("Tutorial will terminate due to error, you can start again with `dodona --tutorial`")
        exit(-1)

    data = res.read()
    connection.close()

    return json.loads(data)


def tutorial_select_course(config, connection, headers):
    print("\n Now use the command `dodona --display` to show the available courses. "
          "Alternatively, you can also use the short '-d' flag.")
    command = input("$ ")

    while command.rstrip() not in ("dodona --display", "dodona -d"):
        print("That was not the right command, please try again")
        command = input("$ ")

    connection.request("GET", "/courses?tab=featured", headers=headers)
    json_data = tutorial_handle_connection(config, connection)

    pretty_print.print_courses_data(json_data)

    print("Select now \"The Coder's Apprenctice\" with `dodona --select` + "
          "the course_id, or (distinct part of) the course_name")
    command = input("$ ")

    while not command.rstrip().startswith("dodona --select") and not command.rstrip().startswith("dodona -s"):
        print("That was not the right command, please try again")
        command = input("$ ")

    if command.split()[2] != "296" and command.split()[2].lower() not in "The Coder's Apprentice".lower():
        print("Watch out, you used a wrong id or name to select \"The Coder's Apprentice\"!\n"
              "The tutorial will continue as if you selected it right, but pay attention next time.")

    config['course_id'] = 296
    config['course_name'] = "The Coder's Apprentice"

    print("\nThe course is now selected, use `dodona --status` to view your selection:")
    command = input("$ ")

    while not command.rstrip() == "dodona --status":
        print("That was not the right command, please try again")
        command = input("$ ")

    pretty_print.print_status(config)
    print("\n Fantastic, let's move on to selecting an exercise series.")

    return config
