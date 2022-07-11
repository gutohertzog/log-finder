"""
Open all log files in the current directory and use the arguments to find all
the matches.
"""

__version__ = 'v1.3.0 beta'
__author__ = 'Guto Hertzog'

import argparse
import os
import sys
from pathlib import Path


ENCODING = 'utf-8'
LOG_EXT = '.log'
I_REQ_TIME = -1  # index of the request time


def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_logs() -> list:
    """Search for all log files in the current directory of this python file.

    Returns:
        logs (list): A list of all log files found in the folder or an empty
        list.
    """
    everything = os.listdir()

    logs = []
    for item in everything:
        item = Path(item)
        if item.suffix == LOG_EXT:
            logs.append(item)

    return logs


def read_log_file(log: str) -> str:
    """Load a single log file from the disc and yield every line.

    Args:
        log (str): Name of the log file to be open.

    Yield:
        str: Every line of the file.
    """
    with open(log, 'r', encoding=ENCODING) as file:
        for line in file.readlines():
            yield line


def save_found_records(matches: list, name: str, log: Path) -> None:
    """The matches will be saved into a file with the name pattern below.

    Examples:
        i-<arg>-<log_file_name>.txt: For includents.
        e-<arg>-<log_file_name>.txt: For excludents.
        s-<time>-<log_file_name>.txt: For request time.

    Args:
        matches (list): A list with all matches found inside a log file.
        name (str): First part of the file name.
        log (str): Sent to create the text file name.
    """
    # Replace the log extension for text extension
    log = log.replace(LOG_EXT, '.txt')
    file_name = name + '-' + log

    with open(file_name, 'w', encoding=ENCODING) as file:
        file.writelines(matches)

    print(f'File {file_name} saved.')


def search_records(log: str, arg: str, include: bool) -> None:
    """Function that will pass through all records of the log.

    If the include is True (includent), all the records that match the arg
    will be saved.

    If the include is False (excludent), will only save the records that
    DON'T match the arg.

    Args:
        log (str): Name of the log file to be open.
        arg (str): Argument to be searched in every record of the file.
        include (bool): Checks if the arg is includent or excludent.
    """
    lines = read_log_file(log)

    if include:
        return [line for line in lines if arg in line]

    return [line for line in lines if arg not in line]


def search_by_time(log: str, arg: int) -> None:
    """Will pass through all records of the log looking for the request time.
    It'll match if it's greater or equal.

    Args:
        log (str): Name of the log file to be open.
        arg (int): Argument to be searched in every record of the file.
    """
    lines = read_log_file(log)

    matches = []
    for line in lines:
        temp_list = line.split(' ')
        if int(temp_list[I_REQ_TIME]) >= arg:
            matches.append(line)

    return matches


def arg_parser() -> list:
    """Argument parser builder and check all received arguments to split them
    into three different lists.

    Returns:
        return (list): Three lists with all conditions to search for.
    """
    parser = argparse.ArgumentParser(
        prog='log-finder',
        description='search for common words in log files')

    parser.add_argument('-v', '--version',
                        action="version",
                        version=f'%(prog)s {__version__}')
    parser.add_argument('-i', '--inc',
                        action="extend",
                        default=[],
                        nargs="+",
                        type=str,
                        help='argument to be included on the search')
    parser.add_argument('-e', '--exc',
                        action="extend",
                        default=[],
                        nargs="+",
                        type=str,
                        help='argument to be excluded from the search')
    parser.add_argument('-s', '--sec',
                        default=0,
                        type=int,
                        help='search by the req time equals or greater than')

    args = parser.parse_args()

    return args.inc, args.exc, args.sec


def start() -> None:
    """Main function of the program."""

    includes, excludes, seconds = arg_parser()

    # No argument was sent when the file was executed, exits the program
    if not includes and not excludes and not seconds:
        print('\n\tInsufficient Arguments\n')
        print('Please, use `python main.py --help` for documentation.')
        return

    print('Begenning search.\n')

    logs = get_logs()

    # No log file was found in the current directory, exits the program
    if not logs:
        print('\n\tFile Not Found\n')
        print('No log file was found in the current directory.')
        print('Checks if at least one log file is in the same folder')
        print('than this python file.')
        return

    clear_screen()
    for log in logs:
        for inc in includes:
            matches = search_records(log.name, inc, True)
            if matches:
                save_found_records(matches, 'i-'+inc, log.name)
            else:
                print(f"The argument '{inc}' wasn't found in {log.name} file.")

        for exc in excludes:
            matches = search_records(log.name, exc, False)
            if matches:
                save_found_records(matches, 'e-'+exc, log.name)
            else:
                print(f"The argument '{exc}' was found all over the", end=' ')
                print(f"{log.name} file.")

        if seconds:
            matches = search_by_time(log.name, seconds)
            if matches:
                save_found_records(matches, 's-'+seconds, log.name)
            else:
                print(f"The argument '{seconds}' wasn't found in", end=' ')
                print(f"{log.name} file.")

    print('\nSearch completed.')


if __name__ == "__main__":
    start()
    sys.exit()
