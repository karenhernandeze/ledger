import sys 
from commands.register import registerCommand
from commands.balance import balanceCommand
from commands.print import printCommand

# Accepted Commands :
accepted_commands = ["bal", "balance", "register", "reg", "print"] 
flags = ["--price-db", "--sort", "-s", "--file", "-f"]

# At least the file argument should be passed with the given file name
total_args = len(sys.argv)
if total_args < 3:
    raise Exception ("Enter a valid command: {\n\tbalance,\n\tbal,\n\tregister,\n\treg,\n\tprint\n}\nAnd specify the file name with the given flag (-f namefile, -file namefile)")

def checkCommand():
    cli = []
    for command in sys.argv:
        cli.append(command)
    flag = 0

    # get the value of the index for the file flag, the next value is the name of the file 
    if "-f" in cli:
        index = cli.index("-f")
    elif "-file" in cli:
        index = cli.index("-file")
    
    # BALANCE COMMAND MANAGEMENT 
    if "bal" in cli or "balance" in cli:
        # this condition is for when an account is passed 
        if len(cli) > 4:
            if "bal" in cli:
                index_bal = cli.index("bal") 
            else:
                index_bal = cli.index("balance") 
            # number of accounts requested
            number_accounts = len(cli) - (index_bal + 1)
            account = []
            for i in range(number_accounts):
                account.append(cli[index_bal + 1 + i])
            balanceCommand(cli[index+1], list(account))
        else:
            balanceCommand(cli[index+1], "")
    
    # REGISTER COMMAND MANAGEMENT 
    elif "register" in cli or "reg" in cli:
         # this condition is for when an account is passed 
        if "--sort" in cli or "-s" in cli:
            registerCommand(cli[index+1], "sort")
        else:
            registerCommand(cli[index+1], "")

    # PRINT COMMAND MANAGEMENT 
    elif "print" in cli:
        # this condition is for when an account is passed 
        if "--sort" in cli or "-s" in cli:
            printCommand(cli[index+1], "sort")
        else:
            printCommand(cli[index+1], "")

    # no command 
    elif "-f" not in cli or "-file" not in cli:
        raise Exception ("Enter a valid command: {\n\tbalance,\n\tbal,\n\tregister,\n\treg,\n\tprint\n}\nAnd specify the file name with the given flag (-f namefile, -file namefile)")


    
if __name__ == "__main__":
    checkCommand()