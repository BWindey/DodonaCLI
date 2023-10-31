# Command Line Interface for Dodona.

IMPORTANT: currently only id's will work to select courses, series and exercises!

## Contents:
1) How to install
2) How to use
3) All flags


## How to install
- Clone this repo somewhere on your pc.
- Run `pip install requirements.txt`
- Make main.py executable: `chmod +x main.py`
- Set an alias for it, in the rest of this I'll assume you have set it like this: `dodona=<path_to_main.py>`
      (I'll assume you know how to set aliasses, if you don't, look it up on the interwebs)
- Check if it works by going to "How to use"
- Updates should be easy: navigate to the folder where you cloned this repo, and do `git pull` 


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
I'm too lazy to type them out right now, even too lazy to copy, just run `dodona --help` or '-h' to get info about all the available flags.
When this project matures, I'll update this README to give more info.
