"""
Module stand alone to clear all results of the main.
Just used when developing.
"""

import os
import sys
from pathlib import Path


TXT_EXT: str = '.txt'
PREFIXES: list[str] = ['i-', 'e-', 's-']


def start() -> None:
    """Main function."""
    clear_txts()


def clear_txts() -> None:
    """Remove all txt files."""
    counter: int = 0

    # loop through all files and folders
    for item in os.listdir():
        item: Path = Path(item)
        if item.name[:2] in PREFIXES and item.suffix == TXT_EXT:
            os.remove(item)
            print(f'{item.name} file removed.')
            counter += 1

    # informative message
    if counter == 0:
        print('No text file found.')


def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    clear_screen()
    start()
    sys.exit()
