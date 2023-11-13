# Command Line Interface for [Dodona](https://dodona.be).

**Contents**:
1) [Disclaimers](#disclaimers)
2) [How to install](#how-to-install)
3) [How to use](#how-to-use)
4) [All flags](#all-flags)
5) [Roadmap](#roadmap)


## Disclaimers

- DodonaCLI is an independent tool created by me, a student, and is not officially affiliated with the Dodona service or its team. Dodona, provided by the dedicated team at UGent University, offers an exceptional service, and this tool has been created as a complementary project. Only issues related to the Dodona website itsself should be directed to the official Dodona support channels. Issues with the CLI tool should be posted on this [project's Issues](https://github.com/BWindey/DodonaCLI/issues).


- DodonaCLI currently uses 'lynx' to format the description, which might not work on Windows

- Altough the exercise-description formatting is decent, do NOT rely on this for tests and exams! The printed description may be incomplete, or even incorrect. Please be aware of this!


- All efforts to display text in an orderly fashion were made using a Linux GNOME-terminal. If it doesn't look good in your terminal, you probably are not running a GNOME-terminal. As this is open-source software, feel free to add terminal-detection to make things pretty for your terminal too, but this isn't feasible to do for me. 


- This project was made in Linux, and was tested in the Command Prompt on Windows (viewing exercise descriptions is currently not supported, but working on it!) and on the zsh shell on MacOS. For those platforms you'll find an installation guide below. If you wish to use this in other terminals, you'll have to experiment yourself.



## How to install
### Linux
- Clone this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move into the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Install 'lynx' using your packagemanager
- Make main.py executable `chmod +x main.py`
- Set an alias (optional but highly recommended) by appending this line to ~/.bashrc or ~/.bashprofile: `alias dodona='<absolute_path_to_DodonaCLI_folder>/main.py'`
- Test if it works with `dodona --help`

### MacOS
- Clone this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move into the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Install 'lynx' using your packagemanager
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
There are 3 things you can do with Dodona: displaying info (`--display`), selecting (`--select`) and posting exercises (`--post`). The behaviour of displaying and selecting will depend on your current selection, which can be viewed with `dodona --status`. You can imagine it as a tree structure:
- courses
  - exercise series
    - exercises

If nothing is selected, you'll need to select a course first, then an exercise series, then an exercise. You can always see all your available options with `dodona --display`. Posting a solution will only work if you have selected an exercise, and can be done with `dodona --post <SOLUTION_FILE>`.
This tree-like structure also explains the name of the deselect-flag: `--up` and `--uptop`. 

The first time you use DodonaCLI, the program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

If there is some boilerplate-code associated with an exercise, it will get printed out to the terminal once you select the exercise. You can also find it in the file 'boilerplate'. You can use it to write your solution in, and post it, but be aware that this file gets overwritten when you select a new exercise that has boilerplate-code attached (not all do).


## All flags
You can get info about all the flags by using the '--help' or '-h' flag. Here is a brief explanation.

Most flags have a short and long version. Exceptions are '--uptop' and '--status', who have no short version. For other flags, the short version is always a single hyphen followed by the first letter of the long version.

To display all the info you need to make your next selection or exercise, use '--display'. Selecting then happens with '--select', posting with '--post'. To deselect the current selection, use '--up', or '--uptop' to deselect everything. '--status' will give you an overview of what you have selected.



## Roadmap
More features to maybe add in the future:
- remove lynx dependency for viewing exercise-description
- potential collapsing of long pages (exercise-series, exercise-descriptions) or remind the user they can pipe it to less/more
- show and load previous submissions if they exist
- use subcommands instead of flags
- add indicator to series to mark if all their exercises are completely solved
- user-settings (f.e. auto-download of files, language, formatting, ...)
- figure out how to more easily view an exercise description, boilerplate and the code you're writing together
- easy (automatic?) downloading of files mentioned in exercise description
- caching to make it feel like a real command, very fast! Currently you'll often have to wait a few hundred milliseconds for the API-call to return
- a python- or ed-like own terminal after running the `dodona` command to not have to repeat the command often. This seems complicated, but it might be possible. Could maybe exists alongside the other option?
- look into https://textual.textualize.io/getting_started/ to maybe use that??
