import re
import shutil
import subprocess
import textwrap

from . import pretty_console


def print_courses_data(json_data):
    """
    Print out the courses in json_data in a neat way
    :param json_data: json object with data about Dodona courses
    """
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
    pretty_console.console.print('\n[u bright_blue]Your courses:[/]')
    all_courses_formatted = ""
    for e in display_data:
        all_courses_formatted += (f'\t{e[0].ljust(max_course_id_length)}: '
                                  f'[bold]{e[1].ljust(max_course_name_length)}[/]\tby {e[2]}\n')
    pretty_console.console.print(all_courses_formatted)


def print_series_data(json_data):
    """
    Print out the exercise-series in json_data in a neat way
    :param json_data: json object with data about Dodona exercise-series
    """
    # List of tuples where each tuple represents an exercise-series by id, name and description
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['description']))

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_series_id_length = max(len(e[0]) for e in display_data)
    max_series_name_length = max(len(e[1]) for e in display_data)

    # Print out all the series in display_data while also handling the Markdown inside the series-description
    pretty_console.console.print("[u bright_blue]All series:[/]")
    for e in display_data:
        description = e[2].split('\n')
        new_description = ''

        for line in description:
            # Convert Markdown links to Ansi links. TERMINAL DEPENDANT
            line = re.sub(r'{: target="_blank"}', '', line)
            # line = re.sub(r'\[(.*?)\]\((.*?)\)', '\033]8;;\\2\033\\ \\1\033]8;;\033\\ ', line)

            # Replace bold and italics in Markdown to use Ansi codes
            line = re.sub(r'\*\*(.*?)\*\*', '\033[1m\\1\033[0m', line)
            line = re.sub(r'_(.*?)_', '\033[3m\\1\033[0m', line)

            # Split lines in multiple when they are too long for the terminal while keeping all lines indented.
            if len(line.replace("**", "").replace("_", "")) > shutil.get_terminal_size().columns - 8:
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
        print(
            f"{e[0].ljust(max_series_id_length)}: "
            f"\033[1m{e[1].ljust(max_series_name_length)}\033[0m\n{new_description}")


def print_exercise_data(json_data):
    """
    Print out the exercises in json_data in a neat way
    :param json_data: json object with data about Dodona exercises in a series
    """
    # List of tuples where each tuple represents an exercise by id, name, solved and has_attempt
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['last_solution_is_best'], field['has_solution']))

    # Find the maximum length of all but the last element in all tuples to align them in the terminal
    max_exercise_id_length = max(len(e[0]) for e in display_data)
    max_exercise_name_length = max(len(e[1]) for e in display_data)

    # Print out all exercises in display_data with indicator about solution-status: solved, wrong or not yet solved
    pretty_console.console.print('[u bright_blue]Exercises:[/]')
    for e in display_data:
        pretty_console.console.print(
            f"{e[0].ljust(max_exercise_id_length)}: [bold]{e[1].ljust(max_exercise_name_length)}[/]\t" +
            "[bold bright_green]SOLVED[/]" * (e[2] and e[3]) +
            "[bold bright_red]WRONG[/]" * (not e[2] and e[3]) +
            "[bold]NOT YET SOLVED[/]" * (not e[3])
        )


def print_exercise(json_data):
    """
    Print out the exercise-description. Needs to call the Dodona-sandbox and convert HTML to text.
    Prints out a warning for potential incompleteness, which may be dangerous for tests and exams.
    :param json_data: json object with info about a Dodona exercise
    """

    # Print the HTML with warnings
    pretty_console.console.print(
        "\n[u bold bright_red]WARNING: the description may not be correct, DO NOT rely on this for exams and tests!!\n"
        "Instead, use this url:[/] " + json_data['description_url']
    )

    pretty_console.console.print("\nExpected programming language: " + json_data['programming_language']['name'] + '\n')

    description = subprocess.getoutput("lynx --dump " + json_data['description_url'])
    description = re.sub(r'\[(\d+)]([ \w-]+)\^(\1)', r'[\1: \2]', description, flags=re.DOTALL)

    pretty_console.console.print(description)

    pretty_console.console.print(
        "\n[u bold bright_red]WARNING: the description may not be correct, DO NOT rely on this for exams and tests!!\n"
        "Instead, use this url:[/] " + json_data['description_url'] + '\n'
    )


def print_result(json_results):
    """
    Print out the results of a submission in a neat way
    :param json_results: json object with data about a submission
    """
    if json_results['accepted']:
        # Everything passed, well done!
        pretty_console.console.print("[bold bright_green]All test passed![/] You can continue to next exercise.")
    else:
        # There were some problems, list them here
        for group in json_results['groups']:
            print(group['description'] + ": " + str(group['badgeCount']) + " tests failed.")

            if group['badgeCount'] > 0:
                print("Failed exercises:")
                for test in group['groups']:
                    if not test['accepted']:
                        print("\t- " + test['description']['description'] + "\n\t\t" +
                              test['groups'][0]['description']['description'])


def print_status(config):
    print(f"\nStatus:\n"
          f"\tCourse: {config['course_name']}\n"
          f"\tSeries: {config['serie_name']}\n"
          f"\tExercise: {config['exercise_name']}\n")
