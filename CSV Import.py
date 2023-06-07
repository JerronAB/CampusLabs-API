'''PS_Export = API.courses()
PS_Export = API.CLData() #not sure how/where we want these classes to be instantiated/placed
PS_Export.CSVimport('PS_Class_Table.csv')'''

import API
PS_Export = API.CLData()
PS_Export.CSVimport('class_table.csv')
PS_Export.associate()
PS_Export.concat('sectionID','term','subject','catalog','section')
PS_Export.DataVertical