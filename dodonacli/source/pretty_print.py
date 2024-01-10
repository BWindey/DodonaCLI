import http.client
import json
import markdownify
import re
import shutil
import textwrap

from bs4 import BeautifulSoup
from rich.markdown import Markdown

from . import get_data, pretty_console


def print_courses_data(json_data, title="Your courses:", prefixes=None):
    """
    Print out the courses in json_data in a neat way
    :param json_data: json object with data about Dodona courses
    :param title: title to display above the courses-list
    :param prefixes: dictionary with a prefix for each id in json_data
    """
    if prefixes is None:
        prefixes = {}

    # List of tuples where each tuple represents a course by id, name and teacher
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['teacher']))

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_course_id_length = max(len(e[0]) for e in display_data)
    max_course_name_length = max(len(e[1]) for e in display_data)

    # Sort the courses by name
    display_data = sorted(display_data, key=lambda x: x[1])

    # Print out all courses in display_data
    pretty_console.console.print(f'\n[u bright_blue]{title}[/]')
    for course in display_data:
        pretty_console.console.print(
            (prefixes.get(course[0]) or "\t") + f"{course[0].ljust(max_course_id_length)}: "
            f"[bold]{course[1].ljust(max_course_name_length)}[/]\tby {course[2]}"
        )


def print_series_data(json_data, force=False, prefixes=None):
    """
    Print out the exercise-series in json_data in a neat way
    :param json_data: json object with data about Dodona exercise-series
    :param force: boolean to decide if the series description has to be printed, or only a link to it
    :param prefixes: dictionary with a prefix for each id in json_data
    """
    if prefixes is None:
        prefixes = {}

    # List of tuples where each tuple represents an exercise-series by id, name and description
    display_data = []

    for field in json_data:
        display_data.append(
            (
                str(field['id']),
                field['name'].strip(),
                field['description']
            )
        )

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_series_id_length = max(len(e[0]) for e in display_data)
    max_series_name_length = max(len(e[1]) for e in display_data)

    # Newline for clarity
    print()
    # Print out all the series in display_data while also handling the Markdown inside the series-description
    pretty_console.console.print("[u bright_blue]All series:[/]")
    for series in display_data:
        if force:
            description = series[2].split('\n')
            new_description = ''

            for line in description:
                line = line.rstrip()

                # Remove target pattern from links as they try to open the link in a new tab, not useful for terminal
                line = re.sub(r'{: target="_blank"}', '', line)

                # Replace Markdown bold to Rich Console bold
                line = re.sub(r'\*\*(.*?)\*\*', r'[bold]\1[/bold]', line)

                # Replace Markdown italics to Rich Console italics if it is not in a (link)
                pattern = re.compile(r'([ ,][^ (]*)_(.*?)_([^ ]*[ ,.])')
                line = pattern.sub(r'\1[i]\2[/i]\3', line)

                # Replace Markdown titles to something that appears as a title in terminal
                line = re.sub(r'##+ (.*)', r'[bold white]\1[/bold white]', line)

                # Split lines in multiple when they are too long for the terminal while keeping all lines indented.
                if len(line.replace("[bold]", "").replace("[/bold]", "")) > shutil.get_terminal_size().columns - 8:
                    line = line.split(" ")
                    new_line = ''
                    line_size = 0
                    for word in line:
                        if line_size + len(word) > shutil.get_terminal_size().columns - 8:
                            new_line += '\n'
                            line_size = 0
                        new_line += word + ' '
                        line_size += len(word + ' ')
                    line = new_line

                new_description += line + '\n'

            new_description = textwrap.indent(new_description, '\t')
            pretty_console.console.print(
                f"\t{series[0].ljust(max_series_id_length)}: "
                f"[bold]{series[1].ljust(max_series_name_length)}[/]"
                f"\n{new_description}")
        else:
            pretty_console.console.print(
                (prefixes.get(series[0]) or "\t") + f"{series[0].ljust(max_series_id_length)}: "
                f"[bold]{series[1].ljust(max_series_name_length)}[/]"
            )
    # Newline for clarity
    print()


