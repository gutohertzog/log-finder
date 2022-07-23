"""
Module stand alone to clear all results of the main.
Just used when developing.
"""

import os
import sys
from pathlib import Path

import source.util as u


def start() -> None:
    """Main function."""
    clear_txts()


def clear_txts() -> None:
    """Remove all txt files."""
    counter = 0

    # loop through all files and folders
    for item in os.listdir():
        item = Path(item)
        if item.name[:2] in u.PREFIXES and item.suffix == u.TXT_EXT:
            os.remove(item)
            print(f'{item.name} file removed.')
            counter += 1

    # informative message
    if counter == 0:
        print('No text file found.')


if __name__ == "__main__":
    u.clear_screen()
    start()
    sys.exit()
