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
- Clones this repo to your pc: `git clone https://github.com/BWindey/DodonaCLI.git`
- Move in the directory: `cd DodonaCLI`
- Run `pip install requirements.txt`
- Set an alias for it by appending this line to ~/.bashrc or ~/.bashprofile: `alias dodona=python3 '<absolute_path_to_DodonaCLI_folder>/main.py'`
- Check if it works with `dodona --help`

### Windows Command Prompt
- Clones this repo to your pc `git clone https://github.com/BWindey/DodonaCLI.git`
- Move in the directory: `cd DodonaCLI`
- Check if Python is installed: `python --version`, if not installed, please install first
- Run `pip install -r requirements.txt`
- Set temporary alias: `doskey dodona=python "<absolute_path_to_DodonaCLI_folder>\main.py" $*`
- Test the alias (preferably in different directories): `dodona --help`
- Create set_alias.bat in homedirectory for permanent alias with folowwing lines:\
      ```
      @echo off
      doskey dodona=python "<absolute_path_to_DodonaCLI_folder>\main.py" $*
      ```
- Open Register-editor (use the Windows search-bar if you don't know where it is)
- Navigate to HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor
- Add a String Value with name 'AutoRun' and give it as value the absolute path to set_alias.bat
- Test by opening a new command prompt and running `dodona --help`

### MacOS
- Clone this repo to your pc
- Move in dir
- Check if Python installed
- Run `pip install -r requirements.txt`
- Create alias by appending this line to ~/.zshrc `alias dodona=python <absolute_path_to_DodonaCLI_folder>/main.py`

## How to use
When freshly installed, run 
```
dodona -d
```
to display all your registred courses on Dodona. The program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

To select a course, use the '-s' or '--select' flag, with a valid course_id. Now you can run `dodona -d` again to display the availaible exercise-series. Again use the '-s' flag to select a serie. Do the same for the exercises.\
You can always check what you have selected by running `dodona --status`.

If you want to deselect something, run `dodona -u` or '--up' to deselect the last selected option. If you want to deselect everything, run `dodona --uptop`.

If there is some boilerplate-code associated with an exercise, it will get printed out to the terminal once you select the exercise. You can also find it in the file 'boilerplate'. You can use it to write your solution in, and post it, but be aware that this file gets overwritten when you select a new exercise that has boilerplate-code attached (not all do).

When you have an exercise selected, you can post your solution as follows:
- write your solution to a file
- run `dodona -p solution_file`, or use the '--post' flag instead of '-p'



## All flags
You can get info about all the flags by using '--help' or '-h'. Here is a brief explanation.

Most flags have a short and long version. Exceptions are '--uptop' and '--status', who have no short version. For other flags, the short version is always a single hyphen followed by the first letter of the long version.

To display all the info you need to make your next selection or post your solution, use '--display'. Selecting then happens with '--select', posting with '--post'. To deselect the current selection, use '--up', or '--uptop' to deselect everything. '--status' will give you an overview of what you have selected.



## Roadmap
More features to maybe add in the future:
- store name too in config file to be able to print it out with the '--status' flag
- add indicator to series to mark if all their exercises are completely solved
- user-settings (f.e. auto-download of files, language, formatting, ...)
- figure out how to more easily view an exercise description, boilerplate and the code you're writing together
- easy (automatic?) downloading of files mentioned in exercise description
- caching to make it feel like a real command, blazingly fast! Currently you'll often have to wait a few hundred milliseconds for the API-call to return
- a python- or ed-like own terminal after running the `dodona` command to not have to repeat the command often. This seems complicated, but it might be possible.
