import http.client
import json
import click


def show_the_courses(connection, headers, short_tab='m'):
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


@click.command()
@click.option('--show_courses', '-c',
              help="")
def main(show_courses):
    token_file = open("token")
    TOKEN = token_file.read()[:-1]
    token_file.close()

    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": TOKEN
    }

    if show_courses:
        print(show_courses)
        show_the_courses(connection, headers, show_courses)


if __name__ == "__main__":
    main()
