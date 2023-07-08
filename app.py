from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask_session import Session
from helpers import login_required, error
from werkzeug.security import check_password_hash, generate_password_hash

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
        # For now Im keeping 12345 as password
        db_entry = [{"user_id" : 1, "email" : "abc@gmail.com", "password" : generate_password_hash("12345")}]

        if len(db_entry) != 1 or not check_password_hash(db_entry[0]["password"], password):
            return error("Invalid username or password")

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