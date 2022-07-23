"""Module to create and register some stuff into a log file."""

from datetime import datetime

from . import util as u

LOG_FILE_NAME = 'log-finder.log'


def save_argv(argv: list) -> None:
    """Append into a log file all arguments sent.

    Args:
        argv (list): List with all arguments used on execution.
    """

    # get the current date and time for the record
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    # string to be saved
    line = dt_string + ' - arguments : ' + ' '.join(argv[1:]) + '\n'

    with open(LOG_FILE_NAME, 'a', encoding=u.ENCODING) as file:
        file.write(line)


def purge_log():
    """Delete all registries of the log file."""
    with open(LOG_FILE_NAME, 'w', encoding=u.ENCODING) as file:
        file.writelines(' ')
