import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "harsh",
    password = "Rogerharsh89#",
    database = "mydatabase"
)

def data(a , b , c):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE if not exists teacher(Name VARCHAR(24), Rollno INT(255), Dept VARCHAR(200));")
    sql = "INSERT INTO teacher (Name , Rollno , Dept) VALUES (%s , %s , %s)"
    val = (a , b , c)
    mycursor.execute(sql , val)
    print("Value inserted !")

while True:
    a = input("Enter Name of student :")
    b = int(input("Enter Roll no :"))
    c = input("Enter Dept of student :")
    data(a , b , c)
    p = input("Do you want to continue ?(Y/N)")
    if (p == 'N'):
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE if not exists teacher(Name VARCHAR(24), Rollno INT(255), Dept VARCHAR(200));")
        sql = "INSERT INTO teacher (Name , Rollno , Dept) VALUES (%s , %s , %s)"
        val = (a , b , c)
        mycursor.execute(sql , val)
        break





