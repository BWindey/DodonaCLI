# Command Line Interface for Dodona.
## Contents:
1) How to install
2) How to use
3) All flags

## How to install
Humpty dumpty.\
I don't even know yet how to install this...

## How to use
When freshly installed, run 
```
dodona -d
```
to display all your registred courses on Dodona. The program will ask you for an API-token, which you can generate on your Dodona-profile page. This will be stored in a file 'config.json' in the same directory as this python script. If you ever delete this file, you'll need to re-enter your API-token. You can either keep a back-up of your token somewhere else, or just generate a new token whenever you (accidently) deleted your old token.

To select a course, use the '-s' or '--select' flag, with a valid course_id or course_name. Now you can run `dodona -d` again to display the availaible exercise-series. Again use the '-s' flag to select a serie. Do the same for the exercises.\
You can always check what you have selected by running `dodona --status`.

If you want to deselect something, run `dodona -u` or '--up' to deselect the last selected option. If you want to deselect all, run `dodona --uptop`.


That's all you can do for now... I hope to be implementing more functionality the coming weeks.


## All flags
I'm too lazy to type them out now, even too lazy to copy, just run `dodona --help` or '-h' to get info about all the available flags.