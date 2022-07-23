"""Open all log files in the current directory and use the arguments to find
all the matches.
"""

import source.util as u
import source.searcher as s


if __name__ == "__main__":
    u.clear_screen()
    s.start()
    u.finish()
