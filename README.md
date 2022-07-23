<div id='top'></div>

<div align='center'>

# log-finder

</div>


Script to find registers with specific arguments inside Apache log files.


<div id='running'></div>

## Running the script
Now, you can run the script to search for multiples arguments from many ways.

* `-i`: used to search for matching patterns over every line of the log file.
* `-e`: used to get only the registers that `DON'T` match the arguments.
* `-s`: used to get the request time. See <a href="#specif">Specificity</a> for more information.

In all three ways, you can search using multiple arguments at once separated by a space only. They can even be combined, like the examples below.
But, every argument of the search will be saved into a separate text file.

Below are some examples of how you can run it:
```
$ python main.py -i abc 192.168.1.1  # get all records that have abc or 192.168.1.1
$ python main.py -e Mozilla 192.168.1.  # get all records that DON'T have Mozilla or 192.168.1.
$ python main.py -s 15 10 1 90  # get all records that the request time is greater or equal than 15 or 10 or 1 or 90 seconds
$ python main.py -i 192.168. abc -e Mozilla -s 10 -i Chrome  # all searches combined
```
For now, all the searches are independent of each other.
In the future, I'm going to add a flag to combine two or more arguments into one search pattern.

<p align='right'>(<a href='#top'>back to top</a>)</p>


<div id='specif'></div>

## Specificity
The Apache log file can be configured with several different ways. See <a href="https://httpd.apache.org/docs/2.4/logs.html" target="_blank">Apache Log Documentation v2.4</a> for more information.

Once you have the exact arrangement of your log file, the exact position of your time request, you will only have to change the index value in `I_REQ_TIME`.

<p align='right'>(<a href='#top'>back to top</a>)</p>


<div id='todo'></div>

## TODO
* [ ] Implement multiple criterias per search. Now, it's only one per file.

<div id='done'></div>

## DONE
* [X] Implement a log file with the history of searches.


<div id='history'></div>

## Update History
* v1.4.0: Logger and Multifiles:
    * The search now is case-insensitive.
    * Created `logger.py` to manage the log file `log-finder-log`.
    * Created `__init__.py` file to store version and author.
    * Created `parser.py` file to manipulate argparser functions.
    * Created `remove_txt.py` file to remove all the results of the search. For development.
    * Better code organization with the creation of `util.py` file.
    * Better code inside `main.py` file.
    * Added the log file `apache_logs.log` for tests.
    * Fixed some Engllish misspell.
    * `.gitignore` updated.
    * `README.md` updated.
* v1.3.1: Match Counter:
    * Added matches counter.
    * Better README.
* v1.3.0: ArgumentParser:
    * Argument Parser added to project.
        * See <a href="#running">Running the script</a> for details.
    * Use of Path library to manage files.
    * The function `read_log_file` now uses yields instead then return a huge list of all records. Much better performance and saver memory.
    * Better comments.
    * Now shows the execution time at the end.
* v1.2.1: Better Comments and Messages:
    * Better documentation.
    * Messages of starting and ending.
* v1.2.0: Includent Excludent Update:
    * Fixed minor translations.
    * Constant for encoding format.
    * Better variable names.
    * Better documentation.
    * Added specific searches:
        * Includents: search all matches of the arguments.
        * Excludents: search all except the matches with the prefix '-'.
        * sec=: search by time request (greater or equal) at in specific position, given the `I_REQ_TIME` value.
    * Fixed the issue with the request time search.
* v1.1.0: English Update:
    * Translated to english.
    * Readme improved.
    * Better documentation.
    * Minor code improvements.
* v1.0.0: First Commit:
    * Repository creation.
    * First version added (in Portuguese and poor documentation).

<p align='right'>(<a href='#top'>back to top</a>)</p>
