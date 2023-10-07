from app import app
from flask import render_template,request,redirect
import users
import courses
import teachers
import students

@app.route("/")
def index():
    if users.get_uid() != False:
        return redirect("/main")        
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if users.get_uid() != False:
        return redirect("/main")
    if request.method == "GET":
        return render_template("register.html", error= False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        account_type = request.form["account_type"]
        if users.register(username,password,account_type):
            users.login(username, password)
            return redirect("/main")
        else:
            return render_template("register.html", error = True)

@app.route("/login", methods=["GET","POST"])
def login():
    if users.get_uid() != False:
        return redirect("/main")
    if request.method == "GET":
        return render_template("login.html", error = False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password) is False:
            return render_template("login.html", error = True)            
        else:            
            return redirect("/main")

@app.route("/logout", methods = ["POST"])
def logout():
    users.logout()
    return render_template("index.html")

@app.route("/main")
def main_page():
    if users.get_uid() == False:
        return redirect("/")
    if users.get_account_type()== "Student":
        own_courses = students.get_courses()
        return render_template("student-main.html", username = users.get_name(), courses = own_courses)
    else:
        own_courses = teachers.get_courses()
        return render_template("teacher-main.html", username = users.get_name(), courses = own_courses)