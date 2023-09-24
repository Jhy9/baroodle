from app import app
from flask import render_template,request
import user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        account_type = request.form["account_type"]
        if user.register(username,password,account_type):
            id = user.login(username,password)
            return render_template("main-page.html", id = id)
        else:
            return render_template("register-error.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        id = user.login(username,password)
        if id is False:
            return render_template("login-error.html")            
        else:            
            return render_template("main-page.html", id = id)

@app.route("/logout",methods=["POST"])
def logout():
    return render_template("index.html")
