import subprocess
import tempfile
import shutil


def check_syntax(file: str, language: str) -> bool:
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
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_python_syntax(file: str) -> bool:
    try:
        with open(file, 'r') as content:
            compile(content.read(), file, 'exec')
        return True
    except SyntaxError as se:
        print(f"\nSyntax error in Python file:\n{se}")
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False


def check_java_syntax(file: str) -> bool:
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(['javac', '-d', temp_dir, file], check=True)
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True

    except FileNotFoundError:
        # This will only occur if javac isn't installed.
        # Click will detect that the user gave an invalid file before this function is called
        print("\nTo check the syntax, 'javac' is called with your file. It appears however, that "
              "the Java compiler isn't installed on your system. Please install it: https://openjdk.org/install/")
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def check_javascript_syntax(file: str) -> bool:
    try:
        subprocess.run(['jshint', file], check=True)
        return True
    except FileNotFoundError:
        print("\nTo check the syntax, 'jshint' is called with your file. It appears however, that "
              "this program isn't installed on your system. Please install it using npm: npm install -g jshint")
        return False
    except Exception as e:
        print("\nNo idea what's going wrong, but something definitly is going wrong:\n" + str(e))
        return False
