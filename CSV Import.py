import CLAPI

Section_Export = CLAPI.CLData()
Section_Export.addDataType('term', ['term', 'period', 'time-period','time period'], lambda x: x.isnumeric() and len(x) == 4)
Section_Export.addDataType('subject', ['subject', 'subj'], lambda x: len(x) < 4)
Section_Export.addDataType('class-title', ['class-desc', 'class desc', 'class description', 'title', 'description'])
Section_Export.addDataType('catalog', ['catalog', 'catalogue', 'course num', 'course nbr', 'number'])
Section_Export.addDataType('section', ['section', 'section name', 'sectionid'])
Section_Export.addDataType('instructor', ['instructor', 'instructor name'], lambda x: x.lower() != 'staff')
Section_Export.addDataType('instructor-email', ['email', 'email address', 'instructor email', 'email id'])
Section_Export.addDataType('start-date', ['first day', 'start date', 'commencement date', 'startdate', 'begin date'])
Section_Export.addDataType('end-date', ['last day', 'end date','enddate', 'finish date', 'completion date', 'end date'])
Section_Export.addDataType('credits', ['credit hours', 'course units', 'units'])
Section_Export.addDataType('delivery-mode', ['delivery mode', 'mode', 'delivery'], datamodifier=lambda x: x.replace("HB", "Hybrid").replace("BP", "Face2Face").replace("BW", "Online").replace("BL", "Face2Face").replace("IB", "Face2Face").replace("P", "Face2Face"))  # I know I could squash this into a list that I unpack, but this is fine
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
Section_Export.prune()
Section_Export.constructReport(construction_dictionary)
Section_Export.deDup('SectionIdentifier')
Section_Export.CSVexport('../4226_sections_report_temp.csv')

Section_Export.CSVimport('temp.class_table_4224.csv')
Section_Export.associate()
Section_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section') #in the future I want this to persist beyond a single import
Section_Export.concat('CourseIdentifier', 'subject', 'catalog')
Section_Export.prune()
Section_Export.constructReport(construction_dictionary)
Section_Export.deDup('SectionIdentifier')
Section_Export.CSVexport('../4224_sections_report_temp.csv')

'''CourseIdentifier	Subject	Number	Title	Credits	OrgUnitIdentifier	Type	Description	CipCode
'''
'''
'CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CipCode'
'''

Course_Export = CLAPI.CLData()

organizational_units = ['OrgUnitIdentifier','Name', 'Acronym', 'ParentIdentifier', 'Type']
academic_term = ['TermIdentifier', 'Name','BeginDate', 'EndDate', 'ParentIdentifier', 'Type']
courses = ['CourseIdentifier', 'Subject', 'Number', 'Title','Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CIPCode']
sections = ['SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate','EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier']
instructors = ['PersonIdentifier', 'SectionIdentifier','FirstName', 'LastName', 'Email', 'Role']
