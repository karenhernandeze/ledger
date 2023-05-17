# My Ledger: Command-Line Accounting

This is a Ledger implementation for the [Ledger Program]
(https://ledger-cli.org/doc/ledger3.html).

## To Build The Program 

First clone the repository:

    $ git clone 
    $ cd ledger
    $ chmod +x my-ledger

Then you must ensure the script (my-ledger) is located in a directory included in your system's PATH variable. Alternatively, you can specify the absolute path when executing the script.

Finally run to activate: 

    $ source ~/.bash_profile


Now, you should be able to run the Python file with the desired flags by simply typing 

    $ ./my-ledger -f index.ledger bal

followed by any additional flags you want to pass.



## The Basic Usage of the Command Line:

The basic syntax of any ledger command is:

    $ ledger -f filename COMMAND [--FLAGS] 

A file must always be specified so the -f flag must always be included:

    $ ledger -f filename.ledger COMMAND


### Basic Reporting Commands
```
balance
bal
```
    Show account balances.

register
reg
    Show all transactions with running total.

print
    Print transactions in a format readable by ledger.


Basic Supported Flags

--price-db
    Print price history for matching commodities in a format readable by ledger.

--sort VEXPR
-S VEXPR
    Sort a report using VEXPR.

MUST FLAG: 

--file FILE
-f FILE
    Read FILE as a ledger file.

