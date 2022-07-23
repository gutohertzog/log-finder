"""Module to have all constants of the application and some other
definitions"""

__version__ = 'v1.4.1'
__author__ = 'Guto Hertzog'


import os
import sys

# encoding for reading and writing files
ENCODING = 'utf-8'

# index of the request time
I_REQ_TIME = -1

# file extension
LOG_EXT = '.log'
TXT_EXT = '.txt'

# prefixes of the text files
PREFIXES = ['i-', 'e-', 's-']


def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def finish():
    """Exits the program."""
    sys.exit()
