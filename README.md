# Command Line Interface for Dodona.

IMPORTANT: currently only id's will work to select courses, series and exercises!\
All efforts to format displayed text in an orderly fashion were made using a GNOME-terminal. If it doesn't look good in your terminal (links can be an issue), you probably are not running a GNOME-terminal. As this is open-source software, feel free to add terminal-detection to make things pretty for your terminal too, but this isn't feasible to do for me. 

## Contents:
1) How to install
2) How to use
3) All flags
4) Roadmap


## How to install
- Clone this repo somewhere on your pc.
- Run `pip install requirements.txt`
- Make main.py executable: `chmod +x main.py`
- Set an alias for it, in the rest of this I'll assume you have set it like this: `dodona=<path_to_main.py>`
      (I'll assume you know how to set aliasses, if you don't, look it up on the interwebs)
- Check if it works by going to "How to use"

Updating should be easy: navigate to the folder where you cloned this repo, and do `git pull`.

By default you should be on the master branch, but if you saw an interesting-looking commit on the develop branch, feel free to switch to develop to try it out and maybe give some feedback on the [Issues](https://github.com/BramWindey/DodonaCLI/issues)-page. The develop-branch does not guarantee proper error-handling, so I'd advice normal users to stay on the master branch.


## How to use
When freshly installed, run 
```
dodona -d
```
to display all your registred courses on Dodona. The program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

To select a course, use the '-s' or '--select' flag, with a valid course_id. Now you can run `dodona -d` again to display the availaible exercise-series. Again use the '-s' flag to select a serie. Do the same for the exercises.\
You can always check what you have selected by running `dodona --status`.

If you want to deselect something, run `dodona -u` or '--up' to deselect the last selected option. If you want to deselect everything, run `dodona --uptop`.

When you have an exercise selected, you can post your solution as follows:
- write your solution to a file
- run `dodona -p solution_file`, or use the '--post' flag instead of '-p'


## All flags
You can get info about all the flags by using '--help' or '-h'. Here is a brief explanation.

Most flags have a short and long version. Exceptions are '--uptop' and '--status', who have no short version. For other flags, the short version is always a single hyphen followed by the first letter of the long version.

To display all the info you need to make your next selection or post your solution, use '--display'. Selecting then happens with '--select', posting with '--post'. To deselect the current selection, use '--up', or '--uptop' to deselect everything. '--status' will give you an overview of what you have selected.


## Roadmap
There are a few steps to take before being able to call this a fully working (minimal) command:
- None! Well done, this command now works well enough to use. Let's start with adding extra features!

When above steps are implemented, there are some features I'd like to add:
- choose course/series/exercises by name instead of id
- format the exercise-description in a neat way
- add indicator to series to mark if all their exercises are completely solved
- easy (automatic?) downloading of files mentioned in exercise description
- user-settings (f.e. auto-download of files, language, formatting, ...)
- caching to make it feel like a real command, blazingly fast! Currently you'll often have to wait a few hundred milliseconds for the API-call to return
- a python- or ed-like own terminal after running the `dodona` command to not have to repeat the command often. This seems complicated, but it might be possible.