def print_exercise_data(json_data, prefixes=None):
    """
    Print out the exercises in json_data in a neat way
    :param json_data: json object with data about Dodona exercises in a series
    :param prefixes: dictionary with a prefix for each id in json_data
    """
    if prefixes is None:
        prefixes = {}

    # List of tuples where each tuple represents an exercise by id, name, solved and has_attempt
    display_data = []

    for field in json_data:
        if field['type'] == "ContentPage":
            display_data.append({
                'type': "ContentPage",
                'id': str(field['id']),
                'name': field['name'],
                'has_read': field['has_read']
            })
        elif field['type'] == "Exercise":
            display_data.append({
                'type': "Exercise",
                'id': str(field['id']),
                'name': field['name'],
                # 'last_solution_is_best': field['last_solution_is_best'],
                'has_solution': field['has_solution'],
                # 'has_correct_solution': field['has_correct_solution'],
                'accepted': field['accepted']
            })

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_exercise_id_length = max(len(e['id']) for e in display_data)
    max_exercise_name_length = max(len(e['name']) for e in display_data)

    # Print out all exercises in display_data with indicator about solution-status: solved, wrong or not yet solved
    pretty_console.console.print('\n[u bright_blue]Exercises:[/]')
    for exercise in display_data:
        if exercise['type'] == "Exercise":
            if exercise['accepted']:
                solve_status = "[bold bright_green]SOLVED[/]"
            elif exercise['has_solution']:
                solve_status = "[bold bright_red]WRONG[/]"
            else:
                solve_status = "[bold]NOT YET SOLVED[/]"

            """
            if not exercise['has_solution']:
                solve_status = "[bold]NOT YET SOLVED[/]"
            elif exercise['last_solution_is_best'] and exercise['has_correct_solution']:
                solve_status = "[bold bright_green]SOLVED[/]"
            else:
                solve_status = "[bold bright_red]WRONG[/]"
            """

        elif exercise['type'] == "ContentPage":
            if exercise['has_read']:
                solve_status = "[bold bright_green]READ[/]"
            else:
                solve_status = "[bold]NOT YET READ[/]"

        else:
            solve_status = "[bold]SOLVE STATUS UNKNOWN"

        pretty_console.console.print(
            (prefixes.get(exercise['id']) or "\t") + f"{exercise['id'].ljust(max_exercise_id_length)}: "
            f"[bold]{exercise['name'].ljust(max_exercise_name_length)}[/]\t"
            + solve_status
        )
    print()


def print_exercise(json_data, token: str, force=False):
    """
    Print out the exercise-description. Needs to call the Dodona-sandbox and convert HTML to text.
    Prints out a warning for potential incompleteness, which may be dangerous for tests and exams.
    :param token: API-token as authorization
    :param json_data: json object with info about a Dodona exercise
    :param force: boolean to decide if the exercise description has to be printed, or only a link to it
    """
    if json_data['type'] == 'ContentPage':
        pretty_console.console.print(
            "\nNo need to program anything this time, but you'll have to go read this and mark it as read:\n"
            + json_data['url'].replace(".json", "") + '\n'
        )

    elif not force:
        pretty_console.console.print("\nYou can find the description at \n" + json_data['description_url'] + '\n')

    else:
        # Print the HTML with warnings
        pretty_console.console.print(
            "\n[bold bright_red]![/] [u bold bright_red]WARNING:[/] the description may not be correct, "
            "DO NOT rely on this for exams and tests!!\n"
            "[bold bright_red]![/] Instead, use this url: " + json_data['description_url'] + '\n'
        )

        pretty_console.console.print(
            '\n'
            "Expected programming language: " + json_data['programming_language']['name'] +
            '\n'
        )

        # Make sandbox.dodona connection for exercise description:
        sandbox = http.client.HTTPSConnection("sandbox.dodona.be")
        headers = {"Authorization": token}

        stripped_link = json_data['description_url'].replace("https://sandbox.dodona.be", "", 1)
        sandbox.request("GET", stripped_link, headers=headers)

        data = get_data.handle_connection_response(sandbox).decode()

        soup = BeautifulSoup(data, features="html.parser")
        html_description = str(soup.find("div", {"class": "card-supporting-text"}))

        md_description = markdownify.markdownify(html_description)

        md = Markdown(md_description)

        pretty_console.console.print(md)

        # Print the HTML with warnings
        pretty_console.console.print(
            "\n[bold bright_red]![/] [u bold bright_red]WARNING:[/] the description may not be correct, "
            "DO NOT rely on this for exams and tests!!\n"
            "[bold bright_red]![/] Instead, use this url: " + json_data['description_url'] + '\n'
        )


