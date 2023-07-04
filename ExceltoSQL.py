import pandas as pd
import sqlalchemy
import pymysql

def sqlentry():
    a = input("Enter Excel file : ")
    if a.endswith('.xlsx'):
        engine = sqlalchemy.create_engine('mysql+pymysql://harsh:Rogerharsh89#@localhost:3306/mydatabase')
        pf = pd.read_excel(a)

        pf.to_sql('entries' , engine , if_exists='replace' , index=False)

        print("data has been exported.......")
    else :
       print("Entered file is not an excel file....!!")
       sqlentry()

sqlentry()



