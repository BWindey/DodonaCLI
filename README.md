# Command Line Interface for Dodona.

**Contents**:
1) [Disclaimers](#disclaimers)
2) [How to install](#how-to-install)
3) [How to use](#how-to-use)
4) [All flags](#all-flags)
5) [Roadmap](#roadmap)


## Disclaimers

Altough the exercise-description formatting is decent, do NOT rely on this for tests and exams! The printed description may not be complete, or even incorrect. Please be aware of this!

All efforts to displayed text in an orderly fashion were made using a Linux GNOME-terminal. If it doesn't look good in your terminal, you probably are not running a GNOME-terminal. As this is open-source software, feel free to add terminal-detection to make things pretty for your terminal too, but this isn't feasible to do for me. 

This project was made in Linux, and was tested in the Command Prompt on Windows and on the zsh shell on MacOS. For those platforms you'll find an installation guide below. If you wish to use this in other terminals, you'll have to experiment yourself.



## How to install
### Linux
- Clone this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move into the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Make main.py executable `chmod +x main.py`
- Set an alias (optional but highly recommended) by appending this line to ~/.bashrc or ~/.bashprofile: `alias dodona='<absolute_path_to_DodonaCLI_folder>/main.py'`
- Test if it works with `dodona --help`

### MacOS
- Clone this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move into the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Create alias (optional but highly recommended) by appending this line to ~/.zshrc: `alias dodona=python <absolute_path_to_DodonaCLI_folder>/main.py`
- Test if it works with `dodona --help`

### Windows Command Prompt
- Clone this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move into the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Create set_alias.bat in your homedirectory for permanent alias (optional but highly recommended) with the folowing lines:\
  ```
  @echo off
  doskey dodona=python "<absolute_path_to_DodonaCLI_folder>\main.py" $*
  ```
- Open Register-editor (use the Windows search-bar if you don't know where it is)
- Navigate to HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor
- Add a String Value with name 'AutoRun' and give it as value the absolute path to set_alias.bat
- Test by opening a new command prompt and running `dodona --help`


## How to use
There are 3 things you can do with Dodona: displaying info (`--display`), selecting (`--select`) and posting exercises (`--post`). The behaviour of displaying and selecting will depend on your current selection, which may be viewed with `dodona --status`. You can imagine it as a tree structure:
- courses
  - exercise series
    - exercises

If nothing is selected, you'll need to select a course first, then an exercise series, then an exercise. You can always see all your available options with `dodona --display`. Posting a solution will only work if you have selected an exercise, and can be done with `dodona --post <SOLUTION_FILE>`.
This tree-like structure also explains the name of the deselect-flag: `--up` and `--uptop`. 

The first time you use DodonaCLI, the program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

If there is some boilerplate-code associated with an exercise, it will get printed out to the terminal once you select the exercise. You can also find it in the file 'boilerplate'. You can use it to write your solution in, and post it, but be aware that this file gets overwritten when you select a new exercise that has boilerplate-code attached (not all do).


## All flags
You can get info about all the flags by using '--help' or '-h'. Here is a brief explanation.

Most flags have a short and long version. Exceptions are '--uptop' and '--status', who have no short version. For other flags, the short version is always a single hyphen followed by the first letter of the long version.

To display all the info you need to make your next selection or post your solution, use '--display'. Selecting then happens with '--select', posting with '--post'. To deselect the current selection, use '--up', or '--uptop' to deselect everything. '--status' will give you an overview of what you have selected.



## Roadmap
More features to maybe add in the future:
- interactive tutorial
- show and load previous submissions if they exist
- use subcommands instead of flags
- add indicator to series to mark if all their exercises are completely solved
- user-settings (f.e. auto-download of files, language, formatting, ...)
- figure out how to more easily view an exercise description, boilerplate and the code you're writing together
- easy (automatic?) downloading of files mentioned in exercise description
- caching to make it feel like a real command, very fast! Currently you'll often have to wait a few hundred milliseconds for the API-call to return
- a python- or ed-like own terminal after running the `dodona` command to not have to repeat the command often. This seems complicated, but it might be possible.
