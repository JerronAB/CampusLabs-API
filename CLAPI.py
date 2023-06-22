#Current Goals:
#   Currently, accessing/retrieving/testing basicDataTypes using a CLData class is circuitous
#   Need to shape it up using dunder methods on the basicDataTypes class. 
#   Finally, do general QA/logic-checking on all CLData methods. I got this out way too quickly. 

class basicDataTypes: #once things get more complex, this class will be used by CLData to represent columns
    def __init__(self,name='dataType',aliasList=[],validator: callable =None,dataMod: callable =None):
        self.name = name
        self.aliasList = aliasList
        self.validator = validator
        self.dataModder = dataMod
    def __eq__(self,string):
        return self.__contains__(string)
    def __contains__(self,string):
        if string.lower() in [item.lower() for item in self.aliasList]: return True
        if string.lower() == self.name: return True
        else: return False
    def validateData(self,data):
        return self.validator(data) # do we also want to raise Exception()
    def aliasMatch(self,alias):
        return alias.lower() in self.aliasList
    def modData(self,list_of_data):
        stripper = lambda input: input.strip() #just throwing this in anyway
        data = [stripper(cell) for cell in list_of_data]
        try:
            data = [self.dataModder(cell) for cell in data]
            return data
        except:
            return data

class CLData: 
    def __init__(self) -> None:
        self.DataHorizontal = tuple()
        self.ColumnsHorizontal = []
        self.DataVertical = {}
        self.dataAliases = {}

    def constructReport(self, reportDictionary: dict):
        #whole thing almost works, but it's very messy and unintuitive
        self.syncData('vertical')
        if not all([column.lower() in (name.lower() for name in self.dataAliases.keys()) for key,column in reportDictionary.items()]): raise Exception('One or more columns in the given list is not present in the basicDataType dictionary, or is not a created column.')
        #next we move the data to match this constructed list
        grabVal = lambda value: [key for key,val in reportDictionary.items() if val == value]
        self.DataVertical = {grabVal(column)[0]:data for column,data in self.DataVertical.items() if column in list(reportDictionary.values())}
        self.syncData('horizontal')

    def concat(self,new_column_name: str,*columns: str): #takes basic data types and allows you to concatenate them into a new column; CLData.concat("sectionID","term","course","section")
        self.syncData('vertical')  #needs data synced vertically
        self.dataAliases[new_column_name] = basicDataTypes(name=new_column_name)
        self.DataVertical[new_column_name] = []
        indices = [self.ColumnsHorizontal.index(column) for column in columns]
        for row in self.DataHorizontal:
            output = ''.join([row[index].strip() for index in indices]) 
            #gets indices of each column, concatenates lists to DataHorizontal
            self.DataVertical[new_column_name].append(output)
        print('Complete... syncing data back to horizontal attributes. ')
        self.syncData('horizontal') #resync the data horizontally

    def associate(self): #this whole stanza is awful
        #this should essentially rename columns if they match an alias above
        self.syncData('auto')
        for index,columnName in enumerate(self.ColumnsHorizontal):
            for key,datatype in self.dataAliases.items():
                if datatype.aliasMatch(columnName): self.ColumnsHorizontal[index] = datatype.name
        self.syncData('vertical')
        for key,data in self.DataVertical.items(): 
            for name,datatype in self.dataAliases.items():
                if key in datatype: #this is possible because of the __contains__ attribute on basicDataTypes
                    self.DataVertical[key] = datatype.modData(data)
        keys = list(self.DataVertical.keys())
        key = keys[0]
        vertLength = len(self.DataVertical[key])              
        for basicDataType in self.dataAliases.values():
            if basicDataType == 'INSERTION':
                print(f'During association, an insertable datatype, {basicDataType.name} was detected.')
                self.DataVertical[basicDataType.name] = ['' for i in range(vertLength)]
                self.DataVertical[basicDataType.name] = basicDataType.modData(self.DataVertical[basicDataType.name])
        self.syncData('horizontal')

    def setDataHorizontal(self, data):
        print(f'setData running on iterable with {len(data)} items.')
        self.DataHorizontal = [item for item in data]
        self.lastSync = 'horizontal'
        self.integrityCheck()

    def addRow(self, line: list):
        self.Data += (line,)

    def addRows(self,rows: list):
        for row in rows: self.addRow(row)
        self.integrityCheck()

    def syncData(self, syncTo: str):
        if syncTo == 'vertical': self.syncToVert()
        elif syncTo == 'horizontal': self.syncToHor()
        elif syncTo == 'auto' and self.lastSync == 'vertical': self.syncToHor() 
        #determines what to sync based on last synced item
        elif syncTo == 'auto' and self.lastSync == 'horizontal': self.syncToVert()

    def syncToVert(self):
        print('Syncing data to vertical dictionaries... ',end='')
        self.DataVertical = {columnName: [row[index] for row in self.DataHorizontal] for index,columnName in enumerate(self.ColumnsHorizontal)}
        self.lastSync = 'vertical'
        print('Done.')

    def syncToHor(self):
        print('Syncing data to horizontal lists... ',end='')
        self.ColumnsHorizontal.clear()
        self.ColumnsHorizontal = [columnName for columnName in self.DataVertical.keys()]
        name, data = next(iter(self.DataVertical.items())) #accesses first value in dictionary
        length = len(data)
        self.DataHorizontal = []
        for index in range(length):
            self.DataHorizontal.append([data[index] for columnName,data in self.DataVertical.items()]) #generating a list of lists
        self.integrityCheck()
        self.lastSync = 'horizontal'

    def addDataType(self, name: str, aliases: list, validator=None, datamodifier=None):
        self.dataAliases[name] = basicDataTypes(name,aliases,validator,datamodifier)
    def insertDataType(self, name: str, validator=None, datamodifier=None): #inserts data if none exists
        self.addDataType(name, ['INSERTION'], validator, datamodifier)

    def mapRows(self, mappedFunction: callable): 
        self.Data = [mappedFunction(row) for row in self.DataHorizontal if row is not None]
        return [mappedFunction(row) for row in self.Data if row is not None]

    def deDup(self, dedupColumn: str): #make this nicer and cleaner
        self.syncData('horizontal')
        index = self.ColumnsHorizontal.index(dedupColumn)
        dedupping_set = set()
        dedupped_list = [item for item in self.DataHorizontal if item[index] not in dedupping_set and not dedupping_set.add(item[index])] #set() does not allow duplicate values. Here we add all items to a set on each loop, and stop loop if item is in set already
        self.setDataHorizontal(dedupped_list)
        self.syncData('vertical')

    def CSVexport(self,filename: str):
        from csv import writer
        nonetoString = lambda cells: [str(cell or '') for cell in cells]
        print(f'Writing to... {filename}\n')
        with open(filename,'w',newline='') as csv_file:
            my_writer = writer(csv_file, delimiter = ',')
            my_writer.writerow(nonetoString(self.ColumnsHorizontal))
            [my_writer.writerow(nonetoString(row)) for row in self.DataHorizontal]

    def CSVimport(self, filename: str):
        from csv import reader
        self.ColumnsHorizontal = []
        self.DataHorizontal = []
        self.DataVertical = []
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile: #UTF-8
                self.filename = filename
                newname = filename.split('\\')
                self.name = newname[-1].replace('.csv','')
                csvData = [row for row in reader(csvfile)]
                self.ColumnsHorizontal = [(lambda inputStr: inputStr.replace("ï»¿",""))(colName) for colName in csvData.pop(0)]
                self.setDataHorizontal(csvData)

    def integrityCheck(self): #this will have to check both vertical and horizontal types now
        print(f'Running integrity check... ',end='')
        if not all(isinstance(line, list) for line in self.DataHorizontal): raise TypeError("tableData data must be a tuple of lists.")
        if not all(len(line) == len(self.ColumnsHorizontal) for line in self.DataHorizontal): raise Exception("Items in self.DataHorizontal do not have the same length as self.ColumnsHorizontal")
        print('Passed.')

    def prune(self): #needs lots of QA later
        self.syncData('auto')
        #for cell in columns, 
        #run validator
        # if validator failed, remove that index of item from all
        indexes_to_prune = []
        for keys,cols in self.DataVertical.items():
            validatorFx = None
            for alias,dataType in self.dataAliases.items():
                if dataType.aliasMatch(keys):
                    validatorFx = dataType.validator
                    break
            if validatorFx is None: break
            for index,cell in enumerate(cols):
                if not validatorFx(cell):
                    indexes_to_prune.append(index)
        for index in indexes_to_prune:
            for keys in self.DataVertical.keys():
                self.DataVertical[keys][index] = 'REMOVE'
        for keys in self.DataVertical.keys():
            self.DataVertical[keys] = [item for item in self.DataVertical[keys] if item != 'REMOVE']
        self.syncData('horizontal')