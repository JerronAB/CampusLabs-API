#a few options here:
   # An importCSV function/class that can "intelligently" make several instantiations of our cours/section/instructor/account classes, and relate that information together
   # A single class that uses many instantiations of section, courses, instructors, etc. to make POST requests (as a method for each item)
   # 

#broad goals:
   # intake CSV files (and potentially other data formats)
   # use intaken data to:
     # determine data to be used for the CL API (courses, sections, instrs, accounts) (whether it's CSVs or JSON POST requests)
     # these determinations need to be resilient, error-correcting, and relationship-aware (i.e., no duplicate sections)
     # use wordlists to determine these relationships automatically
     # allow manual access and assignment to certain values (i.e. column "fname" relates to column firstname in accounts)


class APIData:
    def __init__(self) -> None:
        self.Columns = [] #this will not be "columns" in the future
    def matchColumn(self, string):
        if self.knownColumns is not None:
            ...
        else:
            #here, test if the string is like any of the 'columns'
            ...
    

class courses:
    def __init__(self) -> None:
        self.CourseIdentifier = ""
        self.Subject = ""
        self.Number = ""
        self.Title = ""
        self.Credits = ""
        self.OrgUnitIdentifier = ""
        self.Type = ""
        self.Description = ""
        self.CipCode = ""

class sections:
    def __init__(self) -> None:
        self.SectionIdentifier = ""
        self.TermIdentifier = ""
        self.CourseIdentifier = ""
        self.Subject = ""
        self.CourseNumber = ""
        self.Number = ""
        self.BeginDate = ""
        self.EndDate = ""
        self.OrgUnitIdentifier = ""
        self.Title = ""
        self.Credits = ""
        self.DeliveryMode = ""
        self.Location = ""
        self.Description = ""
        self.CrossListingIdentifier = ""

class instructors:
    def __init__(self) -> None:
        self.PersonIdentifier = ""
        self.SectionIdentifier = ""
        self.Firstname = ""
        self.Lastname = ""
        self.Email = ""
        self.Role = ""

class accounts:
    def __init__(self) -> None:
        self.ExternalId = ""
        self.FirstName = ""
        self.LastName = ""
        self.Email = ""

#not sure this is how we want to do this ultimately. 
class tableData:
    def __init__(self) -> None:
        self.Data = tuple()
        self.Columns = []
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

from csv import reader,writer #maybe this can just become a couple methods on the tableData class??
class CSVTableSubclass(tableData): #creates and interacts with tableData object
    def __init__(self, filename=None) -> None:
        tableData.__init__(self)
        if filename is not None: self.fileIntake(filename)
    def fileIntake(self, filename):
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile: #UTF-8
                self.filename = filename
                newname = filename.split('\\')
                self.name = newname[-1].replace('.csv','')
                csvData = [row for row in reader(csvfile)]
                self.Columns = list(map(lambda input_str: input_str.replace("ï»¿",""), csvData.pop(0)))
                self.setData(csvData)

