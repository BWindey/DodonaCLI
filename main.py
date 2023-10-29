import argparse


class ArgumentParser:
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)
        self.args = None

    def add_arguments(self):
        # Define your command-line arguments here
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    def parse_args(self):
        self.args = self.parser.parse_args()


def main():
    arg_parser = ArgumentParser("Dodona Command Line Interface (dodona.be)")
    arg_parser.add_arguments()
    arg_parser.parse_args()

    print(arg_parser.args)


if __name__ == "__main__":
    main()
