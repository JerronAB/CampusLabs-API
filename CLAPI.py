#Current Goals:
#   Currently, accessing/retrieving/testing basicDataType using a CLData class is circuitous
#   To wrap up, do general QA/logic-checking on all CLData methods. I got this out way too quickly. 

class basicDataType: #once things get more complex, this class will be used by CLData to represent columns
    #eventually I want this to be a subclass of a dictionary
    def __init__(self,name,aliasList=[],validator: callable =None,dataMod: callable =None):
        self.name = name
        self.aliasList = aliasList
        self.validator = validator
        self.dataModder = dataMod
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        return self.name
    def __eq__(self,string_or_object):
        if type(string_or_object) is str: return self.__contains__(string_or_object)
        else: return self.name == string_or_object.name
    def __hash__(self) -> int:
        return hash(self.name)
    def __contains__(self,string):
        if string.lower() in [item.lower() for item in self.aliasList]: return True
        elif string.lower() == self.name: return True
        else: return False
    def validateData(self,data) -> bool:
        if self.validator is None: 
            print(f'No validator for {self.name}, returning True---')
            return True #data is always valid if we haven't defined validator
        return self.validator(data)
    def aliasMatch(self,alias):
        return alias.lower() in self.aliasList
    def modData(self,list_of_data):
        stripper = lambda input: input.strip() #just throwing this in anyway
        data = [stripper(cell) for cell in list_of_data]
        if self.dataModder is None: return data
        try:
            return [self.dataModder(cell) for cell in data]
        except:
            print(f'Error during data modification for {self.name}')
            return data

class CLData: 
    def __init__(self,importDefaultDataTypes=True) -> None:
        self.DataHorizontal = tuple()
        self.ColumnsHorizontal = []
        self.DataVertical = {}
        self.dataAliases = {}
        if importDefaultDataTypes:
            self.addDataType('term', ['term', 'period', 'time-period','time period'], lambda x: x.isnumeric() and len(x) == 4)
            self.addDataType('subject', ['subject', 'subj'], lambda x: len(x) < 4)
            self.addDataType('class-title', ['class-desc', 'class desc', 'class description', 'title', 'description'])
            self.addDataType('catalog', ['catalog', 'catalogue', 'course num', 'course nbr', 'number'])
            self.addDataType('section', ['section', 'section name', 'sectionid'])
            self.addDataType('instructor', ['instructor', 'instructor name'], lambda x: x.lower() != 'staff')
            self.addDataType('instructor-email', ['email', 'email address', 'instructor email', 'email id'])
            self.addDataType('start-date', ['first day', 'start date', 'commencement date', 'startdate', 'begin date'])
            self.addDataType('end-date', ['last day', 'end date','enddate', 'finish date', 'completion date', 'end date'])
            self.addDataType('credits', ['credit hours', 'course units', 'units'])
            self.addDataType('delivery-mode', ['delivery mode', 'mode', 'delivery'], datamodifier=lambda x: x.replace("HB", "Hybrid").replace("BP", "Face2Face").replace("BW", "Online").replace("BL", "Face2Face").replace("IB", "Face2Face").replace("P", "Face2Face"))  # I know I could squash this into a list that I unpack, but this is fine

    def constructReport(self, reportDictionary: dict):
        #whole thing almost works, but it's very messy and unintuitive
        self.syncData('vertical')
        if not all([column.lower() in (name.lower() for name in self.dataAliases.keys()) for key,column in reportDictionary.items()]): raise Exception('One or more columns in the given list is not present in the basicDataType dictionary, or is not a created column.')
        self.prune()
        #next we move the data to match this constructed list
        grabVal = lambda value: [key for key,val in reportDictionary.items() if val == value]
        newDict = {}
        for column, data in self.DataVertical.items():
            if column in list(reportDictionary.values()): 
                print(f'Column: {column} is in reportDictionary...')
                if type(column) is basicDataType: newDict[grabVal(column.name)[0]] = data
                else: newDict[grabVal(column)[0]] = data
        self.DataVertical = newDict
        self.syncData('horizontal')

    def concat(self,new_column_name: str,*columns: str): #takes basic data types and allows you to concatenate them into a new column; CLData.concat("sectionID","term","course","section")
        self.syncData('vertical') #needs data synced vertically
        self.dataAliases[new_column_name] = basicDataType(name=new_column_name)
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
                if datatype.aliasMatch(columnName): self.ColumnsHorizontal[index] = datatype
        self.syncData('vertical')
        for key,data in self.DataVertical.items(): 
            if type(key) is basicDataType: self.DataVertical[key] = key.modData(data)
        keys = list(self.DataVertical.keys())
        key = keys[0]
        vertLength = len(self.DataVertical[key])              
        for _basicDataType in self.dataAliases.values():
            if _basicDataType == 'INSERTION':
                print(f'During association, an insertable datatype, {_basicDataType.name} was detected.')
                self.DataVertical[_basicDataType] = ['' for i in range(vertLength)]
                self.DataVertical[_basicDataType] = _basicDataType.modData(self.DataVertical[_basicDataType])
            if _basicDataType == 'COPIED':
                print(f'A datatype to copy, {_basicDataType} was found during association. Modding {_basicDataType.aliasList[1]} data with function: {_basicDataType.dataModder}')
                self.DataVertical[_basicDataType] = _basicDataType.modData(self.DataVertical[_basicDataType.aliasList[1]])
        self.syncData('horizontal')

    def setDataHorizontal(self, data):
        print(f'setData running on iterable with {len(data)} items.')
        self.DataHorizontal = [item for item in data]
        self.lastSync = 'horizontal'
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
        self.dataAliases[name] = basicDataType(name,aliases,validator,datamodifier)
    def insertDataType(self, name: str, validator=None, datamodifier=None): #inserts data if none exists
        self.addDataType(name, ['INSERTION'], validator, datamodifier)
    def copyDataType(self, newName: str, oldName: str, datamodifier=None):
        self.dataAliases[newName] = basicDataType(newName,['COPIED',oldName],dataMod=datamodifier)

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

    def prune(self): #needs lots of QA later; can't forget tricks like recursion or while loops
        self.syncData('auto')
        indexes_to_remove = []
        for keys,cols in self.DataVertical.items():
            if type(keys) is not basicDataType: continue
            if keys.validator is None: continue
            for index,cell in enumerate(cols):
                if not keys.validateData(cell):
                    indexes_to_remove.append(index)
        for index in indexes_to_remove:
            for keys in self.DataVertical.keys():
                self.DataVertical[keys][index] = 'REMOVE'
        for keys in self.DataVertical.keys():
            self.DataVertical[keys] = [item for item in self.DataVertical[keys] if item != 'REMOVE']
        self.syncData('horizontal')