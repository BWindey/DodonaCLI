# Command Line Interface for [Dodona](https://dodona.be)

PyPI page: https://pypi.org/project/DodonaCLI/#description

**Contents**:
1) [Disclaimers](#disclaimers)
2) [How to install](#how-to-install)
3) [How to use](#how-to-use)
4) [Flags that could be important](#flags-that-could-be-important)
5) [How to update](#how-to-update)
6) [Roadmap](#roadmap)

## Disclaimers

- DodonaCLI is an independent tool created by me, a student, and is not officially affiliated with the Dodona service or its team. Dodona, provided by the dedicated team at UGent University, offers an exceptional service, and this tool has been created as a complementary project. Only issues related to the Dodona website itself should be directed to the official Dodona support channels. Issues with the CLI tool should be posted on this [project’s Issues](https://github.com/BWindey/DodonaCLI/issues).

- Although the exercise-description formatting is mostly useable, do NOT rely on this for tests and exams! The printed description may be incomplete, or even incorrect. Please be aware of this!


- I did my best to format the output of DodonaCLI in a nice manner. If this is not the case for your terminal, please reach out via the [Issues](https://github.com/BWindey/DodonaCLI/issues) to see if we can fix that. I use the Alacritty and Gnome terminal, so if you’re using those, you can be mostly sure that what you see is intended.


## How to install
`pip install DodonaCLI`

Alternatively, you can `git clone https://github.com/BWindey/DodonaCLI` and when inside the DodonaCLI folder,
do `pip install -e .`.
This is mostly useful for those wanting to change/add to the code.

Tab-completion is supported for bash. You can 
download ["dodonacli_completion_script.sh" from GitHub](https://github.com/BWindey/DodonaCLI/blob/master/dodonacli_completion_script.sh),
and source it in your ~/.bashrc. 
This is currently not supported (tested, tried, ...) for other shells than bash.
If you know how to support your platform, please reach out to me.

There is also a manual page. You can download ["dodonacli.1.gz"](https://github.com/BWindey/DodonaCLI/blob/master/man-page/dodonacli.1.gz) and save this in a folder included in `$(manpath)`. 


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
You’ll quickly see why this is hidden behind this flag: the formatting can be aweful. 
For some exercise-descriptions, this can, however, be a nice addition,
and in the future the formatting-"engine" can improve.


### Hidden 
This flag is used in combination with the `select` command, when selecting an exercise-series that is hidden. 
Series can be hidden when they are used in tests or exams, and to get to them, you’ll receive a link to it from your 
teachers. This link will be of the form ".../series/<SERIES-ID>/?token=<TOKEN>". 
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


## How to update
Updating is simple: 
`pip install DodonaCLI --update`

Alternatively, if you installed it with cloning from GitHub, you can `git pull`.


## Roadmap
More features to maybe add in the future:
- add indicator to series to mark if all their exercises are completely solved
- user-settings (f.e. auto-download of files, language, formatting, ...)
- easy (automatic?) downloading of files mentioned in exercise description
- be able to mark as read via terminal for ContentPage

**Not important, but valid ideas:**
- (plugin) for syntax-checking before posting, so you get a quicker response in case of a syntax error, depends on the type of exercise (bash, java, python, C, C++, R, ...)
- caching to make it feel like a real command, very fast! Currently, you’ll often have to wait a few hundred milliseconds for the API call to return
- look into https://textual.textualize.io/getting_started/ to maybe use that??
