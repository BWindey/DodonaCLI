import click


@click.command(help="Post the contents of a file to Dodona as a solution of the current selected exercise."
                   "Only works if there is a selected exercise.")
@click.argument('file', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
def post(file):
    pass