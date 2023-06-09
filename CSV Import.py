import CLAPI

Section_Export = CLAPI.CLData()
Section_Export.insertDataType('type', datamodifier=lambda x: 'Undergraduate')
Section_Export.insertDataType('org-unit', datamodifier=lambda x: '')
Section_Export.insertDataType('location', datamodifier=lambda x: '')
Section_Export.insertDataType('desc', datamodifier=lambda x: '')
Section_Export.insertDataType('crosslisting', datamodifier=lambda x: '')

# name-in-report:name-in-dataType
construction_dictionary = {'SectionIdentifier': 'SectionIdentifier', 
                           'TermIdentifier': 'term', 
                           'CourseIdentifier': 'CourseIdentifier', 
                           'Subject': 'subject', 
                           'CourseNumber': 'catalog',
                           'Number': 'section', 
                           'BeginDate': 'start-date', 
                           'EndDate': 'end-date', 
                           'Title': 'class-title', 
                           'Credits': 'credits', 
                           'DeliveryMode': 'delivery-mode', 
                           'OrgUnitIdentifier': 'org-unit', 
                           'Type': 'type',
                           'Location': 'location',
                           'Description': 'desc',
                           'CrossListingIdentifier': 'crosslisting'
                           }

Section_Export.CSVimport('temp.class_table_4226.csv')
Section_Export.associate()
Section_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section')
Section_Export.concat('CourseIdentifier', 'subject', 'catalog')
Section_Export.constructReport(construction_dictionary)
Section_Export.deDup('SectionIdentifier')
Section_Export.CSVexport('../4226_sections_report_temp.csv')

Section_Export.CSVimport('temp.class_table_4224.csv')
Section_Export.associate()
Section_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section') #in the future I want this to persist beyond a single import
Section_Export.concat('CourseIdentifier', 'subject', 'catalog')
Section_Export.constructReport(construction_dictionary)
Section_Export.deDup('SectionIdentifier')
Section_Export.CSVexport('../4224_sections_report_temp.csv')

'''
'CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CipCode'
'''

Course_Export = CLAPI.CLData()
Course_Export.insertDataType('type', datamodifier=lambda x: 'Undergraduate')
Course_Export.insertDataType('org-unit', datamodifier=lambda x: '')
Course_Export.insertDataType('desc', datamodifier=lambda x: '')
Course_Export.insertDataType('cipcode',datamodifier=lambda x: '')
construction_dictionary = {'CourseIdentifier': 'CourseIdentifier', 
                           'Subject': 'subject', 
                           'Number': 'catalog', 
                           'Title': 'class-title', 
                           'Credits': 'credits', 
                           'OrgUnitIdentifier': 'org-unit', 
                           'Type': 'type',
                           'Description': 'desc',
                           'CipCode': 'cipcode'
                           }
Course_Export.CSVimport('temp.class_table_4224.csv')
Course_Export.associate()
Course_Export.concat('CourseIdentifier', 'subject', 'catalog')
Course_Export.constructReport(construction_dictionary)
Course_Export.deDup('CourseIdentifier')
Course_Export.CSVexport('../4224_course_report_temp.csv')

Course_Export.CSVimport('temp.class_table_4226.csv')
Course_Export.associate()
Course_Export.concat('CourseIdentifier', 'subject', 'catalog')
Course_Export.constructReport(construction_dictionary)
Course_Export.deDup('CourseIdentifier')
Course_Export.CSVexport('../4226_course_report_temp.csv')

with open('temp.accounts.csv', 'r', encoding='ISO-8859-1') as csvfile: #UTF-8
    from csv import reader
    csvData = [row for row in reader(csvfile)]
    columnsHorizontal = [(lambda inputStr: inputStr.replace("ï»¿",""))(colName) for colName in csvData.pop(0)]
    externalIdIndex = columnsHorizontal.index('ExternalId')
    emailIndex = columnsHorizontal.index('Email')
    instrDict = {row[emailIndex]:row[externalIdIndex] for row in csvData}

def splitNameFirst(name):
    nameSplit = name.split(',')
    first = nameSplit[-1].split(' ')
    return first[0]
def splitNameLast(name):
    last = name.split(',')
    return last[0]

Instructors_Export = CLAPI.CLData()
Instructors_Export.copyDataType('PersonIdentifier','instructor-email',datamodifier=lambda email: instrDict.get(email,'UNKNOWN'))
Instructors_Export.copyDataType('firstname','instructor',datamodifier=splitNameFirst)
Instructors_Export.copyDataType('lastname','instructor',datamodifier=splitNameLast)
Instructors_Export.insertDataType('role',datamodifier=lambda x: 'Primary')
construction_dictionary = {'PersonIdentifier': 'PersonIdentifier', 
                           'SectionIdentifier': 'SectionIdentifier', 
                           'FirstName': 'firstname', 
                           'LastName':'lastname',
                           'Email': 'instructor-email', 
                           'Role': 'role', 
                           }
Instructors_Export.CSVimport('temp.class_table_4224.csv')
Instructors_Export.associate()
Instructors_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section')
Instructors_Export.constructReport(construction_dictionary)
Instructors_Export.deDup('SectionIdentifier')
Instructors_Export.CSVexport('../4224_instrs_report_temp.csv')

Instructors_Export.CSVimport('temp.class_table_4226.csv')
Instructors_Export.associate()
Instructors_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section')
Instructors_Export.constructReport(construction_dictionary)
Instructors_Export.deDup('SectionIdentifier')
Instructors_Export.CSVexport('../4226_instrs_report_temp.csv')

#this is just here for a reference
organizational_units = ['OrgUnitIdentifier','Name', 'Acronym', 'ParentIdentifier', 'Type']
academic_term = ['TermIdentifier', 'Name','BeginDate', 'EndDate', 'ParentIdentifier', 'Type']
courses = ['CourseIdentifier', 'Subject', 'Number', 'Title','Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CIPCode']
sections = ['SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate','EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier']
instructors = ['PersonIdentifier', 'SectionIdentifier','FirstName', 'LastName', 'Email', 'Role']
