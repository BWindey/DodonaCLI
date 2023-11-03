"""
Global console object to be able to use it anywhere in the code by just importing it.
    from pretty_console import console
"""
from rich.console import Console
console = Console(color_system="standard")
