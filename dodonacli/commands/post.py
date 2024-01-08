import click
import http.client

from dodonacli.source import set_data
from dodonacli.source import get_data


@click.command(help="Post a solution-file to Dodona. "
                    "The file has to be in your current working directory, and this only works "
                    "if there is a selected exercise.")
@click.option("-l", "--use_link",
              help="Post your solutionfile to the link at the first line of your solutionfile. "
                   "This is inspired by plugins for editors as VSCode for Dodona.",
              is_flag=True, default=False)
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
def post(file, use_link):
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    # Check for the link at the top of the file
    if use_link:
        with open(file, 'r') as solutionfile:
            link = solutionfile.readline()
            link_index = link.find("https://dodona.be/")
            if link_index < 0:
                print("\nNo valid link found on the first line of your file. Please confirm again.\n"
                      "A valid link starts with 'https://dodona.be/'\n")
                return
            link = link[link_index:]

            course_id_index_start = link.find("/courses/") + len("/courses/")
            course_id_index_stop = link.find("/", course_id_index_start)
            course_id = link[course_id_index_start:course_id_index_stop]

            exercise_id_index_start = link.find("/activities/") + len("/activities/")
            exercise_id_index_stop = link.find("/", exercise_id_index_start)
            exercise_id = link[exercise_id_index_start:exercise_id_index_stop]

            # We can read the content of the file now as the file-pointer is already at the 2nd line
            content = solutionfile.read()
    else:
        with open(file, 'r') as solutionfile:
            content = solutionfile.read()
        course_id = config['course_id']
        exercise_id = config['exercise_id']

    # Post exercise to Dodona, does not work if there is no exercise selected or -l flag not used
    if not use_link and not config['exercise_id']:
        print("\nNo exercise selected! If you want to use a link at the top of your file, use the -l flag.\n")
    else:
        set_data.post_solution(content, connection, headers, course_id, exercise_id)
