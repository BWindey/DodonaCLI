import subprocess


def check_syntax(file: str, language: str) -> bool:
    if language == "bash":
        return check_bash_syntax(file)
    if language == "python":
        return check_python_syntax(file)
    return True


def check_bash_syntax(file: str) -> bool:
    try:
        subprocess.run(['shellcheck', file], check=True)
        return True
    except subprocess.CalledProcessError as cpe:
        print(f"Syntax Error in Bash script: {cpe}")
        return False
    except FileNotFoundError:
        # This will only occur if shellcheck isn't installed.
        # Click will detect that the user gave an invalid file before this function is called
        print("\nTo check the syntax, 'shellcheck' is called with your file. It appears however, that "
              "shellcheck isn't installed on your system. Please install it: https://www.shellcheck.net/")
        return False
    except Exception as e:
        print("No idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_python_syntax(file: str) -> bool:
    try:
        with open(file, 'r') as content:
            compile(content.read(), file, 'exec')
        return True
    except SyntaxError as se:
        print(f"\nSyntax error in Python file:\n{se}")
    except Exception as e:
        print("No idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
