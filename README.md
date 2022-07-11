# log-finder

Script to find registers with specific arguments inside Apache log files.


## Running the script
Needs to be updated.


## Specificity
The Apache log file can be configured with several different ways. See [Apache Log Documentation v2.4](https://httpd.apache.org/docs/2.4/logs.html) for more information.

Once you have the exact arrangement of your log file, the exact position of your time request, you will only have to change the index value in `I_REQ_TIME`.


## TODO
* [ ] Implement multiple criterias per search. Now, it's only one per file.


## Update History
* v1.3.0 beta: ArgumentParser:
    * Adding argument parser to project.
    * Use of Path library to manage files.
    * Better comments.
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
