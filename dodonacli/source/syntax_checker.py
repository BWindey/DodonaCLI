import subprocess


def check_syntax(file: str, language: str) -> bool:
    if language == "bash":
        return check_bash_syntax(file)
    return True


def check_bash_syntax(file: str) -> bool:
    # TODO: "bash -n" doesn't always mark errors,
    #   while "shellcheck" incorrectly flags some things as errors (check Tandenstokers)
    #   Find good alternative
    try:
        subprocess.run(['bash', '-n', file], check=True)
        return True
    except subprocess.CalledProcessError as cpe:
        print(f"Syntax Error in Bash script: {cpe}")
        return False
    except FileNotFoundError:
        print("Couldn't find the file you specified")
        return False
    except Exception as e:
        print("No idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
