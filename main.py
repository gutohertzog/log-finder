"""Open all log files in the current directory and use the arguments to find
all the matches.
"""

__version__: str = 'v1.5.1'
__author__: str = 'Guto Hertzog'


import os
import sys
import time
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path


# ----------------------------------------------------------------------------
#                              constants section
# ----------------------------------------------------------------------------
# encoding for reading and writing files
ENCODING: str = 'utf-8'

# index of the request time
I_REQ_TIME: int = -1

# file extension
LOG_EXT: str = '.log'
TXT_EXT: str = '.txt'

# prefixes of the text files
PREFIXES: list[str] = ['i-', 'e-', 's-']

LOG_FILE_NAME: str = 'log-finder.log'


# ----------------------------------------------------------------------------
#                                logger section
# ----------------------------------------------------------------------------
def save_argv() -> None:
    """Append into a log file all arguments sent."""

    # get the current date and time for the record
    now: datetime = datetime.now()
    dt_string: str = now.strftime("%d-%m-%Y %H:%M:%S")

    # string to be saved
    line: str = dt_string + ' - arguments : ' + ' '.join(sys.argv[1:]) + '\n'

    with open(LOG_FILE_NAME, 'a', encoding=ENCODING) as file:
        file.write(line)


def purge_log() -> None:
    """Delete all registries of the log file."""
    with open(LOG_FILE_NAME, 'w', encoding=ENCODING) as file:
        file.writelines(' ')


# ----------------------------------------------------------------------------
#                           argument parser section
# ----------------------------------------------------------------------------
def arg_parser() -> list[list[str]]:
    """Argument parser builder and check all received arguments to split them
    into three different lists.

    Returns:
        return (list): Three lists with all conditions to search for.
    """
    parser: ArgumentParser = ArgumentParser(
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

    args: Namespace = parser.parse_args()

    return args.inc, args.exc, args.sec


# ----------------------------------------------------------------------------
#                               searcher section
# ----------------------------------------------------------------------------
def get_logs() -> list[str]:
    """Search for all log files in the current directory of this python file.

    Returns:
        logs (list): A list of all log files found in the folder or an empty
        list.
    """
    everything: list[str] = os.listdir()

    # remove log file generated from the search
    everything.remove(LOG_FILE_NAME)

    logs: list = []
    for item in everything:
        item: Path = Path(item)
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


def save_found_records(matches: list, name: str, log: str) -> None:
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
    log: str = log.replace(LOG_EXT, '.txt')
    file_name: str = name + '-' + log

    with open(file_name, 'w', encoding=ENCODING) as file:
        file.writelines(matches)

    print(f'File {file_name} saved with {len(matches)} matches.')


def search_records(log: str, arg: str, include: bool) -> list[str]:
    """Pass through all records of the log.

    If the include is True (include), all the records that match the arg will
    be saved.

    If the include is False (exclude), will save the records that DON'T match
    the arg.

    Args:
        log (str): Name of the log file to be open.
        arg (str): Argument to be searched in every record of the file.
        include (bool): Checks if the arg is include or exclude.

    Returns:
        return (list): A list of strings of all matches found.
    """
    lines: str = read_log_file(log)

    if include:
        return [line for line in lines if arg.lower() in line.lower()]

    return [line for line in lines if arg.lower() not in line.lower()]


def search_by_time(log: str, arg: int) -> list[str]:
    """Will pass through all records of the log looking for the request time.
    It'll match if it's greater or equa

    Args:
        log (str): Name of the log file to be open.
        arg (int): Argument to be searched in every record of the file.

    Returns:
        return (list): A list of strings of all matches found.
    """
    lines: str = read_log_file(log)

    matches: list = []
    for line in lines:
        temp_list: list[str] = line.split(' ')
        if int(temp_list[I_REQ_TIME]) >= int(arg):
            matches.append(line)

    return matches


# ----------------------------------------------------------------------------
#                                system section
# ----------------------------------------------------------------------------
def clear_screen() -> None:
    """Clear screen function of any OS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def finish() -> None:
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

    logs: list[str] = get_logs()

    # No log file was found in the current directory, exits the program
    if not logs:
        print('\n\tFile Not Found\n')
        print('No log file was found in the current directory.')
        print('Checks if at least one log file is in the same')
        print('folder than this python file.')
        return

    # begins the timer
    start_time: float = time.time()

    print('--- Beginning search ---\n')
    for log in logs:
        for inc in includes:
            matches: list[str] = search_records(log.name, inc, True)
            if matches:
                save_found_records(matches, 'i-'+inc, log.name)
            else:
                print(f"The argument '{inc}' wasn't found in {log.name} file.")

        for exc in excludes:
            matches: list[str] = search_records(log.name, exc, False)
            if matches:
                save_found_records(matches, 'e-'+exc, log.name)
            else:
                print(f"The argument '{exc}' was found all over the {log.name}\
                    file.")

        for sec in seconds:
            matches: list[str] = search_by_time(log.name, sec)
            if matches:
                save_found_records(matches, 's-'+sec, log.name)
            else:
                print(f"The argument '{sec}' wasn't found in {log.name} file.")

    end_time: float = (time.time() - start_time)
    print(f'\n--- Search completed in {end_time:.4f} seconds ---')


if __name__ == "__main__":
    clear_screen()
    start()
    finish()
