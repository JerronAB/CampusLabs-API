#broad goals:
   # intake CSV files (and potentially other data formats)
   # use intaken data to:
     # determine data to be used for the CL API (courses, sections, instrs, accounts) (whether it's CSVs or JSON POST requests)
     # these determinations need to be resilient, error-correcting, and relationship-aware (i.e., no duplicate sections)
     # use wordlists to determine these relationships automatically
     # allow manual access and assignment to certain values (i.e. column "fname" relates to column firstname in accounts)

#CSVimport function should automatically associate basicDataTypes using wordlists
#after associations are made, the next question is: how do we track what certain CL Core Data requirements need

#next steps are working on construct and concat

class basicDataTypes: #once things get more complex, this class will be used by CLData to represent columns
    def __init__(self,name='dataType',aliasList=[],validator: callable =None,dataMod: callable =None):
        self.name = name
        self.aliasList = aliasList
        self.validator = validator
        self.dataMod = dataMod
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
        self.dataAliases = {
            'term':basicDataTypes('term',['term', 'period', 'time-period', 'time period'],lambda x: x.isnumeric() and len(x) == 4),
            'subject': basicDataTypes('subject',['subject', 'subj'], lambda x: len(x) < 4),
            'class-title': basicDataTypes('class-title',['class-desc', 'class desc', 'class description', 'title','description']),
            'catalog': basicDataTypes('catalog',['catalog', 'catalogue', 'course num', 'course nbr']),
            'section': basicDataTypes('section',['section', 'section name', 'sectionid']),
            'instructor': basicDataTypes('instructor',['instructor', 'instructor name']),
            'instructor-email': basicDataTypes('instructor-email',['email', 'email address', 'instructor email','email id']),
            'start-date': basicDataTypes('start-date',['first day', 'start date', 'commencement date', 'startdate', 'begin date']),
            'end-date': basicDataTypes('end-date',['last day', 'end date', 'enddate', 'finish date', 'completion date', 'end date']),
            'credits': basicDataTypes('credits',['credit hours', 'course units', 'units']),
            'delivery-mode':basicDataTypes('delivery-mode',['delivery mode','mode','delivery'])
        }
    def constructReport(self,*columns: str):
        self.syncData('auto')
        self.constructed = []
        #on the next line, I need to make sure that concatenated lines are also being considered 
        if not all([column.lower() in (name.lower() for name in self.dataAliases.keys()) for column in columns]): raise Exception('One or more columns in the given list is not present in the basicDataType dictionary, or is not a created column.')
        self.constructed = [self.dataAliases[item] for item in columns] #builds a list of our basicDataType objects, in order based on user input
        #next we move the data to match this constructed list
    def concat(self,new_column_name: str,*columns: str): #takes basic data types and allows you to concatenate them into a new column; CLData.concat("sectionID","term","course","section")
        self.syncData('vertical')  #needs data synced vertically
        self.dataAliases[new_column_name] = basicDataTypes(name=new_column_name)
        self.DataVertical[new_column_name] = []
        indices = [self.ColumnsHorizontal.index(column) for column in columns]
        for row in self.DataHorizontal:
            output = ''.join([row[index].strip() for index in indices]) #gets indices of each column, concatenates lists to DataHorizontal
            self.DataVertical[new_column_name].append(output)
        print('Complete... syncing data back to horizontal attributes. ')
        self.syncData('horizontal') #resync the data horizontally
    def associate(self): #this should essentially rename columns if they match an alias above; GOT TO SHAPE THIS UP, it's just ugly
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
        elif syncTo == 'auto' and self.lastSync == 'vertical': self.syncToHor() #determines what to sync based on last synced item
        elif syncTo == 'auto' and self.lastSync == 'horizontal': self.syncToVert()
    def syncToVert(self):
        self.DataVertical = {columnName: [row[index] for row in self.DataHorizontal] for index,columnName in enumerate(self.ColumnsHorizontal)}
        self.lastSync = 'vertical'
    def syncToHor(self):
        print('Performing syncToHor()')
        self.ColumnsHorizontal = [columnName for columnName in self.DataVertical.keys()]
        name, data = next(iter(self.DataVertical.items())) #accesses first value in dictionary
        length = len(data)
        print(f'Length of data: {length}')
        self.DataHorizontal = []
        for index in range(length):
            self.DataHorizontal.append([data[index] for columnName,data in self.DataVertical.items()]) #generating a list of lists
        self.integrityCheck()
        self.lastSync = 'horizontal'
    def mapRows(self, mappedFunction: callable, inPlace: bool =False): #here, I need to explore using lambda & map, vs. using eval(), vs. using exec()
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
    def export(self,filename: str): #looking at export function to make sure it doesn't export empty cells
        from csv import writer
        #this uses the 'writer' function from the csv module
        nonetoString = lambda cells: [str(cell or '') for cell in cells]
        print(f'Writing to... {filename}')
        with open(filename,'w',newline='') as csv_file:
            my_writer = writer(csv_file, delimiter = ',')
            my_writer.writerow(nonetoString(self.ColumnsHorizontal))
            for row in self.Data:
                my_writer.writerow(nonetoString(row))
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
    def remove(self,data_type, illegal_strings):
        pass
    def repair():
        pass

class courses(CLData): #here I need to flesh out a minor example of a subclass that will represent our core data in the future
    def __init__(self) -> None:
        CLData.__init__(self)

organizational_units = ['OrgUnitIdentifier', 'Name', 'Acronym', 'ParentIdentifier', 'Type']
academic_term = ['TermIdentifier', 'Name', 'BeginDate', 'EndDate', 'ParentIdentifier', 'Type']
courses_ = ['CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CIPCode']
sections = ['SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate', 'EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier']
instructors = ['PersonIdentifier', 'SectionIdentifier', 'FirstName', 'LastName', 'Email', 'Role']
