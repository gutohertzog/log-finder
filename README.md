# log-finder

Script to find registers with specific arguments inside Apache log files.


## Running the script
To execute, just run like below:

```
python main.py arg1 arg2 etc
```


## Specificity
The Apache log file can be configured with several different ways. See [Apache Log Documentation v2.4](https://httpd.apache.org/docs/2.4/logs.html) for more information.

For this, in specific, the time request is the last item configured.

If you want to reuse it to find the request time, you will have to change the code a bit. Check for the comments (like below) to see where to change.
```py
########## SPECIFIC BEGINS ##########
# code
########## SPECIFIC ENDS ##########
```
If you don't want the request time, you can change the `if RESP_TIME in arg:` condition to `if False:` (it's really ugly, I know). I will improve it later.


## TODO
* [ ] Add 3 separate criterias to use on the match system.
    * [ ] Inclusive search.
    * [ ] Exclusive search.
    * [ ] Search by time to execute.


## Update History
* v1.1.0: English Update
    * Translated to english.
    * Readme improved.
    * Better documentation.
    * Minor code improvements.
* v1.0.0: First Commit
    * Repository creation.
    * First version added (in Portuguese and poor documentation).
