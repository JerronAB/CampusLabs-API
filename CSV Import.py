import API

PS_Export = API.CLData()

PS_Export.addDataType('term', ['term', 'period', 'time-period','time period'], lambda x: x.isnumeric() and len(x) == 4)
PS_Export.addDataType('subject', ['subject', 'subj'], lambda x: len(x) < 4)
PS_Export.addDataType('class-title', ['class-desc', 'class desc','class description', 'title', 'description'])
PS_Export.addDataType('catalog', ['catalog', 'catalogue', 'course num', 'course nbr'])
PS_Export.addDataType('section', ['section', 'section name', 'sectionid'])
PS_Export.addDataType('instructor', ['instructor', 'instructor name'])
PS_Export.addDataType('instructor-email',['email', 'email address', 'instructor email', 'email id'])
PS_Export.addDataType('start-date', ['first day', 'start date','commencement date', 'startdate', 'begin date'])
PS_Export.addDataType('end-date', ['last day', 'end date','enddate', 'finish date', 'completion date', 'end date'])
PS_Export.addDataType('credits', ['credit hours', 'course units', 'units'])
PS_Export.addDataType('delivery-mode', ['delivery mode', 'mode', 'delivery'],datamodifier=lambda x: x.replace("HB", "Hybrid").replace("BP", "Face2Face").replace("BW", "Online").replace("BL","Face2Face").replace("IB","Face2Face").replace("P","Face2Face")) #I know I could squash this into a list that I unpack, but this is fine

PS_Export.CSVimport('2temp.class_table.csv')
PS_Export.associate()
PS_Export.concat('sectionID', 'term', 'subject', 'catalog', 'section')
PS_Export.concat('CourseIdentifier', 'subject', 'catalog')
PS_Export.export('../report_temp.csv')

# PS_Export.constructReport('sectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'Begin-Date', 'end-date', 'OrgUnitIdentifier', 'class-title', 'credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier')
PS_Export.constructReport('sectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'start-date', 'end-date', 'class-title', 'credits', 'delivery-mode','class-title','credits', inPlace=True)
print(PS_Export.DataVertical)
print(PS_Export.DataHorizontal)