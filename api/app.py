from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask_session import Session
from api.helpers import login_required, error
from werkzeug.security import check_password_hash, generate_password_hash
from pathlib import Path
import sqlite3
import smtplib
import ssl
from email.message import EmailMessage



sqliteConnection = sqlite3.connect('GradeInsight.db', check_same_thread=False)
mydb = sqliteConnection.cursor()


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            return error("Email not entered")
        if not request.form.get("password"):
            return error("Password not entered")
        
        email = request.form.get("email")
        password = request.form.get("password")
        password_hash = generate_password_hash(password)
        # Query from database for entry which matches email
        #Converted table to DataFrame and then checked whether the crediantials are available or not
        q = (email,)
        sql = 'SELECT * FROM teacher_entry WHERE email = ?'
        mydb.execute(sql, q)
        account = mydb.fetchone()
        if account:
            if check_password_hash(account[2], password):
                session["user_id"] = account[0]
                x = str(session["user_id"])
                return redirect("/")
            return error("Wrong credentials!")
        else:
            return error("Wrong credentials!")
    else:
        return render_template("login.html")
    
@app.route("/a21bcd", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("email"):
            return error("email not entered")
        if not request.form.get("password"):
            return error("password not entered")
        if not request.form.get("confirmation"):
            return error("confirmation not entered")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")



        if password != confirmation:
            return error("password and confirmation do not match")
        
        # Enter this info into database, email, password as a hash, and primary key will be user_id
        password_hash = generate_password_hash(password)
        mydb.execute("CREATE TABLE if not exists teacher_entry(teacher_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email CHAR(200) NOT NULL, password CHAR(250));")
        sql = "INSERT INTO teacher_entry(email ,Password) VALUES (%r, %r)" %(email, password_hash)
        mydb.execute(sql)
        sqliteConnection.commit()
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/addacourse", methods=['GET', 'POST'])
@login_required
def addacourse():
    if request.method == "GET":
        return render_template("addacourse.html")
    else:
        if not request.form.get("name"):
            return error("Course Name not entered")
        if not request.form.get("year"):
            return error("Course Year not entered")
        course_name = request.form.get("name")
        course_year = request.form.get("year")
        user_id = session["user_id"]
        # Database Entry 1. course name 2. user who created the course
        mydb.execute("CREATE TABLE if not exists [courses] ([course_id] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,[course_name] NVARCHAR(250)  NOT NULL,[teacher_id] INTEGER  NOT NULL,[class] NVARCHAR(250)  NOT NULL,FOREIGN KEY(teacher_id) REFERENCES teacher_entry(teacher_id));")
        sql = "INSERT INTO courses(teacher_id ,course_name, class) VALUES (%r , %r , %r)"%(user_id, course_name, course_year)
        mydb.execute(sql)
        sqliteConnection.commit()
        return redirect("/courses")

@app.route("/courses")
@login_required
def display_courses():
    
    val = (session["user_id"],)
    sql = "SELECT * FROM courses WHERE teacher_id = %r"%(val)
    mydb.execute(sql)
    courses = mydb.fetchall()
    #print(courses)
    return render_template("addCourse.html", courses=courses)
    
@app.route("/course/<course_id>", methods = ["GET"])
@login_required
def course(course_id):
    
    val = (course_id,)
    sql = "SELECT * FROM courses WHERE course_id = %r"%(val)
    mydb.execute(sql)
    courses = mydb.fetchone()
    if courses[2] != session["user_id"]:
        return error("You Cannot access this page")
    path = Path("uploads/" + course_id)
    if(not path.is_file()):
    
        return render_template("table.html", course_id = course_id, course_info=courses,)
    return redirect(url_for('upload', filename=course_id))
@app.route("/")
@login_required
def hello_world():
    return redirect("/courses")
    return "<p>Hello, World!</p>"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileupload/<course_id>', methods=['GET', 'POST'])
@login_required
def upload_file(course_id):
    if request.method == 'POST':
        
        if 'file' not in request.files:
            print("DIDNT GET FILE 1")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            print("DIDNT GET FILE 2")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("GOT FILE")
            filename = secure_filename(file.filename)
            filename = course_id
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            # Make a db entry for the file for particular user and subject
            return redirect(url_for('upload', filename=filename))
    return render_template('upload.html', course_id=course_id)

@app.route('/graph/<course_id>', methods=['GET'])
@login_required
def graph(course_id):
    xl = 'uploads/'+ course_id
    df = pd.read_excel(io = xl) # can also index sheet by name or fetch all sheets
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
    labels = ["0-10", "10-20", "20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100"]
    labels2 = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30"]
    labels3 = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50"]
    data = [0,0,0,0,0,0,0,0,0,0]
    data1 = [0,0,0,0,0,0,0,0,0,0]
    data2 = [0,0,0,0,0,0,0,0,0,0]

    for marks in tot:
        r = int(marks/10)
        
        data[r] += 1
    #print(tot)
    #return redirect("/courses")
    for marks in ese:
        r = int(marks/5)
        
        data1[r] += 1
    #print(ese)

    for marks in ise:
        r = int(marks/5)

        data2[r] += 1
    return render_template('graph.html', course_id=course_id, labels=labels, data=data, labels_ise=labels2, data_ise=data2, labels_ese=labels3, data_ese=data1)



@app.route('/viewmarks/<filename>')
@login_required
def upload(filename):
    path = Path("uploads/" + filename)
    if(not path.is_file()):
        return error("You have not uploaded an excel file for this yet.(Frontend peeps link to /fileupload/course_id pls)")
    xl = 'uploads/'+filename
    df = pd.read_excel(io = xl)
    #print(1)
    #print(df)
    return render_template('table.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, course_id=filename)

@app.route('/sendmail/<courseid>')
@login_required
def sendmail(courseid):
    path = Path("uploads/" + courseid)

    xl = 'uploads/'+courseid
    df = pd.read_excel(io = xl)
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
    email_sender = 'grade.insight1@gmail.com'
    email_password = ''
    
    for i in range(len(name)):
        email_receiver = somaiyaid[i]

        # Set the subject and body of the email
        subject = 'Marks Recieved'
        body = f"ISE: {ise[i]} \n IA1: {ia1[i]} \n IA2: {ia2[i]} \n IA: {ia[i]} \nCA: {ca[i]}\n ESE: {ese[i]}\n TOT = {tot[i]}"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    return redirect("/course/" + courseid)




@app.route('/delete', methods=['POST'])
def delete():
    id = request.form.get("course_id")
    #print(id)
    # HArsh delete entry where course_id = id
    val = (id)
    sql = "DELETE FROM courses WHERE course_id = %r"%(val)
    mydb.execute(sql)
    sqliteConnection.commit()
    return redirect("courses")
    #print("DELETING")

if __name__ == "__main__":
    #print(os.getenv('TEST'))
    app.run(debug="True")

