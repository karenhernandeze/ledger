# My Ledger: Command-Line Accounting

This is a Ledger implementation for the Ledger Program.
https://ledger-cli.org/doc/ledger3.html

## To Build The Program 

First install all the dependencies, then simply do this:

    $ git clone 
    $ cd my-ledger
    $ chmod +x my-ledger

Then you must ensure the script (my-ledger) is located in a directory included in your system's PATH variable. Alternatively, you can specify the absolute path when executing the script.

Finally: 

    $ source ~/.bash_profile

To activate. 

Now, you should be able to run the Python file with the desired flags by simply typing 

    $ ./my-ledger -f test/input/sample.dat reg

followed by any additional flags you want to pass.


The supported commands are as follows: 

The print command 

The print command prints out ledger transactions in a textual format that can be parsed by Ledger. They will be properly formatted, and output in the most economic form possible. The print command also takes a list of optional regexes, which will cause only those postings which match in some way to be printed. 

The print command can be a handy way to clean up a ledger file whose formatting has gotten out of hand.



The Basic Usage of the Command Line:

The basic syntax of any ledger command is:

    $ ledger -f || --file filename COMMAND [--FLAGS] 

A file must always be specified so the -f flag must always be included:

    $ ledger -f filename.ledger COMMAND


Basic Reporting Commands

balance
bal
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

