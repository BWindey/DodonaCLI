#!/bin/env python3
import click
import http.client

from source import handle_flags, get_data, interactive_tutorial


@click.command(help="A Command Line Interface for Dodona. Finally you have no need to exit your terminal anymore!\n"
                    "Use --help for more info about flags, or read the README on discord.",
               context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--display', '-d', is_flag=True,
              help="Display info based on what is already selected. If no course is yet selected, it gives a list of "
                   "courses to select from, if no serie or exercise is selected, idem")
@click.option('--select', '-s',
              help="Select based on name or id. Depends on where in the structure you are. With nothing yet selected, "
                   "this tries to select a course. When a course is selected, you can select a series of exercises, "
                   "and when a serie is selected, you can select an exercise. When using a name instead of an id, "
                   "the first occurence of that name will be chosen.")
@click.option('--post', '-p', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
              help="Post the contents of a file to Dodona as a solution of the current selected exercise."
                   "Only works if there is a selected exercise.")
@click.option('--up', '-u', is_flag=True,
              help="Go up in the structure by one level depending on where you are. "
                   "Exercise -> serie, serie -> course, course -> top. Use --up-top to immediatly go to the top.")
@click.option('--uptop', is_flag=True,
              help="Go immediatly to the top of the structure.")
@click.option('--status', is_flag=True,
              help="Shows selected course, selected serie and selected exercise.")
@click.option('--tutorial', is_flag=True,
              help="Starts an interactive tutorial.")
def main(display, select, post, up, uptop, status, tutorial):
    """
    A Command Line Interface for Dodona. Finally, you have no need to exit your terminal anymore!
    Use --help for more info about flags, or read the README on discord.
    """
    # Read configs in
    config = get_data.get_configs()

    # Start up the connection to Dodona
    connection = http.client.HTTPSConnection("dodona.be")
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": config['TOKEN']
    }

    # Handle all the different flags
    if display:
        handle_flags.handle_display(config, connection, headers)

    elif select:
        handle_flags.handle_select(select, config, connection, headers)

    elif post:
        handle_flags.handle_post(post, config, connection, headers)

    elif up:
        handle_flags.handle_up(config)

    elif uptop:
        handle_flags.handle_uptop(config)

    elif status:
        handle_flags.handle_status(config)

    elif tutorial:
        interactive_tutorial.start_tutorial(config)

    else:
        # No flags specified, print command summary
        print(main.help)


if __name__ == "__main__":
    # Main entry-point
    main()
