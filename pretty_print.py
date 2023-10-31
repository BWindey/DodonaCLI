import shutil
import textwrap
import re


def print_courses_data(json_data):
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['teacher']))
    max_course_id_length = max(len(e[0]) for e in display_data)
    max_course_name_length = max(len(e[1]) for e in display_data)
    display_data = sorted(display_data, key=lambda x: x[1])

    print('\033[4;94mYour courses:\033[0m')
    for e in display_data:
        print(f'{e[0].ljust(max_course_id_length)}: \033[1m{e[1].ljust(max_course_name_length)}\033[0m\tby {e[2]}')


def print_series_data(json_data):
    display_data = []

    for field in json_data:
        display_data.append((str(field['id']), field['name'], field['description']))
    max_series_id_length = max(len(e[0]) for e in display_data)
    max_series_name_length = max(len(e[1]) for e in display_data)

    print("\033[4;94mAll series:\033[0m")
    for e in display_data:
        description = e[2].split('\n')
        new_description = ''

        for line in description:
            # Convert Markdown links to Ansi links. TERMINAL DEPENDANT
            line = re.sub(r'{: target="_blank"}', '', line)
            line = re.sub(r'\[([^\]]*)\]\(([^\)]*)\)', '\033]8;;\\2\033\\ \\1\033]8;;\033\\ ', line)

            # Replace bold and italics in Markdown to use Ansi codes
            line = re.sub(r'\*\*(.*?)\*\*', '\033[1m\\1\033[0m', line)
            # line = re.sub(r'_(.*?)_', '\033[3m\\1\033[0m', line)

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
            f"{e[0].ljust(max_series_id_length)}: \033[1m{e[1].ljust(max_series_name_length)}\033[0m\n{new_description}")
