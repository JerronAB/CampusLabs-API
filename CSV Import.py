import API
PS_Export = API.CLData()
PS_Export.CSVimport('2temp.class_table.csv')
PS_Export.associate()
PS_Export.concat('sectionID','term','subject','catalog','section')
PS_Export.concat('CourseIdentifier','subject','catalog')


#PS_Export.constructReport('sectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'Begin-Date', 'end-date', 'OrgUnitIdentifier', 'class-title', 'credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier')
PS_Export.constructReport('sectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'start-date', 'end-date', 'class-title', 'credits')
print(PS_Export.constructed)