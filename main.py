"""
Open all log files on the current folder and search for all
occurrences of the given arguments.
"""

__version__ = '1.1.0'
__author__ = 'Guto Hertzog'

import os
import sys


RESP_TIME = 'seg='
LOG_EXT = '.log'


def clear_screen() -> None:
    """
    Clear screen function. of any os.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_logs() -> list:
    """
    Search by all log files on the current directory of this python file.

    return -- a list of all log files founded.
    """
    everything = os.listdir()

    logs = []
    # Passes through all files and folders of the current directory
    for item_name in everything:
        # Gets the last 4 chars, that it's the file extension
        end = item_name[-4:]
        if end == LOG_EXT:
            logs.append(item_name)

    return logs


def find_all(log:str, arg:str, sec: bool = False) -> None:
    """
    Function that will pass through all lines of the log for the desired arg.
    Every match will be stored on a variable and, at the end, saved into a file
    with the name pattern \n <arg>-<log>.txt

    Keyword arguments:\n
    log -- nome of the log file to be open;\n
    arg -- argument to be search inside the file;\n
    sec -- checker if should search for load page time;
    """
    lines = []
    with open(log, 'r', encoding='utf-8') as file:
        lines =  file.readlines()

    matches = []

    ########## SPECIFIC BEGINS ##########
    # Check if sec was send as argument
    if sec:
        for line in lines:
            temp_list = line.split(' ')
            # Checks if the last item of the list (response time) is bigger
            # than the time argument specified
            if int(temp_list[-1]) >= int(arg):
                matches.append(line)
        arg = RESP_TIME + arg
    ########## SPECIFIC ENDS ##########
    # Search for regular arguments
    else:
        matches = [line for line in lines if arg in line]

    # Only creates a file if any match was found
    if matches:
        # Remove log extension from log file name
        log = log.replace(LOG_EXT,'')
        # Creates the file name with the argument and log file name
        nome = arg + '-' + log + '.txt'
        with open(nome, 'w', encoding='utf-8') as arq:
            arq.writelines(matches)
        print(f'File {nome} saved.\n')
    else:
        print(f"The argument {arg} wasn't found in {log}.")


def start():
    """
    Main function of the program.
    """
    logs = get_logs()

    # If no log file was found in the current directory, exits the program
    if len(logs) == 0:
        print('\n\tFile Not Found\n')
        print('No .log file was found in the current directory.')
        print('Checks if the log file is in the same folder')
        print('than this python file.')
        return None

    # No argument was send when the file was executed
    if len(sys.argv) == 1:
        print('\n\tInsufficient Arguments\n')
        print('You need to specify one or more arguments')
        print('when executing the file.')
        print('\nExample: python main.py <argument_1> <argument_2> etc')
        return None

    # At least one argument and one log file were found, so all the arguments
    # to be searched in log files are stored in separate a variable
    args = sys.argv[1:]

    for log in logs:
        for arg in args:
            ########## SPECIFIC BEGINS ##########
            # Checks if shoud search by response time
            if RESP_TIME in arg:
                arg = arg.replace(RESP_TIME,'')
                try:
                    int(arg)
                except ValueError:
                    print('The seconds value sent is not valid!')
                else:
                    find_all(log, arg, True)
                # If the integer castinf fails or succeed, goes to the next
                # argument or log file
                finally:
                    continue
            ########## SPECIFIC ENDS ##########
            else:
                find_all(log, arg)

    return None


if __name__ == "__main__":
    clear_screen()
    start()
    sys.exit()
