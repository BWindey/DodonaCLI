"""
This file will contain everything needed to provide a tutorial to first-time users.
"""
import http.client
import json

from . import set_data


def start_tutorial(config):
    print("Welcome to DodonaCLI, "
          "this tutorial will show you everything you need to interact with Dodona from your terminal.")
    print("\nBefore we begin, we'll need an API-token to authorize your connection with Dodona."
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
    return config


def tutorial_handle_connection(config, connection, headers):
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
    json_data = tutorial_handle_connection(config, connection, headers)

    return config
