import pandas as pd
import sqlalchemy
import pymysql

a = input("Enter Excel file : ")
engine = sqlalchemy.create_engine('mysql+pymysql://harsh:Rogerharsh89#@localhost:3306/mydatabase')
pf = pd.read_excel('Entrytemplate.xlsx')

pf.to_sql('entries' , engine , if_exists='replace' , index=False)

print("data has been exported.......")




