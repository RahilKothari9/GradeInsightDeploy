from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask_session import Session
from helpers import login_required, error
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from pathlib import Path
import sqlalchemy

mydb = mysql.connector.connect(
    host = "sql6.freesqldatabase.com",
    user = "sql6631415",
    password = "WUj4HddHA2",
    database = "sql6631415"
)

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

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM teacher_entry WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            if check_password_hash(account[2], password):
                session["user_id"] = account[0]
                x = str(session["user_id"])
                return redirect("/")
            return error("Wrong credentials!")
        else:
            return error("Wrong credentials!")
    else:
        return render_template("newlogin.html")
    
@app.route("/register", methods = ["GET", "POST"])
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
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE if not exists teacher_entry (teacher_id int NOT NULL AUTO_INCREMENT, email varchar(255) NOT NULL,password varchar(255), PRIMARY KEY (teacher_id))")
        sql = "INSERT INTO teacher_entry(email ,Password) VALUES (%s , %s)"
        val = (email, password_hash)
        mycursor.execute(sql , val)
        mydb.commit()
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
        course_name = request.form.get("name")
        user_id = session["user_id"]
        # Database Entry 1. course name 2. user who created the course
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE if not exists courses(course_id int NOT NULL AUTO_INCREMENT, teacher_id int, course_name VARCHAR(200) NOT NULL, PRIMARY KEY (course_id), FOREIGN KEY (teacher_id) REFERENCES teacher_entry(teacher_id));")
        sql = "INSERT INTO courses(teacher_id ,course_name) VALUES (%s , %s)"
        val = (user_id, course_name)
        mycursor.execute(sql , val)
        mydb.commit()
        return redirect("/courses")
@app.route("/courses")
@login_required
def display_courses():
    mycursor = mydb.cursor()
    
    sql = "SELECT * FROM courses WHERE teacher_id = %s"
    val = (session["user_id"],)
    mycursor.execute(sql , val)
    courses = mycursor.fetchall()
    #print(courses)
    if courses:
        
        return render_template("courses.html", courses=courses)
    else:
        return error("You do not have any courses(Frontend peeps add a link to addacourse page)")
@app.route("/course/<course_id>", methods = ["GET"])
@login_required
def course(course_id):
    mycursor = mydb.cursor()
    
    sql = "SELECT * FROM courses WHERE course_id = %s"
    val = (course_id,)
    mycursor.execute(sql , val)
    courses = mycursor.fetchone()
    if courses[1] != session["user_id"]:
        return error("You Cannot access this page")
    return render_template("courseview.html", course_id = course_id, course_info=courses)
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
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = course_id
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            # Make a db entry for the file for particular user and subject
            return redirect(url_for('upload', filename=filename))
    return render_template('dragdrop.html', course_id=course_id)

@app.route('/viewmarks/<filename>')
@login_required
def upload(filename):
    path = Path("uploads/" + filename)
    if(not path.is_file()):
        return error("You have not uploaded an excel file for this yet.(Frontend peeps link to /fileupload/course_id pls)")
    xl = 'uploads/'+filename
    df = pd.read_excel(io = xl)
    #print(1)
    print(df)
    return render_template('viewmarks.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == "__main__":
    app.run(debug="True")