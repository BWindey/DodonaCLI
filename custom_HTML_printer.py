import re
import markdownify

from pretty_console import console


def print_html(raw_html: str):
    # Remove unnecessary tags
    stripped_html = re.sub("<div .*?>", "", raw_html)
    stripped_html = re.sub("</div>", "", stripped_html)
    stripped_html = re.sub("<meta .*?>", "", stripped_html)

    markdown_description = markdownify.markdownify(stripped_html)

    # Bold and italic formatting
    description = re.sub("\\*\\*(.*?)\\*\\*", "[bold]\\1[/bold]", markdown_description, flags=re.DOTALL)
    description = re.sub("\\*(.*?)\\*", "[i]\\1[/i]", description, flags=re.DOTALL)

    # Link formatting
    links = description.split("### Links")[-1]
    links = [link.strip() for link in links.split('\n') if link.strip()]
    link_dict = {line[2]: '[' + line[6:] for line in links}



    # console.print(description)
