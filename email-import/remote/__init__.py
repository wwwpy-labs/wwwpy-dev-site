from js import document
from wwwpy.remote import simple_dark_theme


async def main():
    simple_dark_theme.setup()

    from . import html_editor  # for component registration
    document.body.innerHTML = '<component-1></component-1>'
