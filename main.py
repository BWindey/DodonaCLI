import argparse
import http.client
import json


class ArgumentParser:
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
        self.add_arguments()
        self.args = None
        self.parse_args()

    def add_arguments(self):
        # Command-line arguments
        self.parser.add_argument("-c", "--show_courses",
                                 metavar='OPTION',
                                 nargs='?',
                                 choices=['a', 'm', 'i', 'f'],
                                 default='m',
                                 help="Show courses (a: all, m: my (default), i: institution, f: featured")

    def parse_args(self):
        self.args = self.parser.parse_args()


def show_courses(connection, headers, short_tab='m'):
    if short_tab == 'm':
        tab = 'my'
    elif short_tab == 'f':
        tab = 'featured'
    elif short_tab == 'i':
        tab = 'institution'
    elif short_tab == 'a':
        tab = 'all'
    else:
        return

    connection.request("GET", "/courses.json?tab=" + tab, headers=headers)
    res = connection.getresponse()
    print(res.status, res.reason)
    data = res.read()
    connection.close()

    pretty_json = json.dumps(json.loads(data), indent=2)
    print(pretty_json)


def main():
    token_file = open("token")
    TOKEN = token_file.read()[:-1]
    token_file.close()

    arg_parser = ArgumentParser("Dodona Command Line Interface (dodona.be)")
    print(arg_parser.args)

    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": TOKEN
    }

    if arg_parser.args.show_courses:
        print(arg_parser.args.show_courses)
        show_courses(connection, headers, arg_parser.args.show_courses)


if __name__ == "__main__":
    main()
