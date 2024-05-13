import click


@click.command(help="Post a solution-file to Dodona. "
                    "The file has to be in your current working directory, and this only works "
                    "if there is a selected exercise. "
                    "DodonaCLI will give a try at rendering a small part of the feedback-table so you can continue "
                    "working from the terminal, this isn't guarenteed to provide enough info, but it's doing its best.")
@click.option("-l", "--use-link",
              help="Post your solutionfile to the link at the first line of your solutionfile. "
                   "This is inspired by plugins for editors as VSCode for Dodona.",
              is_flag=True, default=False)
@click.option("-c", "--check",
              help="Check the file you provided if the syntax is valid for the programming language "
                   "associated with the exercise. Currently supported languages: bash, python, java, "
                   "javascript. For Java files, it will use javac to compile all *.java files that "
                   "don't have 'test' in them.",
              is_flag=True, default=False)
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
def post(file, use_link, check):
    import http.client
    from dodonacli.source import set_data, get_data, syntax_checker

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
            if link[:2] == '#!':
                link = solutionfile.readline()
            link_index = link.find("https://dodona.be/")
            if link_index < 0:
                print("\nNo valid link found on the first line of your file. Please confirm again.\n"
                      "A valid link starts with 'https://dodona.be/'\n")
                return
            link = link[link_index:]

            if link.find("/courses/") != -1:
                course_id_index_start = link.find("/courses/") + len("/courses/")
                course_id_index_stop = link.find("/", course_id_index_start)
                course_id = link[course_id_index_start:course_id_index_stop]
            else:
                course_id = None
            exercise_id_index_start = link.find("/activities/") + len("/activities/")
            exercise_id_index_stop = link.find("/", exercise_id_index_start)
            exercise_id = link[exercise_id_index_start:exercise_id_index_stop]

            # We can read the content of the file now as the file-pointer is already at the 2nd line
            content = solutionfile.read()
    else:
        # Syntax check not available with link at top of file
        if check:
            if not syntax_checker.check_syntax(file, config['programming_language']):
                return

        with open(file, 'r') as solutionfile:
            content = solutionfile.read()
        course_id = config['course_id']
        exercise_id = config['exercise_id']

    # Make sure the amount of newlines is exactly 1
    content = content.rstrip() + "\n"

    # Post exercise to Dodona, does not work if there is no exercise selected or -l flag not used
    if not use_link and not config['exercise_id']:
        print("\nNo exercise selected! If you want to use a link at the top of your file, use the -l flag.\n")
    else:
        set_data.post_solution(content, connection, headers, course_id, exercise_id)
