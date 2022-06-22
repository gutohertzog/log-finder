"""
Open all log files in the current folder and apply the criteria (sent by
command line) of searches to find or exclude matches.
"""

__version__ = '1.2.0'
__author__ = 'Guto Hertzog'

import os
import sys


ENCODING = 'utf-8'
I_REQ_TIME = -1
LOG_EXT = '.log'
RESP_TIME = 'sec='


def clear_screen() -> None:
    """
    Clear screen function. of any os.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_logs() -> list:
    """
    Search by all log files on the current directory of this python file.

    return -- a list of all log files founded;
    """
    everything = os.listdir()

    # The item[-4:] is for file extension
    logs = [item for item in everything if item[-4:] == LOG_EXT]

    return logs


def read_log_file(log:str) -> list:
    """
    Function to read the log file from the disc.

    log -- name of the log file to be open;\n
    return -- list with all the records;
    """
    with open(log, 'r', encoding=ENCODING) as file:
        return file.readlines()


def save_found_records(matches:list, name:str, arg:str, log:str) -> None:
    """
    Function to test if at least one match was found.
    If found, it'll will be saved into a file with the name pattern below.

    i-<arg>-<log>.txt -- for includents
    e-<arg>-<log>.txt -- for excludents

    matches -- list with all matches found inside a log file;\n
    name -- first part of the file name;\n
    arg -- just sent to show the argument when nothing is found;\n
    log -- sent to create the text file name;
    """
    if matches:
        # Replace the log extension for text extension
        log = log.replace(LOG_EXT,'.txt')
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


def split_args(args:list) -> list:
    """
    Function to check all the received arguments and split them into three
    different lists.

    args -- a list of arguments to be splited;\n
    return -- 3 lists with all conditions to search for;
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
            arg = arg.replace(RESP_TIME,'')
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


def search_records(log:str, arg:str, include:bool) -> None:
    """
    Function that will pass through all records of the log.
    If the include is True (includent), all the records that match the arg
    will be saved.
    If the include is False (excludent), will only save the records that
    DON'T match the arg.

    log -- name of the log file to be open;\n
    arg -- argument to be searched in every record of the file;\n
    include -- check if the arg is includent or excludent;
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


def search_by_time(log:str, arg:str) -> None:
    """
    Function that will pass through all records of the log looking for the
    request time. It'll match if it's greater or equal.

    log -- name of the log file to be open;\n
    arg -- argument to be searched in every record of the file;
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


def start() -> None:
    """
    Main function of the program.
    """
    logs = get_logs()

    # No log file was found in the current directory, exits the program
    if not logs:
        print('\n\tFile Not Found\n')
        print('No .log file was found in the current directory.')
        print('Checks if the log file is in the same folder')
        print('than this python file.')
        return None

    # No argument was sent when the file was executed, exits the program
    if len(sys.argv) == 1:
        print('\n\tInsufficient Arguments\n')
        print('You need to specify one or more arguments')
        print('when executing the file.')
        print('\nExample: python main.py <argument_1> <argument_2> etc')
        return None

    # At least one argument and one log file were found, so all the arguments
    # to be searched in the log files are passed to the function to split them
    includents, excludents, seconds = split_args(sys.argv[1:])

    for log in logs:
        for incl in includents:
            search_records(log, incl, True)
        for excl in excludents:
            search_records(log, excl, False)
        for sec in seconds:
            search_by_time(log, sec)
    return None


if __name__ == "__main__":
    clear_screen()
    start()
    sys.exit()
