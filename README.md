# Command Line Interface for [Dodona](https://dodona.be)

PyPI page: https://pypi.org/project/DodonaCLI/#description

**Contents**:
1) [Disclaimers](#disclaimers)
2) [Installation and updating](#installation-and-updating)
3) [How to use](#how-to-use)
4) [Flags that could be important](#flags-that-could-be-important)
5) [Settings](#settings)
6) [Tab-completion and man-pages](#tab-completion-and-man-pages)
7) [Help, DodonaCLI freezes](#help-dodonacli-freezes)
8) [Roadmap](#roadmap)


## Disclaimers

- DodonaCLI is an independent tool created by me, a student, and is not officially affiliated with the Dodona service or its team. Dodona, provided by the dedicated team at UGent University, offers an exceptional service, and this tool has been created as a complementary project. Only issues related to the Dodona website itself should be directed to the official Dodona support channels. Issues with the CLI tool should be posted on this [project’s Issues](https://github.com/BWindey/DodonaCLI/issues).

- Although the exercise-description formatting is mostly useable, do NOT rely on this for tests and exams! The printed description may be incomplete, or even incorrect. Please be aware of this!

- I did my best to format the output of DodonaCLI in a nice manner. If this is not the case for your terminal, please reach out via the [Issues](https://github.com/BWindey/DodonaCLI/issues) to see if we can fix that. I use the Alacritty and Gnome terminal, so if you’re using those, you can be mostly sure that what you see is intended.


## Installation and updating
Both installation and updating happen through pip:
```pip install DodonaCLI```
and
```pip install --upgrade DodonaCLI```

Alternatively, you can `git clone https://github.com/BWindey/DodonaCLI` and when inside the DodonaCLI folder,
do `pip install -e .`. The `-e` flag ensures that when you change files (or did a `git pull`), the cli will use the new code.
This is mostly useful for those wanting to change/add to the code, or test new features on the develop-branch (not recommended for normal users).


## How to use
There are three main things you can do with Dodona: displaying info (`dodona display`),
selecting (`dodona select`) and posting exercises (`dodona post`).
The behaviour of displaying and selecting will depend on your current selection,
which can be viewed with `dodona status`.
You can imagine it as a tree structure:
- courses
  - exercise series
    - exercises

If nothing is selected, you’ll need to select a course first, then an exercise series, then an exercise.
You can always see all your available options with `dodona display`.
Posting a solution will only work if you have selected an exercise, and can be done with `dodona post <SOLUTION_FILE>`.
This tree-like structure also explains the name of the deselect-flag: `up` and `uptop`. 
To select the next exercise, you don’t need to go up and select the new one, you can use the `next` command.

The first time you use DodonaCLI, the program will ask you for an API token,
which you can generate on your Dodona-profile page.
This will be stored in a file 'config.json' in the same directory as this python script.
If you ever delete this file, you’ll need to re-enter your API token.
You can either keep a back-up of your token somewhere else,
or just generate a new token whenever you (accidently) deleted your old token.

If there is some boilerplate code associated with an exercise,
it will get printed out to the terminal once you select the exercise.
You can also find it in the file 'boilerplate'.
You can use it to write your solution in, and post it,
but be aware that this file gets overwritten when you select a new exercise that has boilerplate-code attached
(not all do).


## Flags that could be important
There currently are four flags that can be important when working with non-standard exercises. 
- --force
- --hidden
- --other
- --use-link

They are all context-specific. A short explanation can be found in the help-pages, a slightly longer one here:

### Force 
This flag is used in combination with the `display` command, when viewing exercise-series and exercise-descriptions. 
It will do its best to render the html and markdown of the web-page in your terminal. 
You’ll quickly see why this is hidden behind this flag: the formatting can be awful. 
For some exercise-descriptions, this can, however, be a nice addition,
and in the future the formatting-"engine" can improve.


### Hidden 
This flag is used in combination with the `select` command, when selecting an exercise-series that is hidden. 
Series can be hidden when they are used in tests or exams, and to get to them, you’ll receive a link to it from your 
teachers. This link will be of the form `.../series/<SERIES-ID>/?token=<TOKEN>`. 
The only correct syntax to then select that hidden series with DodonaCLI is:
    ```dodona select --hidden <TOKEN> <SERIES-ID>```


### Other 
This flag is used in combination with the `select` command, when selecting a course you’re not registered for.
This allows you, for example, to select courses from previous years to try out those old tests or exams.
You cannot find these courses when using `display`,
so you’ll need the correct course-id to select it, not the course-name.

### Use-link
This flag is used in combination with the `post` command,
when posting a solution-file to a link provided at the first line of the solution-file.
The link has to include "/courses/<COURSE-ID>" and "/activities/<ACTIVITIES-ID"
to know which exercise to submit your solution to.
It also has to start with "https:<!-- comment to prevent link from appearing as real link-->//dodona.be/".
This link is not included in the solution submitted to the Dodona servers; it is stripped out.


## Settings
DodonaCLI has some settings (starting from version 2024.5.20). 
Currently they are only editable by editing the settings.json file directly.
In the future, there will be a sub-command to edit these in a more convenient way.
For info on what is all changeable with these settings, take a look at the changelog
```dodona info changelog```


## Tab-completion and man-pages
Tab-completion is supported for bash, fish and zsh. The easiest way to install it, is by following the short instructions at 
https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion,
where you replace all occurences of 'foo-bar' with 'dodona'.

You can also use my custom-written script for bash (if you're using bash), by downloading the autocomplete-script from  
https://github.com/BWindey/DodonaCLI/blob/master/dodonacli_completion_script.sh 
and source it in your ~/.bashrc. 
I personally use this custom one, as it allows me more control over the completion.
The disadvantage over using this, however, is that you'll need to redownload it if it ever changes.
I'll promise here and now that if I don't forget, I will always mention in the changelog 
(`dodona info changelog`), that you need to download the new completion-script.

A while ago, I strongly recommended the custom script, because the other way took about 200ms to complete, which felt slow, but due to some code-restructuring, the completion happens in around 50ms.

There is also a manual page available (very prefessional). 
You can download ["dodonacli.1.gz"](https://github.com/BWindey/DodonaCLI/blob/master/man-page/dodonacli.1.gz) and save this in a folder included in `$(manpath)`. 
This will have to be downloaded again if it is updated. I'll let you know in the changelogs.


## Help, DodonaCLI freezes
Since I just got this situation, I wanted to tell you how I fixed it.
My computer didn’t succeed in making any network requests over IPv6, and thus waited and waited and waited ...
To fix this, I had to disable IPv6 entirely on my own pc. 
This is not something I’ll show you how to do, you’ll have to do some research on the internet.
Before trying that, confirm first if this is indeed the issue by running `wget` with --inet6-only and --inet4-only 
to see if this is indeed the issue.


## Roadmap
This section has a bunch of ideas for me to work on, but also for you, the potential contributor!
Remember to look at the recent branches/commits to see if I’m not working on one of these:
- user-settings (f.e. auto-download of files, language, formatting, number of submissions shown, ...)
  - language
  - whether to save feedback to a file
  - auto download links from sandbox.dodona when selecting exercise
- easy (automatic?) downloading of files mentioned in exercise description
- improve the rendering of all html/markdown frankensteins, in descriptions of exercises and exercise-descriptions 
- add connection time-out to prevent long waiting when IPv6 doesn’t want to work along
- add support for more languages syntax checkers
- caching some info for faster navigation and/or autocompletion
- add indicator to series to mark if all their exercises are completely solved (maybe fetch from html-version)
- get exercise-names via html-parsing for a submission list to only need 1 API call (instead of 30)

Code cleanup:
- general refactoring of too large files (>150 lines can often be split)
- 'display_after_select' should maybe not need to make a 2nd API call? 
- special print that prints with right amount of new-lines to group that together
