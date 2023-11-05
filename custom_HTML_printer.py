import re
import markdownify

from pretty_console import console


def print_html(raw_html: str):
    stripped_html = re.sub("<div .*?>", "", raw_html)
    stripped_html = re.sub("</div>", "", stripped_html)
    stripped_html = re.sub("<meta .*?>", "", stripped_html)

    markdown_description = markdownify.markdownify(stripped_html)

    description = re.sub("\\*\\*(.*?)\\*\\*", "[bold]\\1[/bold]", markdown_description, flags=re.DOTALL)
    description = re.sub("\\*(.*?)\\*", "[i]\\1[/i]", description, flags=re.DOTALL)

    console.print(description)
