def save_boilerplate(content: str, exercise_name: str, extension: str):
    import os.path
    import textwrap
    from . import pretty_console

    boiler_filename = f"{exercise_name.lower()}.{extension}"

    if os.path.isfile(boiler_filename):
        print(
            f"\nNot saving boilerplate code because '{boiler_filename}' "
            "already exists.\nBoilerplate:\n"
        )
        pretty_console.console.print(
            textwrap.indent(content.rstrip(), '\t')
        )
    else:
        print(f"\nBoilerplate code (copy in '{boiler_filename}'):\n")
        pretty_console.console.print(
            textwrap.indent(content.rstrip(), '\t')
        )
        with open(boiler_filename, "w") as boilerplate_file:
            boilerplate_file.write(content)
    pass
