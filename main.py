"""
Open all log files in the current folder and apply the criteria (sent by
command line) of searches to find or exclude matches.
"""

__version__ = 'v1.3.0 beta'
__author__ = 'Guto Hertzog'

import argparse
import os
import sys
from pathlib import Path


ENCODING = 'utf-8'
I_REQ_TIME = -1
LOG_EXT = '.log'
RESP_TIME = 'sec='


def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_logs() -> list:
    """Search by all log files on the current directory of this python file.

    Returns:
        logs (list): A list of all log files founded in the folder.
    """
    everything = os.listdir()

    # The item[-4:] is for file extension
    # logs = [item for item in everything if item[-4:] == LOG_EXT]
    logs = []
    for item in everything:
        item = Path(item)
        if item.suffix == LOG_EXT:
            logs.append(item)

    return logs


def read_log_file(log: str) -> list:
    """Function to read the log file from the disc.

    Args:
        log (str): Name of the log file to be open.

    Returns:
        list: A list with all the records.
    """
    with open(log, 'r', encoding=ENCODING) as file:
        return file.readlines()


def save_found_records(matches: list, name: str, arg: str, log: str) -> None:
    """Function to test if at least one match was found.
    If found, it'll will be saved into a file with the name pattern below.

    Examples:
        i-<arg>-<log_file_name>.txt: For includents.
        e-<arg>-<log_file_name>.txt: For excludents.
        sec=<time>-<log_file_name>.txt: For request time.

    Args:
        matches (list): A list with all matches found inside a log file.
        name (str): First part of the file name.
        arg (str): Just sent to show the argument when nothing is found.
        log (str): Sent to create the text file name.
    """
    if matches:
        # Replace the log extension for text extension
        log = log.replace(LOG_EXT, '.txt')
        file_name = name + '-' + log

        with open(file_name, 'w', encoding=ENCODING) as file:
            file.writelines(matches)

        print(f'File {file_name} saved.')
    else:
        # Checks the type of operation to show the appropriate message
        if name[0:2] == 'e-':
            print(f"The argument {arg} was found all over the {log} file.")
        else:
            print(f"The argument {arg} wasn't found in {log} file.")


def split_args(args: list) -> list:
    """Function to check all the received arguments and split them into three
    different lists.

    Args:
        args (list): A list of arguments to be splited.

    Returns:
        return (list): Three lists with all conditions to search for.
    """
    includents = []
    excludents = []
    seconds = []

    for arg in args:
        # The - is the excludent indicator
        if arg[0] == '-':
            excludents.append(arg[1:])
        elif RESP_TIME in arg:
            # Remove the RESP_TIME value to test the integer part
            arg = arg.replace(RESP_TIME, '')
            try:
                int(arg)
            except ValueError:
                print('The seconds value sent is not valid!')
            else:
                seconds.append(arg)
            # If the integer cast fails or succeeds, goes to the next argument
            finally:
                continue
        else:
            includents.append(arg)
    return includents, excludents, seconds


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
        matches = [line for line in lines if arg in line]
        prefix = 'i-'
    else:
        matches = [line for line in lines if arg not in line]
        prefix = 'e-'

    name = prefix + arg
    save_found_records(matches, name, arg, log)


def search_by_time(log: str, arg: str) -> None:
    """Function that will pass through all records of the log looking for the
    request time. It'll match if it's greater or equal.

    Args:
        log (str): Name of the log file to be open.
        arg (str): Argument to be searched in every record of the file.
    """
    lines = read_log_file(log)

    matches = []

    for line in lines:
        temp_list = line.split(' ')
        if int(temp_list[I_REQ_TIME]) >= int(arg):
            matches.append(line)

    # Rebuild the argument as original sent to use it
    # on the file name later
    arg = RESP_TIME + arg
    save_found_records(matches, arg, arg, log)


def arg_parser():
    """
    arg parser do programa
    """
    parser = argparse.ArgumentParser(
        prog='log-finder',
        description='search for common words in log files')

    # group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('-v', '--version', action="version",
                        version=f'%(prog)s {__version__}')
    parser.add_argument('-i', '--inc', action="append", nargs="+",
                        type=str, help='argument to be included on the search')
    parser.add_argument('-e', '--exc', action="extend", nargs="+",
                        type=str,
                        help='argument to be excluded from the search')
    parser.add_argument('-s', '--sec', type=int,
                        help='search by the req time equals or greater than')

    args = parser.parse_args()

    print(args)
    sys.exit()


def start() -> None:
    """Main function of the program."""

    arg_parser()

    # No argument was sent when the file was executed, exits the program
    if len(sys.argv) == 1:
        print('\n\tInsufficient Arguments\n')
        print('You need to specify one or more arguments')
        print('when executing the file.')
        print('\nExample: python main.py <argument_1> <argument_2> etc')
        return None

    print('Begenning search.\n')

    logs = get_logs()

    # No log file was found in the current directory, exits the program
    if not logs:
        print('\n\tFile Not Found\n')
        print('No .log file was found in the current directory.')
        print('Checks if the log file is in the same folder')
        print('than this python file.')
        return None

    # At least one argument and one log file were found, so all the arguments
    # to be searched in the log files are passed to the function to split them
    includents, excludents, seconds = split_args(sys.argv[1:])

    clear_screen()
    for log in logs:
        for incl in includents:
            search_records(log, incl, True)
        for excl in excludents:
            search_records(log, excl, False)
        for sec in seconds:
            search_by_time(log, sec)

    print('\nSearch completed.')

    return None


if __name__ == "__main__":
    start()
    sys.exit()
