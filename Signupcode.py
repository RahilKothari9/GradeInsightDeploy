import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "harsh",
    password = "Rogerharsh89#",
    database = "mydatabase"
)

def data(a , b , c):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE if not exists teacher_entry(Username VARCHAR(240), SomaiyaId VARCHAR(255), Password VARCHAR(200));")
    sql = "INSERT INTO teacher_entry(Username ,SomaiyaId ,Password) VALUES (%s , %s , %s)"
    val = (a , b , c)
    mycursor.execute(sql , val)
    print("Value inserted !")

    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE if not exists teacher_entry(Username VARCHAR(240), SomaiyaId VARCHAR(255), Password VARCHAR(200));")
    sql = "INSERT INTO teacher_entry(Username ,SomaiyaId ,Password) VALUES (%s , %s , %s)"
    val = (a , b , c)
    mycursor.execute(sql , val)

a = input("Enter Username :")
b = input("Enter SomaiyaID :")
c = input("Enter Password :")
data(a , b , c)
