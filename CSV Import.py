'''PS_Export = API.courses()
PS_Export = API.CLData() #not sure how/where we want these classes to be instantiated/placed
PS_Export.CSVimport('PS_Class_Table.csv')'''

import API
PS_Export = API.CLData()
PS_Export.CSVimport('temp.class_table.csv')
PS_Export.associate()
PS_Export.concat('sectionID','term','subject','catalog','section')
PS_Export.concat('CourseIdentifier','subject','catalog')
print(PS_Export.DataVertical)

#PS_Export.constructReport('SectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'Begin-Date', 'end-date', 'OrgUnitIdentifier', 'class-title', 'credits', 'DeliveryMode', 'Location', 'Description', 'CrossListingIdentifier')
PS_Export.constructReport('SectionID', 'term', 'CourseIdentifier', 'subject', 'catalog', 'section', 'begin-date', 'end-date', 'class-title', 'credits')