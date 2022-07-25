"""Open all log files in the current directory and use the arguments to find
all the matches.
"""

__version__ = 'v1.4.2'
__author__ = 'Guto Hertzog'


import argparse
import os
import sys
import time
from datetime import datetime as dt
from pathlib import Path


# ----------------------------------------------------------------------------
#                              constants section
# ----------------------------------------------------------------------------
# encoding for reading and writing files
ENCODING = 'utf-8'

# index of the request time
I_REQ_TIME = -1

# file extension
LOG_EXT = '.log'
TXT_EXT = '.txt'

# prefixes of the text files
PREFIXES = ['i-', 'e-', 's-']


LOG_FILE_NAME = 'log-finder.log'


# ----------------------------------------------------------------------------
#                                logger section
# ----------------------------------------------------------------------------
def save_argv() -> None:
    """Append into a log file all arguments sent."""

    # get the current date and time for the record
    now = dt.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    # string to be saved
    line = dt_string + ' - arguments : ' + ' '.join(sys.argv[1:]) + '\n'

    with open(LOG_FILE_NAME, 'a', encoding=ENCODING) as file:
        file.write(line)


def purge_log():
    """Delete all registries of the log file."""
    with open(LOG_FILE_NAME, 'w', encoding=ENCODING) as file:
        file.writelines(' ')


# ----------------------------------------------------------------------------
#                           argument parser section
# ----------------------------------------------------------------------------
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
                        help='one or more argument to be included on the\
                            search')
    parser.add_argument('-e', '--exc',
                        action="extend",
                        default=[],
                        nargs="+",
                        type=str,
                        help='one or more argument to be excluded from the\
                            search')
    parser.add_argument('-s', '--sec',
                        action="extend",
                        default=[],
                        nargs="+",
                        type=str,
                        help='search by one or more request time equals or\
                            greater than the argument')

    args = parser.parse_args()

    return args.inc, args.exc, args.sec


# ----------------------------------------------------------------------------
#                               searcher section
# ----------------------------------------------------------------------------
def get_logs() -> list:
    """Search for all log files in the current directory of this python file.

    Returns:
        logs (list): A list of all log files found in the folder or an empty
        list.
    """
    everything = os.listdir()

    # remove log file generated from the search
    everything.remove(LOG_FILE_NAME)

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
        i-<arg>-<log_file_name>.txt: For includes.
        e-<arg>-<log_file_name>.txt: For excludes.
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

    print(f'File {file_name} saved with {len(matches)} matches.')


def search_records(log: str, arg: str, include: bool) -> None:
    """Pass through all records of the log.

    If the include is True (include), all the records that match the arg will
    be saved.

    If the include is False (exclude), will only save the records that DON'T
    match the arg.

    Args:
        log (str): Name of the log file to be open.
        arg (str): Argument to be searched in every record of the file.
        include (bool): Checks if the arg is include or exclude.
    """
    lines = read_log_file(log)

    if include:
        return [line for line in lines if arg.lower() in line.lower()]

    return [line for line in lines if arg.lower() not in line.lower()]


def search_by_time(log: str, arg: int) -> None:
    """Will pass through all records of the log looking for the request time.
    It'll match if it's greater or equa

    Args:
        log (str): Name of the log file to be open.
        arg (int): Argument to be searched in every record of the file.
    """
    lines = read_log_file(log)

    matches = []
    for line in lines:
        temp_list = line.split(' ')
        if int(temp_list[I_REQ_TIME]) >= int(arg):
            matches.append(line)

    return matches


# ----------------------------------------------------------------------------
#                                system section
# ----------------------------------------------------------------------------
def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def finish():
    """Exits the program."""
    sys.exit()


# ----------------------------------------------------------------------------
#                                 main section
# ----------------------------------------------------------------------------
def start() -> None:
    """Main function of the program."""

    includes, excludes, seconds = arg_parser()

    save_argv()

    # No argument was sent when the file was executed, exits the program
    if not includes and not excludes and not seconds:
        print('\n\tInsufficient Arguments\n')
        print('Please, use `python main.py --help` for documentation.')
        return

    logs = get_logs()

    # No log file was found in the current directory, exits the program
    if not logs:
        print('\n\tFile Not Found\n')
        print('No log file was found in the current directory.')
        print('Checks if at least one log file is in the same')
        print('folder than this python file.')
        return

    # begins the timer
    start_time = time.time()

    print('--- Beginning search ---\n')
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
                print(f"The argument '{exc}' was found all over the {log.name}\
                    file.")

        for sec in seconds:
            matches = search_by_time(log.name, sec)
            if matches:
                save_found_records(matches, 's-'+sec, log.name)
            else:
                print(f"The argument '{sec}' wasn't found in {log.name} file.")

    end_time = (time.time() - start_time)
    print(f'\n--- Search completed in {end_time:.4f} seconds ---')


if __name__ == "__main__":
    clear_screen()
    start()
    finish()
