# log-finder

Script to find registers with specific arguments inside Apache log files.


## Running the script
To execute, just run like the examples below:

```
$ python main.py 192.168.0.0  # here, it'll look up for all occurrences of the given IP address
$ python main.py -iPhone  # here, it'll look up for all occurrences that doesn't have the word 'iPhone'
$ python main.py sec=60  # here, it'll look up for a request time equal or greater than 1 minute
```

You can use multiple arguments too:
```
$ python main.py 192.168.0.0 sec=60 -iPhone  # here, it's doing all the searches above with one command
```


## Specificity
The Apache log file can be configured with several different ways. See [Apache Log Documentation v2.4](https://httpd.apache.org/docs/2.4/logs.html) for more information.

Once you have the exact arrangement of your log file, the exact position of your time request, you will only have to change the index value in `I_REQ_TIME`.


## TODO
* [ ] Implement multiple criterias per search. Now, it's only one per file.


## Update History
* v1.2.1: Better comments:
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
