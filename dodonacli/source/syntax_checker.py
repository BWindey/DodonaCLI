import os
import shutil
import subprocess
import tempfile


def check_syntax(file: str, language: str) -> bool:
    """
    Check the syntax of the code in the file using external tools
    :param file: Filename containing the code to check
    :param language: Programming language to determine what tool to use
    :return: Returns whether the syntax is right
    """
    if language in ("bash", "sh"):
        return check_bash_syntax(file)
    if language == "python":
        return check_python_syntax(file)
    if language == "java":
        return check_java_syntax(file)
    if language == "javascript":
        return check_javascript_syntax(file)
    print("\nLanguage syntax check is not implemented for: " + language)
    return True


def check_bash_syntax(file: str) -> bool:
    try:
        # Exclude:
        # SC2001: See if you can use ${variable//search/replace} instead.
        subprocess.run(['shellcheck', '-e', 'SC2001', file], check=True)
        return True
    except subprocess.CalledProcessError as cpe:
        print(f"Syntax Error in Bash script: {str(cpe)}")
        return False
    except FileNotFoundError:
        # This will only occur if shellcheck isn't installed.
        # Click will detect that the user gave an invalid file before this function is called
        print(
            "\nTo check the syntax, 'shellcheck' is called with your file. "
            "It appears however, that shellcheck isn't installed on your system. \n"
            "Please install it: https://www.shellcheck.net/\n"
        )
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_python_syntax(file: str) -> bool:
    try:
        with open(file, 'r') as content:
            compile(content.read(), file, 'exec')
        return True
    except SyntaxError as se:
        print(f"\nSyntax error in Python file:\n{se}\n")
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_java_syntax(file: str) -> bool:
    temp_dir = tempfile.mkdtemp()
    try:
        directory = os.path.dirname(file)
        java_files = [file for file in os.listdir(directory) if file.endswith('.java') and "test" not in file.lower()]
        if not java_files:
            return False  # No Java files found in the directory

        # Construct the list of Java files with their full paths
        java_files_with_paths = [os.path.join(directory, file) for file in java_files]

        subprocess.run(['javac', '-d', temp_dir] + java_files_with_paths, check=True)

        # Remove temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True

    except subprocess.CalledProcessError:
        # This error will happen if there was something wrong with the Java syntax
        return False

    except FileNotFoundError:
        # This will only occur if javac isn't installed.
        # Click will detect that the user gave an invalid file before this function is called
        print(
            "\nTo check the syntax, 'javac' is called with your file. "
            "It appears however, that the Java compiler isn't installed on your system.\n"
            "Please install it: https://openjdk.org/install/\n"
        )
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def check_javascript_syntax(file: str) -> bool:
    try:
        subprocess.run(['node', '-c', file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # This will only occur if jshint isn't installed.
        # Click will detect that the user gave an invalid file before this function is called
        print(
            "\nTo check the syntax, 'node' is called with your file. "
            "It appears however, that this program isn't installed on your system.\n"
            "Please install it: https://nodejs.org/en/learn/getting-started/how-to-install-nodejs\n"
        )
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_haskell_syntax(file: str) -> bool:
    try:
        # TODO: enable compiling without main function present
        subprocess.run(['ghc', '-fno-code', '-v0', file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print(
            "\nTo check the syntax, 'ghc' is called with your file. "
            "It appears however, that this program isn't installed on your system.\n"
            "Please install it: https://www.haskell.org/ghcup/\n"
        )
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
