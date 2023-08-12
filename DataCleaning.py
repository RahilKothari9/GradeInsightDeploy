import pandas as pd

df = pd.read_excel('EntryTemplate.xlsx') # can also index sheet by name or fetch all sheets
mylist = df['ROLLNO'].tolist()
print(mylist)