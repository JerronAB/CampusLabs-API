import API

PS_Export = API.CLData()
PS_Export.addDataType('term', ['term', 'period', 'time-period','time period'], lambda x: x.isnumeric() and len(x) == 4)
PS_Export.addDataType('subject', ['subject', 'subj'], lambda x: len(x) < 4)
PS_Export.addDataType('class-title', ['class-desc', 'class desc','class description', 'title', 'description'])
PS_Export.addDataType('catalog', ['catalog', 'catalogue', 'course num', 'course nbr', 'number'])
PS_Export.addDataType('section', ['section', 'section name','sectionid'])
PS_Export.addDataType('instructor', ['instructor', 'instructor name'],lambda x: x.lower() != 'staff')
PS_Export.addDataType('instructor-email',['email', 'email address', 'instructor email', 'email id'])
PS_Export.addDataType('start-date', ['first day', 'start date','commencement date', 'startdate', 'begin date'])
PS_Export.addDataType('end-date', ['last day', 'end date','enddate', 'finish date', 'completion date', 'end date'])
PS_Export.addDataType('credits', ['credit hours', 'course units', 'units'])
PS_Export.addDataType('delivery-mode', ['delivery mode', 'mode', 'delivery'],datamodifier=lambda x: x.replace("HB", "Hybrid").replace("BP", "Face2Face").replace("BW", "Online").replace("BL","Face2Face").replace("IB","Face2Face").replace("P","Face2Face")) #I know I could squash this into a list that I unpack, but this is fine
PS_Export.addDataType('type',['type'],datamodifier=lambda x: 'Undergraduate')
PS_Export.addDataType('org-unit',['orgunitidentifier','orgunit'],datamodifier=lambda x: '')

PS_Export.CSVimport('2temp.class_table.csv')
PS_Export.associate()
PS_Export.concat('SectionIdentifier', 'term', 'subject', 'catalog', 'section')
PS_Export.concat('CourseIdentifier', 'subject', 'catalog')

PS_Export.prune()

#PS_Export.constructReport('SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate', 'EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier')
PS_Export.constructReport({'SectionIdentifier':'SectionIdentifier', 'TermIdentifier':'term', 'CourseIdentifier':'CourseIdentifier', 'Subject':'subject', 'CourseNumber':'catalog', 'Number':'section', 'BeginDate':'start-date', 'EndDate':'end-date', 'Title':'class-title', 'Credits':'credits', 'DeliveryMode':'delivery-mode','OrgUnitIdentifier':'org-unit','Type':'type'})
PS_Export.CSVexport('../report_temp.csv')

#PS_Export.CSVimport('2temp.class_table.csv')
#PS_Export.associate()
#PS_Export.concat('CourseIdentifier','subject','number','Title','Credits','Type')

'''CourseIdentifier	Subject	Number	Title	Credits	OrgUnitIdentifier	Type	Description	CipCode'''
'''
'''
'CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CipCode'
'''

'SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate', 'EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier'
4226CIT105A0Y3	4226	CIT105	CIT	 105	A0Y3	8/15/2022	12/8/2022		Introduction to Computers	3.00	HYBRID	OWC		
'''

organizational_units = ['OrgUnitIdentifier', 'Name', 'Acronym', 'ParentIdentifier', 'Type']
academic_term = ['TermIdentifier', 'Name', 'BeginDate', 'EndDate', 'ParentIdentifier', 'Type']
courses_ = ['CourseIdentifier', 'Subject', 'Number', 'Title', 'Credits', 'OrgUnitIdentifier', 'Type', 'Description', 'CIPCode']
sections = ['SectionIdentifier', 'TermIdentifier', 'CourseIdentifier', 'Subject', 'CourseNumber', 'Number', 'BeginDate', 'EndDate', 'OrgUnitIdentifier', 'Title', 'Credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier']
instructors = ['PersonIdentifier', 'SectionIdentifier', 'FirstName', 'LastName', 'Email', 'Role']