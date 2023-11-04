from bs4 import BeautifulSoup
import re
import textwrap
import markdownify
import os

from pretty_console import console


def print_html(raw_html: str):
    # markdown_my_beloved = markdownify.markdownify(raw_html)
    return ('\n' +
            str(os.system(
                "lynx -dump https://sandbox.dodona.be/nl/activities/1669118545/description/QGv8syuDRqqCpiWk/"))
            + '\n')
