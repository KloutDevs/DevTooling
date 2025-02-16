"""
Styles and themes for the user interface
"""

from rich.theme import Theme
from rich.style import Style

# Main theme of the application
THEME = Theme({
    'info': 'cyan',
    'warning': 'yellow',
    'error': 'red bold',
    'success': 'green bold',
    'title': 'magenta bold',
    'subtitle': 'blue',
    'highlight': 'yellow bold',
    'directory': 'cyan',
    'file': 'yellow',
    'prompt': 'cyan bold',
})

# Styles for the directory tree
TREE_STYLES = {
    'directory': Style(color="cyan", bold=True),
    'file': Style(color="yellow"),
    'ignored': Style(color="dim white", italic=True),
    'error': Style(color="red", bold=True),
}

# Configuration of panels
PANEL_STYLES = {
    'default': {
        'border_style': 'cyan',
        'padding': (1, 2),
    },
    'info': {
        'border_style': 'blue',
        'padding': (1, 2),
    },
    'error': {
        'border_style': 'red',
        'padding': (1, 2),
    }
}