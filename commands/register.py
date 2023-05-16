from datetime import datetime

def registerCommand(filename: str, flags: str):
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
            # if the line is an odd number it is the money spent. Since there are 3 different
            # lines, the one that divides by 3 is the one where the money was sent to 
            if ((i+1)%3 != 0):
                for i,char in enumerate(x):
                    if char == "$" or char.isdigit() or char == "-" or char == ",":
                        break
                    else:
                        index = i+1
                key = (x[:index]).strip()
                value = (x[index:len(x)]).strip()
                tempValue = value

                if flags:
                    if "sort" in flags:
                        data[key] = value
                    else:
                        for i in flags: 
                            if i in key:
                                data[key] = value
                            continue
                else:
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

                if flags: 
                    if "sort" in flags:
                        data[key] = value
                    else:
                        for i in flags: 
                            if i in key:
                                if flag == 1: 
                                    if "-" in value: 
                                        data[key] = value[1:]
                                    else:
                                        data[key] = '-'+value
                                else:
                                    data[key] = value
                            continue
                else:
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

    final_BTC_sum = 0 #number
    final_Dls_sum = 0 #number
    prevValueDls = "" #string
    prevValueBtc = "" #string
    valueBTC = 0
    valueDLS = 0
    flag = 0   
    
    if "sort" in flags or "-s" in flags or "--sort" in flags:
        # Sort the dictionary by date in descending order
        ledger = dict(sorted(ledger.items(), key=lambda x: datetime.strptime(x[0].split()[0], '%Y/%m/%d'), reverse=True))

    for i in ledger:
        inc = 0
        print(f"{BLACK}{i}")  

        for key, value in (ledger[i]).items():
            if (inc%2 == 0):
                value = value.replace("$", "+")
                value = value.replace("BTC", "|")
                value = value.replace("-+", "+-")
                

                if "|" in value:
                    valueBTC = value.replace('|', "")
                    flag = 1
                    valueDLS = 0
                else:
                    valueDLS = value.replace('+', "")
                    valueBTC = 0

                key_string = key.ljust(40)
                final_Dls_sum = float(final_Dls_sum) + float(valueDLS)
                final_BTC_sum = float(final_BTC_sum) + float(valueBTC)
                
                prevValueDls = "${:.2f}".format(final_Dls_sum)
                prevValueBtc = "{:.2f}BTC".format(final_BTC_sum)
                
                if flag == 1:
                    if "-" in valueBTC:
                        color1 = RED
                    else:
                        color1 = GREEN
                    if "-" in prevValueDls:
                        color2 = RED
                    else:
                        color2 = GREEN
                    if "-" in prevValueBtc:
                        color3 = RED
                    else:
                        color3 = GREEN

                    # if ledger has only $ 
                    if final_BTC_sum == 0:
                        valueBTC = valueBTC + "BTC"
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}{color2}{prevValueDls}")
                    # if ledger has only BTC
                    elif final_Dls_sum == 0:
                        valueBTC = valueBTC + "BTC"
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}{color2}{prevValueBtc}")
                    # if ledger manages both 
                    else:
                        valueBTC = valueBTC + "BTC"
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}{color2}{prevValueDls} {color3}{prevValueBtc}")
                else:
                    if "-" in valueDLS:
                        color1 = RED
                    else:
                        color1 = GREEN
                    if "-" in prevValueDls:
                        color2 = RED
                    else:
                        color2 = GREEN
                    if "-" in prevValueBtc:
                        color3 = RED
                    else:
                        color3 = GREEN

                    if final_BTC_sum == 0:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueDls}")
                    elif final_Dls_sum == 0:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueBtc}")
                    else:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueDls} {color3}{prevValueBtc}")

            elif (inc%2 == 1):
                value = value.replace("$", "+")
                value = value.replace("BTC", "|")
                value = value.replace("-+", "+-")

                if "|" in value:
                    valueBTC = value.replace('|', "")
                    valueDLS = 0
                    flag = 1
                else:
                    valueDLS = value.replace('+', "")
                    valueBTC = 0
                    flag = 0

                key_string = key.ljust(40)
                final_Dls_sum = float(final_Dls_sum) + float(valueDLS)
                final_BTC_sum = float(final_BTC_sum) + float(valueBTC)

                prevValueDls = "${:.2f}".format(final_Dls_sum)
                prevValueBtc = "{:.2f}BTC".format(final_BTC_sum)
                
                if flag == 1:
                    if "-" in valueBTC:
                        color1 = RED
                    else:
                        color1 = GREEN
                    if "-" in prevValueDls:
                        color2 = RED
                    else:
                        color2 = GREEN
                    if "-" in prevValueDls:
                        color3 = RED
                    else:
                        color3 = GREEN
                    
                    # if ledger has only $ 
                    if final_BTC_sum == 0:
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}BTC{color2}{prevValueDls}")
                    # if ledger has only BTC
                    elif final_Dls_sum == 0:
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}BTC{color2}{prevValueBtc}")
                    else:
                        valueBTC = valueBTC + "BTC"
                        print(f"{BLUE}\t{key_string}{color1}{valueBTC.ljust(15)}{color2}{prevValueDls} {color3}{prevValueBtc}")
                else:
                    if "-" in valueDLS:
                        color1 = RED
                    else:
                        color1 = GREEN
                    if "-" in prevValueDls:
                        color2 = RED
                    else:
                        color2 = GREEN
                    if "-" in prevValueBtc:
                        color3 = RED
                    else:
                        color3 = GREEN
                    
                    if final_BTC_sum == 0:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueDls}")
                    elif final_Dls_sum == 0:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueBtc}")
                    else:
                        valueDLS = "$"+valueDLS
                        print(f"{BLUE}\t{key_string}{color1}{valueDLS.ljust(15)}{color2}{prevValueDls} {color3}{prevValueBtc}")
            inc += 1
