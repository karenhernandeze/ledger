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

```
register
reg
```

   Show all transactions with running total.

```
print
```
   
   Print transactions in a format readable by ledger.


### Basic Supported Flags

```
--price-db
```
   Print price history for matching commodities in a format readable by ledger.

```
--sort 
-s
```
   Sort a report using VEXPR.

MUST FLAG: 

```
--file FILENAME
-f FILENAME
```
   Read FILE as a ledger file.


Some example commands are as follow:
```
my-ledger -f index.ledger bal
my-ledger -f index.ledger balance Asset Payable Expense
my-ledger -f index.ledger reg 
my-ledger -f Bitcoin.ledger reg Asset Payable Expense
my-ledger -f index.ledger reg Asset Payable Expense -s
my-ledger -f index.ledger print -s
my-ledger -f index.ledger print Bank Asset
```
To see some examples, you can go to the output folder and check the screenshots.
