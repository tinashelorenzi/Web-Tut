from flask import Flask, render_template, request, redirect, session
import hashlib,sqlite3

app = Flask(__name__)
app.secret_key = "eb2a7c994f75e51521cbf87623d5c1eb13e3a525"

@app.route("/")
def index():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
    username = request.form["usrname"]
    password = request.form["passcode"]
    text_bytes = password.encode()
    result = (hashlib.md5(text_bytes)).hexdigest()
    conn = sqlite3.connect('./data/login.db')
    c = conn.cursor()
    query = "SELECT password FROM credentials WHERE username = ?"
    try:
        c.execute(query, (username,))
        data = c.fetchone()[0]
        if data == result:
            session["username"] = username
            session["loggedin"] = True
            return redirect("/home")
        else:
            return "Login failed"
    except:
        return "User does not exist"
    
@app.route('/home')
def home():
    if session["loggedin"]:
        return render_template("dashboard.html",person=session["username"])
    else:
        return redirect("/")

@app.route("/logout",methods=["POST"])
def logout():
    session["loggedin"] = False
    session["username"] = ""
    return redirect("/")
