#broad goals:
   # intake CSV files (and potentially other data formats)
   # use intaken data to:
     # determine data to be used for the CL API (courses, sections, instrs, accounts) (whether it's CSVs or JSON POST requests)
     # these determinations need to be resilient, error-correcting, and relationship-aware (i.e., no duplicate sections)
     # use wordlists to determine these relationships automatically
     # allow manual access and assignment to certain values (i.e. column "fname" relates to column firstname in accounts)

#import function should automatically associate basicDataTypes using wordlists
#after associations are made, the next question is: how do we track what certain CL Core Data requirements need


class basicDataTypes: #once things get more complex, this class will be used by CLData to represent columns
    def __init__(self,name='dataType',aliasList=[],validator=None,dataMod=None) -> None:
        self.name = name
        self.aliasList = aliasList
        self.validator = validator
    def validateData(data):
        if self.validator(data) is not True: raise Exception()
    def aliasMatch(self,alias):
        return alias in self.aliasList
    def modData(self):
        pass #here there will be a map function most likely

#not sure this is how we want to do this ultimately. 
class CLData:
    def __init__(self) -> None:
        self.Data = tuple()
        self.Columns = []
        self.dataAliases = {
            'term':basicDataTypes('term',['term', 'period', 'time-period', 'time period'],lambda x: x.isnumeric() and len(x) == 4),
            'subject': basicDataTypes('subject',['subject', 'subj'], lambda x: len(x) < 4),
            'class-title': basicDataTypes('class-title',['class-desc', 'class desc', 'class description', 'title','description']),
            'catalog': basicDataTypes('catalog',['catalog', 'catalogue', 'course num', 'course nbr']),
            'section': basicDataTypes('section',['section', 'section name', 'sectionid']),
            'instructor': basicDataTypes('instructor',['instructor', 'instructor name']),
            'instructor-email': basicDataTypes('instructor-email',['email', 'email address', 'instructor email','email id']),
            'start date': basicDataTypes('start date',['first day', 'start date', 'commencement date', 'startdate']),
            'end date': basicDataTypes('end date',['last day', 'end date', 'enddate', 'finish date', 'completion date']),
            'credits': basicDataTypes('credits',['credit hours', 'course units', 'units']),
            'delivery-mode':basicDataTypes('delivery-mode',['delivery mode','mode','delivery'])
        }
        for column in self.Data:
            for Alias in self.dataAliases:
                if column == Alias: basicDataTypes()
    def construct():
        pass
    def concat(new_column_name,*columns):
        pass
    def remove(data_type, illegal_strings):
        pass
    def repair():
        pass
    def setData(self, data):
        print(f'setData running on iterable with {len(data)} items.')
        self.Data = tuple([item for item in data]) 
        self.integrityCheck()
    def addRow(self, line):
        self.Data += (line,)
    def addRows(self,rows):
        for row in rows: self.addRow(row)
        self.integrityCheck()
    def mapRows(self, mappedFunction, inPlace=False): #here, I need to explore using lambda & map, vs. using eval(), vs. using exec()
        print(f'Function being passed: {mappedFunction}')
        print(f'Modifying in-place: {inPlace}')
        if inPlace is True: self.Data = [mappedFunction(row) for row in self.Data if row is not None]
        else: return [mappedFunction(row) for row in self.Data if row is not None]
    def integrityCheck(self):
        print(f'Running integrity check---')
        if not all(isinstance(line, list) and len(line) == len(self.Columns) for line in self.Data): raise TypeError("tableData data must be a tuple of lists with the same length as tableColumns")
        print('Passed.')
    def deDup(self, dedupColumn): #make this nicer and cleaner
        index = self.Columns.index(dedupColumn)
        dedupping_set = set()
        dedupped_list = [item for item in self.Data if item[index] not in dedupping_set and not dedupping_set.add(item[index])] #set() does not allow duplicate values. Here we add all items to a set on each loop, and stop loop if item is in set already
        self.Data = ()
        self.setData(dedupped_list)
    def export(self,filename): #looking at export function to make sure it doesn't export empty cells
        #this uses the 'writer' function from the csv module
        nonetoString = lambda cells: [str(cell or '') for cell in cells]
        print(f'Writing to... {filename}')
        with open(filename,'w',newline='') as csv_file:
            my_writer = writer(csv_file, delimiter = ',')
            my_writer.writerow(nonetoString(self.Columns))
            for row in self.Data:
                my_writer.writerow(nonetoString(row))
    def CSVimport(self):
        pass

class courses(CLData): #here I need to flesh out a minor example of a subclass that will represent our core data in the future
    def __init__(self) -> None:
        CLData.__init__(self)

organizational_units = ['OrgUnitIdentifier', 'Name', 'Acronym', 'ParentIdentifier', 'Type']
academic_term = ['TermIdentifier', 'Name', 'BeginDate', 'EndDate', 'ParentIdentifier', 'Type']
courses = ['CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CIPCode']
sections = ['SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate', 'EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier']
instructors = ['PersonIdentifier', 'SectionIdentifier', 'FirstName', 'LastName', 'Email', 'Role']
