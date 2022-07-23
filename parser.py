"""Module for Argument Parser"""

import argparse

from . import __version__


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
