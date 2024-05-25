from .pretty_printer import custom_print


def print_courses_data(json_data: dict, settings: dict, title: str = "Your courses:", prefixes: dict = None):
    """
    Print out the courses in json_data in a neat way
    :param json_data: json object with data about Dodona courses
    :param settings: dict with settings
    :param title: title to display above the courses-list
    :param prefixes: dictionary with a prefix for each id in json_data
    """
    if prefixes is None:
        prefixes = {}

    # List of tuples where each tuple represents a course by id, name and teacher
    display_data: list[tuple] = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['teacher']))

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_course_id_length = max(len(e[0]) for e in display_data)
    max_course_name_length = max(len(e[1]) for e in display_data)

    # Print out all courses in display_data
    result = f'[u bright_blue]{title}[/]\n'
    for course in display_data:
        result += (prefixes.get(course[0]) or "\t")
        result += (f"{course[0].ljust(max_course_id_length)}: [bold]"
                   f"{course[1].ljust(max_course_name_length)}[/]\tby {course[2]}\n")

    custom_print(result.strip(), settings, pretty=True)


def print_series_data(json_data: dict, settings: dict, force: bool = False, prefixes: dict = None):
    """
    Print out the exercise-series in json_data in a neat (unless force) way.
    :param json_data: Json object with data about Dodona exercise-series
    :param settings: dict with settings
    :param force: Boolean to decide if the series description has to be printed, or only a link to it
    :param prefixes: Dictionary with a prefix for each id in json_data
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

    # Print out all the series in display_data while also handling the Markdown inside the series-description
    result = "[u bright_blue]All series:[/]\n"
    if force:
        import markdownify
        import re
        from rich.markdown import Markdown
        from rich.padding import Padding
        from dodonacli.source import pretty_console

        pretty_console.console.print('\n' * settings['new_lines_above'] + result, end='')

        for i, series in enumerate(display_data):
            description = series[2].strip('\n')
            description = re.sub(r'{: *target="_blank"}', '', description).strip()
            md_description = Markdown(markdownify.markdownify(description))

            pretty_console.console.print(
                f"\t{series[0].ljust(max_series_id_length)}: "
                f"[bold]{series[1].ljust(max_series_name_length)}[/]"
            )
            pretty_console.console.print(
                Padding(
                    md_description,
                    pad=(0, 0, 1 if description and i + 1 < len(display_data) else 0, 12)
                ), end=''
            )
        print('\n' * settings['new_lines_below'], end='')

    else:
        for i, series in enumerate(display_data):
            result += prefixes.get(series[0]) or "\t"
            result += f"{series[0].ljust(max_series_id_length)}: [bold]{series[1].ljust(max_series_name_length)}[/]\n"

        custom_print(result.strip(), settings, pretty=True)


def print_exercise_data(json_data: dict, settings: dict, prefixes: dict = None):
    """
    Print out the exercises in json_data in a neat way
    :param json_data: json object with data about Dodona exercises in a series
    :param settings: dict with settings
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
    result = '[u bright_blue]Exercises:[/]\n'
    for exercise in display_data:
        if exercise['type'] == "Exercise":
            if exercise['accepted']:
                solve_status = "[bold bright_green]SOLVED[/]"
            elif exercise['has_solution']:
                solve_status = "[bold bright_red]WRONG[/]"
            else:
                solve_status = "[bold]NOT YET SOLVED[/]"

        elif exercise['type'] == "ContentPage":
            if exercise['has_read']:
                solve_status = "[bold bright_green]READ[/]"
            else:
                solve_status = "[bold]NOT YET READ[/]"

        else:
            solve_status = "[bold]SOLVE STATUS UNKNOWN"

        result += (prefixes.get(exercise['id']) or "\t")
        result += f"{exercise['id'].ljust(max_exercise_id_length)}: "
        result += f"[bold]{exercise['name'].ljust(max_exercise_name_length)}[/]\t" + solve_status + '\n'

    custom_print(result.strip(), settings, pretty=True)


