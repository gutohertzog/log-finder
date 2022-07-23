"""Module that will search the matches."""

import os
import time
from pathlib import Path

import source.logger as l
import source.parser as p
import source.util as u


def get_logs() -> list:
    """Search for all log files in the current directory of this python file.

    Returns:
        logs (list): A list of all log files found in the folder or an empty
        list.
    """
    everything = os.listdir()

    # remove log file generated from the search
    everything.remove(l.LOG_FILE_NAME)

    logs = []
    for item in everything:
        item = Path(item)
        if item.suffix == u.LOG_EXT:
            logs.append(item)

    return logs


def read_log_file(log: str) -> str:
    """Load a single log file from the disc and yield every line.

    Args:
        log (str): Name of the log file to be open.

    Yield:
        str: Every line of the file.
    """
    with open(log, 'r', encoding=u.ENCODING) as file:
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
    log = log.replace(u.LOG_EXT, '.txt')
    file_name = name + '-' + log

    with open(file_name, 'w', encoding=u.ENCODING) as file:
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
    It'll match if it's greater or equal.

    Args:
        log (str): Name of the log file to be open.
        arg (int): Argument to be searched in every record of the file.
    """
    lines = read_log_file(log)

    matches = []
    for line in lines:
        temp_list = line.split(' ')
        if int(temp_list[u.I_REQ_TIME]) >= int(arg):
            matches.append(line)

    return matches


def start() -> None:
    """Main function of the program."""

    includes, excludes, seconds = p.arg_parser()

    l.save_argv()

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
