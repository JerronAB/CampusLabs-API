import API

try:
    envDict = {}
    with open('.env') as envFile:
        for line in envFile:
            if line[0] != "#": key, value = line.strip().split('=')
            envDict[key.strip()] = value.strip()
except:
    print('.env file was not found, but is required for this script. Is your Python session running in the correct directory?\n')
    exit()

[print(f'{key}: {envDict[key]}') for key in envDict]

PS_Export = API.courses()
PS_Export = API.CLData() #not sure how/where we want these classes to be instantiated/placed
PS_Export.CSVimport('PS_Class_Table')