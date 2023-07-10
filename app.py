from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask_session import Session
from helpers import login_required, error
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
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

        # Query from database for entry which matches email
        #Converted table to DataFrame and then checked whether the crediantials are available or not..

        engine = sqlalchemy.create_engine('mysql+pymysql://sql6631415:WUj4HddHA2@sql6.freesqldatabase.com:3306/sql6631415')
        df = pd.read_sql_table("teacher_entry", engine)
        if((email in set(df["email"])) & (password in set(df["password"]))):
            return render_template("fileupload.html")
        else:
            return "Wrong credientials...!!"

        session["user_id"] = db_entry[0]["user_id"]
        return redirect("/")

    else:
        return render_template("login.html")
    
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

        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE if not exists teacher_entry (teacher_id int NOT NULL AUTO_INCREMENT, email varchar(255) NOT NULL,password varchar(255), PRIMARY KEY (teacher_id))")
        sql = "INSERT INTO teacher_entry(email ,Password) VALUES (%s , %s)"
        val = (email, password)
        mycursor.execute(sql , val)
        mydb.commit()


        print("Value inserted !")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/")
@login_required
def hello_world():
    return redirect("/fileupload")
    return "<p>Hello, World!</p>"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileupload', methods=['GET', 'POST'])
@login_required
def upload_file():
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
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            # Make a db entry for the file for particular user and subject
            return redirect(url_for('upload', filename=filename))
    return render_template('fileupload.html')

@app.route('/viewmarks/<filename>')
@login_required
def upload(filename):
    #get filename from db;
    
    xl = 'uploads/'+filename
    df = pd.read_excel(io = xl)
    return render_template('viewmarks.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == "__main__":
    app.run(debug="True")