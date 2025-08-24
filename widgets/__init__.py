# Init - add imports for specific widget classes here
#   This allows other files to import directly from widgets
from .text_replace_widget import TextReplaceWidget


# Define explicitly included classes
WIDGET_CLASSES = [
    TextReplaceWidget,
]

__all__ = [c.__name__ for c in WIDGET_CLASSES]
