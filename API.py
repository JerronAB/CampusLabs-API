#Current Goals:
#   Currently, accessing/retrieving/testing basicDataTypes using a CLData class is circuitous
#   Need to shape it up using dunder methods on the basicDataTypes class. 
#   Finally, do general QA/logic-checking on all CLData methods. I got this out way too quickly. 

class basicDataTypes: #once things get more complex, this class will be used by CLData to represent columns
    def __init__(self,name='dataType',aliasList=[],validator: callable =None,dataMod: callable =None):
        self.name = name
        self.aliasList = aliasList
        self.validator = validator
        self.dataMod = dataMod
    def __eq__(self,string):
        return self.__contains__(string)
    def __contains__(self,string):
        if string.lower() in [item.lower() for item in self.aliasList]: return True
        else: return False
    def validateData(self,data):
        return self.validator(data) # do we also want to raise Exception()
    def aliasMatch(self,alias):
        return alias.lower() in self.aliasList
    def modData(self,data):
        lambda data: data.strip() #just throwing this in anyway
        data = self.dataMod(data)

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
        print(f'{[grabVal(column)[0] for column,data in self.DataVertical.items() if column in list(reportDictionary.values())]} from \n{[column for column,data in self.DataVertical.items() if column in list(reportDictionary.values())]}')
        #it appears this line is screwing with the process/not working right. Exports have original names for columns 
        self.DataVertical = {grabVal(column)[0]:data for column,data in self.DataVertical.items() if column in list(reportDictionary.values())} 
        self.syncData('horizontal')
        self.associate()

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

    def associate(self): 
        #this should essentially rename columns if they match an alias above; GOT TO SHAPE THIS UP, it's just ugly
        for index,columnName in enumerate(self.ColumnsHorizontal):
            for key,datatype in self.dataAliases.items():
                if datatype.aliasMatch(columnName): self.ColumnsHorizontal[index] = datatype.name

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
        self.DataVertical = {columnName: [row[index] for row in self.DataHorizontal] for index,columnName in enumerate(self.ColumnsHorizontal)}
        self.lastSync = 'vertical'

    def syncToHor(self):
        print('Performing syncToHor()')
        self.ColumnsHorizontal.clear()
        self.ColumnsHorizontal = [columnName for columnName in self.DataVertical.keys()]
        name, data = next(iter(self.DataVertical.items())) #accesses first value in dictionary
        length = len(data)
        print(f'Length of data: {length}')
        self.DataHorizontal = []
        for index in range(length):
            self.DataHorizontal.append([data[index] for columnName,data in self.DataVertical.items()]) #generating a list of lists
        self.integrityCheck()
        self.lastSync = 'horizontal'

    def addDataType(self, name: str, aliases: list, validator=None, datamodifier=None):
        self.dataAliases[name] = basicDataTypes(name,aliases,validator,datamodifier)

    def mapRows(self, mappedFunction: callable, inPlace: bool =False): 
        #here, I need to explore using lambda & map, vs. using eval(), vs. using exec()
        print(f'Function being passed: {mappedFunction}')
        print(f'Modifying in-place: {inPlace}')
        if inPlace is True: self.Data = [mappedFunction(row) for row in self.DataHorizontal if row is not None]
        else: return [mappedFunction(row) for row in self.Data if row is not None]

    def deDup(self, dedupColumn: str): #make this nicer and cleaner
        index = self.ColumnsHorizontal.index(dedupColumn)
        dedupping_set = set()
        dedupped_list = [item for item in self.Data if item[index] not in dedupping_set and not dedupping_set.add(item[index])] #set() does not allow duplicate values. Here we add all items to a set on each loop, and stop loop if item is in set already
        self.Data = ()
        self.setDataHorizontal(dedupped_list)

    def CSVexport(self,filename: str):
        from csv import writer
        nonetoString = lambda cells: [str(cell or '') for cell in cells]
        print(f'Writing to... {filename}')
        with open(filename,'w',newline='') as csv_file:
            my_writer = writer(csv_file, delimiter = ',')
            my_writer.writerow(nonetoString(self.ColumnsHorizontal))
            [my_writer.writerow(nonetoString(row)) for row in self.DataHorizontal]

    def CSVimport(self, filename: str):
        from csv import reader
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile: #UTF-8
                self.filename = filename
                newname = filename.split('\\')
                self.name = newname[-1].replace('.csv','')
                csvData = [row for row in reader(csvfile)]
                self.ColumnsHorizontal = [(lambda inputStr: inputStr.replace("ï»¿",""))(colName) for colName in csvData.pop(0)]
                self.setDataHorizontal(csvData)

    def integrityCheck(self): #this will have to check both vertical and horizontal types now
        print(f'Running integrity check...')
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
