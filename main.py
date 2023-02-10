"""Open all log files in the current directory and use the arguments to find
all the matches.
"""

__version__: str = 'v1.6.1'
__author__: str = 'Guto hertzog'


import os
import sys
import time
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Iterator


# ----------------------------------------------------------------------------
#                                  constants
# ----------------------------------------------------------------------------
ENCODING: str = 'utf-8'
LOG_FILE_NAME: str = 'log-finder.log'


# -----------------------------------------------------------------------------
#                                 logger class
# -----------------------------------------------------------------------------
class Logger():
    """Class responsible for create and update the log."""

    def save_argv(self) -> None:
        """Append into a log file all arguments sent."""
        # get the current date and time for the record
        dt_str: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # string to be saved
        line: str = dt_str + ' - arguments : ' + ' '.join(sys.argv[1:]) + '\n'

        with open(LOG_FILE_NAME, 'a', encoding=ENCODING) as file:
            file.write(line)

    def purge_log(self) -> None:
        """Delete all registries of the log file (for development)."""
        with open(LOG_FILE_NAME, 'w', encoding=ENCODING) as file:
            file.write('')


# -----------------------------------------------------------------------------
#                                 system class
# -----------------------------------------------------------------------------
class System():
    """Class to handle some system stuff"""

    @staticmethod
    def clear_screen() -> None:
        """Clear screen function of any OS."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def finish() -> None:
        """Exits the program."""
        sys.exit()


# -----------------------------------------------------------------------------
#                                 timer class
# -----------------------------------------------------------------------------
class Timer():
    """Timer class to calculate the execution time."""

    def __init__(self) -> None:
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def timer_start(self) -> None:
        """Start the clock."""
        self.start_time: float = time.time()

    def timer_finish(self) -> None:
        """Finish the clock."""
        self.end_time: float = time.time() - self.start_time

    def show(self) -> None:
        """Shows the amount of time spent."""
        print(f'\n--- Search completed in {self.end_time:.4f} seconds ---')


# -----------------------------------------------------------------------------
#                                searcher class
# -----------------------------------------------------------------------------
class Searcher():
    """Searcher Class"""

    # constant for the prefixes
    _prefixes: list[str] = ['i-', 'e-', 's-']
    # index of the request time
    _i_req_time: int = -1
    # log file extension
    _log_ext: str = '.log'

    def __init__(self) -> None:
        # variable to hold the arguments
        self.args: None = None
        # variable to fill the logger before the search
        self.logger: Logger = Logger()
        # list of log files found
        self.logs: list[str] = []

        # structure to be used to fill each argument
        self.struct: dict = {
            'argument': '',
            'log': '',
            'matches': [],
            'prefix': ''
        }

        self._arg_parser()

    def _arg_parser(self) -> None:
        """Argument parser split the them into three different lists."""
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

        self.args: Namespace = parser.parse_args()

        # no argument was sent when the file was executed, exit the program
        if not self.args.inc and not self.args.exc and not self.args.sec:
            print('\n\tInsufficient Arguments\n')
            print('Please, use `python main.py --help` for documentation.')
            System.finish()

        self.logger.save_argv()

    def get_logs(self) -> None:
        """Search for all log files in the current directory."""
        # get all files that have '.log' in the end
        self.logs = [e for e in os.listdir() if e[-4:] == self._log_ext]

        # remove log file generated from search
        self.logs.remove(LOG_FILE_NAME)

    def main_search(self) -> None:
        """Search inside the log files with the given arguments."""
        print('--- Beginning search ---\n')

        # start getting the logs
        self.get_logs()

        for log in self.logs:
            self.struct['log'] = log

            self.struct['prefix'] = self._prefixes[0]
            for inc in self.args.inc:
                self.struct['argument'] = inc
                self.get_matches()
                self.save_found_records()

            self.struct['prefix'] = self._prefixes[1]
            for exc in self.args.exc:
                self.struct['argument'] = exc
                self.get_matches()
                self.save_found_records()

            self.struct['prefix'] = self._prefixes[2]
            for sec in self.args.sec:
                self.struct['argument'] = sec
                self.get_matches()
                self.save_found_records()

    def get_matches(self) -> None:
        """This method is going to be called several times, but it'll only
        execute the portion of the code for the actual value of the
        struct['prefix'].
        """
        iter_lines: Iterator = Searcher.read_log_file(self.struct['log'])
        # restart the value
        self.struct['matches'] = []

        # prefix i-
        if self.struct['prefix'] == self._prefixes[0]:
            for line in iter_lines:
                if self.struct['argument'].lower() in line.lower():
                    self.struct['matches'].append(line)
            return

        # prefix e-
        if self.struct['prefix'] == self._prefixes[1]:
            for line in iter_lines:
                if self.struct['argument'].lower() not in line.lower():
                    self.struct['matches'].append(line)
            return

        # prefix s-
        if self.struct['prefix'] == self._prefixes[2]:
            for line in iter_lines:
                temp_list: list[str] = line.split(' ')
                req_time: int = int(temp_list[self._i_req_time])

                if req_time >= int(self.struct['argument']):
                    self.struct['matches'].append(line)
            return

        # space for future updates
        return

    def save_found_records(self) -> None:
        """The matches will be saved into a file with the name pattern below.

        Examples:
            i-<arg>-<log_file_name>.txt: For includes.
            e-<arg>-<log_file_name>.txt: For excludes.
            s-<time>-<log_file_name>.txt: For request time.
        """
        # Replace the log extension for text extension
        file_name: str = self.struct['prefix'] + self.struct['argument'] + '-'
        file_name += self.struct['log'].replace(self._log_ext, '.txt')

        if self.struct['matches']:
            with open(file_name, 'w', encoding=ENCODING) as file:
                file.writelines(self.struct["matches"])

            print(
                f'File {file_name} saved with {len(self.struct["matches"])} \
                    matches.')
        else:
            if self.struct['prefix'] == self._prefixes[1]:
                print(
                    f"The argument '{self.struct['argument']}' was found all \
                        over the {self.struct['log']} file.")
            else:
                print(
                    f"The argument '{self.struct['argument']}' wasn't found \
                        in {self.struct['log']} file.")

    @staticmethod
    def read_log_file(log: str) -> Iterator:
        """Load a single log file from the disc and yield every line.

        Args:
            log (str): name of the log file to be open.

        Yield:
            iterator: an iterator for every line of the file.
        """
        with open(log, 'r', encoding=ENCODING) as file:
            for line in file.readlines():
                yield line


# -----------------------------------------------------------------------------
#                                     main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    System.clear_screen()

    timer: Timer = Timer()
    timer.timer_start()

    search: Searcher = Searcher()
    search.main_search()

    timer.timer_finish()
    timer.show()

    System.finish()
