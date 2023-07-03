import pandas as pd
df = pd.read_excel("students.xlsx")
dict = df.to_dict()
print(dict)