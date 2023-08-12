import pandas as pd

df = pd.read_excel('EntryTemplate.xlsx', sheetname='0') # can also index sheet by name or fetch all sheets
mylist = df['column name'].tolist()
print(mylist)