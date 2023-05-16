from datetime import datetime
from collections import defaultdict

def printCommand(filename: str, flags: str):
    transaction =[]
    with open(f'ledgers/{filename}', 'r') as f: 
        # if there is NOT an include in the file 
        for line in f: 
            i = 0
            if line[0] == " ":
                while line[i] == " ":
                    i += 1
            if line[i] == ";" or line[i] == "=" or line[i] == "(" or "apply tag" in line or "end tag" in line:
                pass

            # if there is an include in the file 
            elif "!include" in line:
                with open(f'ledgers/{line[9:].strip()}', 'r') as f: 
                    for line in f: 
                        i = 0
                        if line[0] == " ":
                            while line[i] == " ":
                                i += 1
                        if line[i] == ";" or line[i] == "=" or line[i] == "(" or "apply tag" in line or "end tag" in line:
                            pass
                        else:
                            if line[0].isdigit(): 
                                transaction.append(line.strip())
                            else:
                                transaction.append(line.strip())
            else:
                if line[0].isdigit(): 
                    transaction.append(line.strip())
                else:
                    transaction.append(line.strip())

    data = createOuput(transaction, flags)
    printData(data, flags)

def createOuput(lines, flags):
    ledger = {}
    data = {}
    index = 0
    tempValue = 0

    # the format that will be used to save the data is the following 
    # it will be an object and the key will be the date and string, 
    # the value inside will be an object the first value will be the 
    # transaction and the second value will be transaction to where the money goes
    for i,x in enumerate(lines):
        if x[0].isdigit():
            if data:
                ledger[x] = data
            data = {}
        else:
            # second line 
            if ((i+1)%3 != 0):
                for i,char in enumerate(x):
                    if char == "$" or char.isdigit() or char == "-" or char == ",":
                        break
                    else:
                        index = i+1
                key = (x[:index]).strip()
                value = (x[index:len(x)]).strip()
                tempValue = value
                data[key] = value
            # third line in the transaction
            else:
                flag = 0
                for i,char in enumerate(x):
                    if char == "$" or char.isdigit() or char == "-" or char == ",":
                        break
                    else:
                        index = i+1

                key = (x[:index]).strip()
                value = (x[index:len(x)]).strip()
                # if we have to get the value from the previous transaction 
                if value == "":
                    value = tempValue
                    flag = 1
                else:
                    value = value

                if flag == 1: 
                    if "-" in value: 
                        data[key] = value[1:]
                    else:
                        data[key] = '-'+value
                else:
                    data[key] = value
    return ledger

def printData(ledger, flags):
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    BLACK = '\033[30m'

    if "sort" in flags:
        ledger = dict(sorted(ledger.items(), key=lambda x: datetime.strptime(x[0].split()[0], '%Y/%m/%d'), reverse=True))

    for i, j in ledger.items():
        RED = '\033[31m'
        GREEN = '\033[32m'
        BLUE = '\033[34m'
        BLACK = '\033[30m'
        inc = 0
        print(f"{BLACK}{i}") 

        for key, value in (ledger[i]).items():
            key = key.ljust(40)

            if (inc%2 == 0):
                if "-" in value and "$" in value:
                    print(f"{BLUE}\t{key}{RED}{value.ljust(15)}")
                elif "-" in value and "BTC" in value:
                    print(f"{BLUE}\t{key}{RED}{value.ljust(15)}")
                elif "-" not in value and "$" in value:
                    print(f"{BLUE}\t{key}{GREEN}{value.ljust(15)}")
                elif "-" not in value and "BTC" in value:
                    print(f"{BLUE}\t{key}{GREEN}{value.ljust(15)}")
            elif (inc%2 == 1):
                if "-" in value and "$" in value:
                    print(f"{BLUE}\t{key}{RED}{value.ljust(15)}")
                elif "-" in value and "BTC" in value:
                    print(f"{BLUE}\t{key}{RED}{value.ljust(15)}")
                elif "-" not in value and "$" in value:
                    print(f"{BLUE}\t{key}{GREEN}{value.ljust(15)}")
                elif "-" not in value and "BTC" in value:
                    print(f"{BLUE}\t{key}{GREEN}{value.ljust(15)}")
            inc += 1
            
           