import pandas as pd

df = pd.read_excel('EntryTemplate.xlsx') # can also index sheet by name or fetch all sheets

name = df['NAME'].tolist()
somaiyaid = df['SOMAIYA_ID'].tolist()
rollno = df['ROLLNO'].tolist()
ia1 = df['IA1'].tolist()
ia2 = df['IA2'].tolist()
ia = df['IA'].tolist()
ise = df['ISE'].tolist()
ese = df['ESE'].tolist()
ca = df['CA'].tolist()
tot = df['TOTAL'].tolist()

for i in range (len(ese)):
    if tot[i] < 40 or ese[i] < 35:
        print(name[i], "got a kt")