def print_result(json_results):
    """
    Print out the results of a submission in a neat way
    :param json_results: json object with data about a submission
    """
    if json_results['accepted']:
        # Everything passed, well done!
        pretty_console.console.print("[bold bright_green]All tests passed![/] You can continue to next exercise.")
    else:
        try:
            if json_results['status'] in ("memory limit exceeded", "test"):
                print("\t" + json_results['description'])
                return

            # There were some problems, list them here
            for group in json_results['groups']:
                print(group['description'] + ": " + str(group['badgeCount']) + " tests failed.")

                if group['badgeCount'] > 0:
                    print("Failed exercises:")
                    for test in group['groups']:
                        if not test['accepted']:
                            pass
                            print("\t- " + test['groups'][0]['description'] + "\n\t\t" +
                                  test['groups'][0]['description']['description'])
        except Exception as e:
            print("\tSomething went wrong trying to display the results: " + str(e))


def print_status(config):
    pretty_console.console.print(f"\n[u bright_blue]Status:[/]\n"
                                 f"\t{'Course: '.ljust(10)}{config['course_name']}\n"
                                 f"\t{'Series: '.ljust(10)}{config['serie_name']}\n"
                                 f"\t{'Exercise: '.ljust(10)}{config['exercise_name']}\n")


def print_exercise_submissions(json_data):
    pretty_console.console.print(
        "\n[u bright_blue]Most recent submissions:[/]"
    )
    for i, submission in enumerate(json_data[:10]):
        if submission['accepted']:
            accepted_emoji = "[bright_green]:heavy_check_mark:[/bright_green]"
        else:
            accepted_emoji = "[bright_red]:heavy_multiplication_x:[/bright_red]"

        status = submission['status']
        if submission['status'] in ("memory limit exceeded", "geheugenlimiet overschreden"):
            status += "\n\t\t\tWow, how did you do that?"

        pretty_console.console.print(
            f"\t{accepted_emoji}  [link={submission['url'].rstrip('.json')}]#{len(json_data) - i: <2}[/link]"
            f"\t{status}\t"
        )

    print()


def print_all_submissions(connection, headers, json_data):
    pretty_console.console.print(
        "\n[u bright_blue]Most recent submissions:[/]"
    )

    for i, submission in enumerate(json_data):
        if submission['accepted']:
            accepted_emoji = "[bright_green]:heavy_check_mark:[/bright_green]"
        else:
            accepted_emoji = "[bright_red]:heavy_multiplication_x:[/bright_red]"

        status = submission['status']

        exercise_link = submission['exercise'].replace("https://dodona.be/nl", "", 1)
        connection.request("GET", exercise_link, headers=headers)
        json_exercise_data = json.loads(get_data.handle_connection_response(connection))

        exercise_name = json_exercise_data['name']

        pretty_console.console.print(
            f"\t{accepted_emoji}  [link={submission['url'].rstrip('.json')}]#{len(json_data) - i: <2}[/link]"
            f"\t{status}"
            f"\t\t\t{exercise_name}"
        )
    print()
