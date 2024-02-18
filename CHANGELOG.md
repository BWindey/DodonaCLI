- Added **info** command:
    - Subcommand 'version' to display your current DodonaCLI version. Versions use the YYYY.M.D format.
    - Subcommand 'check-update' lets you know if there is an update available.
    - Subcommand 'github' gives a link to DodonaCLI’s GitHub page.
    - Subcommand 'changelog' shows a changelog for the latest downloaded version.

- Added syntax-check option to **post** command:
  - Use '-c' or '--check' to check syntax. This uses other commandline utilities like shellcheck, javac or python
  - Currently implemented for:
    - Bash
    - Java
    - JavaScript
    - Python

- Added CHANGELOG.md

As always, use the "--help" flag after every command and sub-command to learn more.