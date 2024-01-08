import datetime
import os

from dodonacli.source import get_data, set_data


def check_for_update():
    config = get_data.get_configs()

    last_check = config['date_update_checked']
    date_last_check = datetime.datetime.strptime(last_check, "%Y-%m-%d")
    current_date = datetime.datetime.now()

    if current_date >= date_last_check + datetime.timedelta(days=7):
        _check_for_update()
        config['date_update_checked'] = current_date.strftime("%Y-%m-%d")

        set_data.dump_config(config)


def _check_for_update():
    from update_notipy import update_notify
    import tomli

    # Get the path of the toml-file.
    # This is a bit more complicated because this file exists in the same directory as
    # the python files, but the command may be executed from anywhere with the appropriate alias set.
    # Thus, first the path to the directory of the python files is retrieved; then the config-file-name is appended
    script_directory = os.path.dirname(os.path.abspath(__file__))
    toml_file_path = os.path.join(script_directory, '../../pyproject.toml')

    with open(toml_file_path, 'rb') as toml_file:
        toml_dict = tomli.load(toml_file)

    DodonaCLI_version = toml_dict['project']['version']

    update_notify(
        "DodonaCLI",
        DodonaCLI_version,
        message="\nThere is a new version. You can upgrade with 'pip install --upgrade DodonaCLI'"
    ).notify()
