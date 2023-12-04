# Command Line Interface for [Dodona](https://dodona.be)

**Contents**:
1) [Disclaimers](#disclaimers)
2) [How to install](#how-to-install)
3) [How to use](#how-to-use)
4) [How to update](#how-to-update)
5) [All flags](#all-subcommands)
6) [Roadmap](#roadmap)
7) [Docker?](#what-is-docker-doing-here)

## Disclaimers

- DodonaCLI is an independent tool created by me, a student, and is not officially affiliated with the Dodona service or its team. Dodona, provided by the dedicated team at UGent University, offers an exceptional service, and this tool has been created as a complementary project. Only issues related to the Dodona website itsself should be directed to the official Dodona support channels. Issues with the CLI tool should be posted on this [project's Issues](https://github.com/BWindey/DodonaCLI/issues).

- Altough the exercise-description formatting is decent, do NOT rely on this for tests and exams! The printed description may be incomplete, or even incorrect. Please be aware of this!


- All efforts to display text in an orderly fashion were made using a Linux GNOME-terminal. If it doesn't look good in your terminal, you probably are not running a GNOME-terminal. As this is open-source software, feel free to add terminal-detection to make things pretty for your terminal too, but this isn't feasible to do for me. 


- This project was made in Linux, and was tested in the Command Prompt on Windows and on the zsh shell on macOS. For those platforms you'll find an installation guide below. If you wish to use this in other terminals, you'll have to experiment yourself.



## How to install
`pip install dodonacli`

Alternatively, you can `git clone https://github.com/BWindey/DodonaCLI` and when inside the DodonaCLI do `pip install .`. This is mostly usefull for those wanting to change/add to the code.

If you want to have tab-completion, this can be done when you're using bash. Download ["dodonacli_completion_script.sh" from github](https://github.com/BWindey/DodonaCLI/blob/master/completion_script.sh). 
This is currently not supported (tested, tried, ...) for other shells then bash

## How to use
There are 3 main things you can do with Dodona: displaying info (`dodona display`), selecting (`dodona select`) and posting exercises (`dodona post`). The behaviour of displaying and selecting will depend on your current selection, which can be viewed with `dodona status`. You can imagine it as a tree structure:
- courses
  - exercise series
    - exercises

If nothing is selected, you'll need to select a course first, then an exercise series, then an exercise. You can always see all your available options with `dodona display`. Posting a solution will only work if you have selected an exercise, and can be done with `dodona post <SOLUTION_FILE>`.
This tree-like structure also explains the name of the deselect-flag: `up` and `uptop`. 

The first time you use DodonaCLI, the program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

If there is some boilerplate-code associated with an exercise, it will get printed out to the terminal once you select the exercise. You can also find it in the file 'boilerplate'. You can use it to write your solution in, and post it, but be aware that this file gets overwritten when you select a new exercise that has boilerplate-code attached (not all do).

When you want to use this tool seriously, you will probably want to have multiple terminal sessions open. For example, I would want to have one to view the exercise description, and one to write my solution in vim. One way to achieve this is using 'tmux'. There are other ways to do this, but I'll explain how I use tmux to make an exercise:
- open tmux with `tmux`
- create new tmux window by typing ctrl + b with % or ". % opens a new one next to it, " opens a new one under it
- display exercise in one window `dodona display`
- move to other tmux window to use an editor to write my code in with ctrl + b and arrow keys to select a different window

## How to update
Updating is simple: 
`pip install DodonaCLI --update`

Alternatively, if you installed it with cloning from GitHub, you can just `git pull` and `pip build .` again like you would install it.

## All subcommands
You can get info about all subcommands and flags by using the '--help' flag after a (sub-) command. Here is a brief explanation.

## Roadmap
More features to maybe add in the future:
- show and load previous submissions if they exist
- add indicator to series to mark if all their exercises are completely solved
- user-settings (f.e. auto-download of files, language, formatting, ...)
- easy (automatic?) downloading of files mentioned in exercise description
- be able to mark as read via terminal for ContentPage
- use links at top of solution-files to ignore the configs and straight post to right exercise, like the plugins

**Not important, but valid ideas:**
- (plugin) for syntax-checking before posting, so you get a quicker response in case of a syntax error, depends on the type of exercise (bash, java, python, C, C++, R, ...)
- potential collapsing of long pages (exercise-series, exercise-descriptions) or remind the user they can pipe it to less/more
- caching to make it feel like a real command, very fast! Currently, you'll often have to wait a few hundred milliseconds for the API-call to return
- a python- or ed-like own terminal after running the `dodona` command to not have to repeat the command often. This seems complicated, but it might be possible. Could maybe exist alongside the other option?
- look into https://textual.textualize.io/getting_started/ to maybe use that??

## What is Docker doing here
Docker is a way for me to set up a clean environment to test out some experimental things that would affect more than just the python-source files. It will also allow me too to test out new release versions I push out, without the need to ask my friends if I can test it on their computer. 
I would encourage anyone looking into helping this project seriously, to install Docker on your system and 'docker build' and 'run' the Dockerfile.

It currently creates an Ubuntu environment with a 'tester'-user, has git, python, pip and vim installed, and has DodonaCLI cloned and an alias set. Perfect to start testing.
