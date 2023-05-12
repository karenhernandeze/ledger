def printCommand(filename: str):
    print("Print")
    print(filename)
    with open(f'ledgers/{filename}', 'r') as f: 
        print("Success")
        print(f.read())




    return 0 
