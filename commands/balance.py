# NEED TO FIND ANOTHER APPROACH FOR WHEN MORE THAN 1 TRANSACTION IS LISTED AND AT THE END THE DESTINATION
from collections import defaultdict

def balanceCommand(filename: str, flags: str):
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
                            if line[0].isdigit(): pass
                            else:
                                transaction.append(line.strip())
            else:
                if line[0].isdigit(): pass
                else:
                    transaction.append(line.strip())


    data = createOuput(transaction)
    printData(data, flags)

def createOuput(lines):
    ledger = {}
    i = 0
    index = 0
    tempValue = 0

    for i, line in enumerate(lines):
        # if the line is an odd number it is the money spent
        if (i%2 == 0 ):
            for i,char in enumerate(line):
                if char == "$" or char.isdigit() or char == "-" or char == ",":
                    break
                else:
                    index = i+1

            key = (line[:index]).strip()
            value = (line[index:len(line)]).strip()
            tempValue = value
            # check if key already exists and if yes, increment the value to the current one
            if key in ledger:
                ledger[key] += value
            else:
                ledger[key] = value

        # if the line is an even number it is the money to be paid to the given account 
        elif (i%2 != 0):
            flag = 0
            for i,char in enumerate(line):
                if char == "$" or char.isdigit() or char == "-" or char == ",":
                    break
                else:
                    index = i+1

            key = (line[:index]).strip()
            value = (line[index:len(line)]).strip()
            if value == "":
                value = tempValue
                flag = 1
            else:
                value = value

            # check if key already exists and if yes, increment the value to the current one
            if key in ledger:
                # if the transactions doesn't specify the amount
                if flag == 1: 
                    if "-" in value: 
                            ledger[key] += value[1:]
                    else:
                        ledger[key] += '-'+value
                else:
                    ledger[key] += value

            else:
                if flag == 1: 
                    if "-" in value: 
                            ledger[key] = value[1:]
                    else:
                        ledger[key] = '-'+value
                else:
                    ledger[key] = value
    return ledger

def printData(ledger, flags):
    output = {}
    sumTotalBTC = {}
    merged_currencies = defaultdict(list)
    final_BTC_sum = 0
    final_Dls_sum = 0

    for k, v in ledger.items():
        account = k.split(':')[0]

        # for dlls replace with + for the BTC currency replace with | 
        v = v.replace("$", "+")
        v = v.replace("BTC", "|")
        # the delimiter will be + or -         
        v = v.replace("-+", "+-")

        if "|" in v:
            key = account
            nums = v.split('|')
            total = sum(float(num) for num in nums if num)
            total = round(total, 2)
            if key in sumTotalBTC:
                sumTotalBTC[key] += total
            else:
                sumTotalBTC[key] = total
        else:
            nums = v.split('+')
            total = sum(float(num) for num in nums if num)
            total = round(total, 2)
            if account in output:
                output[account] += total
            else:
                output[account] = total 

    # add the BTC character to the result 
    for k, v in sumTotalBTC.items():
        if flags:
            for i in flags: 
                if i in sumTotalBTC:
                    final_BTC_sum = final_BTC_sum + float(sumTotalBTC[i])
                    currency = "BTC" 
                    result = (str(sumTotalBTC[i]) + currency)
                    sumTotalBTC[i] = result
            break
        else:
            final_BTC_sum = final_BTC_sum + v
        currency = "BTC" 
        result = (str(v) + currency)
        sumTotalBTC[k] = result

    # add the $ character to the result 
    for k, v in output.items():
        if flags:
            for i in flags: 
                if i in output:
                    final_Dls_sum = final_Dls_sum + float(output[i])
                    currency = "$" 
                    result = (currency+str(output[i]))
                    output[i] = result
            break
        else:
            final_Dls_sum = final_Dls_sum + v
        currency = "$" 
        result = (currency+str(v))
        output[k] = result
        
    # merge both currencies into one dict 
    for key, value in output.items():
        merged_currencies[key].append(value)

    for key, value in sumTotalBTC.items():
        merged_currencies[key].append(value)
   
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    BLACK = '\033[30m'
    WHITE = '\033[37m'

    if flags:
        j = 0
        for i in flags:
            if i in merged_currencies:
                if len(merged_currencies[i]) == 1:
                    output = '{}'.format(*merged_currencies[i])
                else:
                    output = '{} {}'.format(*merged_currencies[i])
                padded_number = output.rjust(20, " ")
                if "-" in padded_number:
                    print(f"{RED}{padded_number}", f"{BLUE}{i}")  
                else:
                    print(f"{GREEN}{padded_number}", f"{BLUE}{i}")  
            else:
                print("Account does not exist: ", i)
            j += 1

        print(f"{WHITE}",'-' * 40)

        formatted_value_b = "{:.2f}".format(final_BTC_sum).rjust(16, " ")
        formatted_value_d = "{:.2f}".format(final_Dls_sum).rjust(18, " ")
        if final_Dls_sum < 0:
            print(f"{RED}$ {formatted_value_d}")  
        else:
            print(f"{GREEN}$ {formatted_value_d}")  
        if final_BTC_sum < 0:
            print(f"{RED}{formatted_value_b} BTC")  
        else:
            print(f"{GREEN}{formatted_value_b} BTC")  

    else:
        for k, v in merged_currencies.items():
            output = ' '.join(v).strip('[]')
            padded_number = output.rjust(20, " ")
            if "-" in padded_number:
                print(f"{RED}{padded_number}", f"{BLUE}{k}")  
            else:
                print(f"{GREEN}{padded_number}", f"{BLUE}{k}")  

        print(f"{BLACK}",'-' * 40)

        formatted_value_b = "{:.2f}".format(final_BTC_sum).rjust(16, " ")
        formatted_value_d = "{:.2f}".format(final_Dls_sum).rjust(18, " ")
        if final_Dls_sum < 0:
            print(f"{RED}$ {formatted_value_d}")  
        else:
            print(f"{GREEN}$ {formatted_value_d}")  
        if final_BTC_sum < 0:
            print(f"{RED}{formatted_value_b} BTC")  
        else:
            print(f"{GREEN}{formatted_value_b} BTC")  
