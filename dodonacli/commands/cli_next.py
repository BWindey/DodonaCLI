import click


# Function and file have to be called cli_next, as next
# is a Python built-in. The command, however, will still be called
# with 'next', as click provides the 'name=' argument
@click.command(name="next",
               help="Move to the next type of what you have selected. "
                    "It loops around to the beginning if the current selection "
                    "is at the end of the 'list'")
@click.option("-r", "--reverse",
              help="Goes to the previous instead of the next.")
@click.option("-u", "--unsolved",
              help="Find the next unsolved item. "
                   "Currently only available for exercises, not series or courses.")
def cli_next():
    print("Function cli_next called!")
