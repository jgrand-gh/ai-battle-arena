import time

from enum import Enum
from rich import print
from rich.text import Text

DELAY_PER_WORD = 0.12 # default: 0.24, lowered for testing purposes

class ColorList(Enum):
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"

def print_with_delay(text: str | list[str], seconds_per_word=DELAY_PER_WORD, end='\n'):
    if isinstance(text, str):
        lines = [text]
    else:
        lines = text
        
    # delayed output based on reading speed average per line
    for i, line in enumerate(lines):
        print(line, end=(end if i == len(lines) - 1 else '\n'), flush=True)
        delay = len(line.split()) * seconds_per_word
        time.sleep(delay)

def staggered_print_with_delay(text: str | list[str], seconds_per_word=DELAY_PER_WORD, end='\n'):
    if isinstance(text, str):
        rich_text = Text.from_markup(text)
    else:
        rich_text = Text.from_markup(" ".join(text))

    words = rich_text.split(" ")
    # delayed output based on reading speed average per word
    for i, word in enumerate(words):
        print(word, end=(' ' if i < len(words) - 1 else end), flush=True)
        time.sleep(seconds_per_word)