def print_exercise(json_data: dict, token: str, settings: dict, force: bool = False):
    """
    Print out the exercise-description.
    Needs to call the Dodona sandbox and convert HTML to text.
    Print out a warning for potential incompleteness, which may be dangerous for tests and exams.
    :param token: API-token as authorization
    :param json_data: json object with info about a Dodona exercise
    :param force: boolean to decide if the exercise description has to be printed, or only a link to it
    :param settings: dict with settings
    """
    if json_data['type'] == 'ContentPage':
        custom_print(
            "No need to program anything this time, but you'll have to go read this and mark it as read:\n"
            + json_data['url'].replace(".json", ""),
            settings, pretty=True
        )

    elif not force:
        custom_print(
            f"You can find the exercise description at \n{json_data['description_url']}",
            settings,
            pretty=True
        )

    else:
        import http.client
        import markdownify
        from bs4 import BeautifulSoup
        from rich.markdown import Markdown
        from rich.padding import Padding
        from dodonacli.source import get_data, pretty_console

        custom_print(
            "Expected programming language: " + json_data['programming_language']['name'] + '\n',
            {'new_lines_above': settings['new_lines_above']},
            pretty=True
        )

        # Make sandbox.dodona connection for exercise description:
        sandbox = http.client.HTTPSConnection("sandbox.dodona.be")
        headers = {"Authorization": token}

        stripped_link = json_data['description_url'].replace("https://sandbox.dodona.be", "", 1)
        sandbox.request("GET", stripped_link, headers=headers)

        data = get_data.handle_connection_response(sandbox).decode()

        soup = BeautifulSoup(data, features="html.parser")
        html_description = str(soup.find("div", {"class": "card-supporting-text"}))

        md_description = markdownify.markdownify(html_description).strip()

        md = Markdown(md_description)

        if settings['paste_force_warning']:
            # Print the HTML with warnings
            warning = (
                    "\n[u bold bright_red]WARNING:[/] the description may be incorrect, "
                    "DO NOT rely on this for exams and tests!\n"
                    "View in browser: " + json_data['description_url'] + '\n'
            )
            pretty_console.console.print(warning)
            pretty_console.console.print(Padding(md, pad=(0, 0, 0, 3)))
            pretty_console.console.print(warning)
        else:
            pretty_console.console.print(Padding(md, pad=(0, 0, 0, 3)))

        print('\n' * settings['new_lines_below'], end='')


def print_result(json_results: dict, url: str, settings: dict):
    """
    Print out the results of a submission in a neat way
    :param json_results: json object with data about a submission
    :param url: link to the submission
    :param settings: dict with settings
    """
    from dodonacli.source import submission_data_handler

    if json_results['accepted']:
        # Everything passed, well done!
        result = "[bold bright_green]All tests passed![/] You can continue to next exercise.\n"
    else:
        result = submission_data_handler.submission_data_handler(json_results, settings).strip() + '\n'

    result += url
    custom_print(result, settings, pretty=True)


def print_status(config: dict, settings: dict):
    """
    Print out the current selection of course, exercise-series and exercise.
    :param config: Dictionary with the configs
    :param settings: Dictionary with the settings
    """
    course_string = config['course_name']
    if config['course_id'] is not None:
        course_string += f" ({config['course_id']})"

    custom_print(
        f"[u bright_blue]Status:[/]\n"
        f"\t{'Course: '.ljust(10)}{course_string}\n"
        f"\t{'Series: '.ljust(10)}{config['serie_name']}\n"
        f"\t{'Exercise: '.ljust(10)}{config['exercise_name']}",
        settings, pretty=True
    )


def print_exercise_submissions(json_data: dict, settings: dict):
    """
    Print out a list of the (up to) 10 most recent submissions as found in json_data
    :param json_data: Dictionary with submission data
    :param settings: Dictionary with settings
    """
    from dodonacli.source import pretty_console

    pretty_console.console.print(
        "\n[u bright_blue]Most recent submissions:[/]"
    )

    amount_shown = min(settings['amount_sub_exercise'], len(json_data))
    if amount_shown == -1:
        amount_shown = len(json_data)

    for i, submission in enumerate(json_data[:amount_shown]):
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
    # Newline for clarity
    print()


def print_all_submissions(connection, headers: dict, json_data: dict, settings: dict):
    """
    Print out a list of the latest 30 submissions for the user, userwide (not tied to an exercise).
    Makes extra requests to Dodona to get the name of the exercises of the submissions
    :param connection: Connection to Dodona
    :param headers: Headers to send with the connection
    :param json_data: Dictionary with submission info
    :param settings: Dictionary with settings
    :return:
    """
    from dodonacli.source import pretty_console
    import json

    print('\n' * settings['new_lines_above'], end='')

    pretty_console.console.print(
        "[u bright_blue]Most recent submissions:[/]"
    )

    amount_shown = min(settings['amount_sub_global'], len(json_data))
    if amount_shown == -1:
        amount_shown = len(json_data)

    for i, submission in enumerate(json_data[:amount_shown]):
        if submission['accepted']:
            accepted_emoji = "[bright_green]:heavy_check_mark:[/bright_green]"
        else:
            accepted_emoji = "[bright_red]:heavy_multiplication_x:[/bright_red]"

        status = submission['status']

        exercise_link = submission['exercise'].replace("https://dodona.be/nl", "", 1)
        connection.request("GET", exercise_link, headers=headers)

        response = connection.getresponse()
        res_status = response.status
        # Need to read always to be able to accept a new request
        result = response.read()

        if res_status == 200:
            exercise_name = json.loads(result).get('name') or "[i]unkown[/i]"
        else:
            exercise_name = "[i]unable to get info about exercise[/i]"

        pretty_console.console.print(
            f"\t{accepted_emoji}  [link={submission['url'].rstrip('.json')}]#{len(json_data) - i: <2}[/link]"
            f"\t{status: <25}"
            f"\t{exercise_name}"
        )

    connection.close()
    print('\n' * settings['new_lines_below'], end='')
