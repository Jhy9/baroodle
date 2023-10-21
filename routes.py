from app import app
from flask import render_template,request,redirect,url_for, flash
import users
import courses
import teachers
import students
import inputCheck
import testfile

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
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        account_type = request.form["account_type"]
        check_result = inputCheck.registration(username,password)
        if check_result != True:
            flash(check_result)
            return render_template("register.html")
        if users.register(username,password,account_type):
            users.login(username, password)
            return redirect("/main")
        else:
            flash("Käyttäjää ei pystytty lisäämään tietokantaan. Tarkista tietokantayhteys.")
            return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if users.get_uid() != False:
        return redirect("/main")
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password) is False:
            flash("Väärä käyttäjätunnus tai salasana")
            return render_template("login.html")            
        else:            
            return redirect("/main")

@app.route("/logout", methods = ["POST"])
def logout():
    users.logout()
    flash("Olet kirjautunut ulos")
    return redirect(url_for('index'))

@app.route("/main")
def main_page():
    if users.get_uid() == False:
        return redirect("/")
    if users.get_account_type()== "Student":
        return render_template("student-main.html", username = users.get_name(), courses = students.get_courses())
    else:
        return render_template("teacher-main.html", username = users.get_name(), courses = teachers.get_courses())
    
@app.route("/create", methods =["GET","POST"])
def create():
    if users.get_account_type()!= "Teacher":
        return redirect("/main")
    if request.method == "GET":
        return render_template("course-creator.html")
    if request.method == "POST":
        course_name = request.form["course_name"]
        description = request.form["description"]
        check_result = inputCheck.course_creation(course_name, description)
        if check_result != True:
            flash(check_result)
            return render_template("course-creator.html")
        if courses.create(users.get_uid(),course_name, description):
            flash("Kurssin luonti onnistui")
            return redirect(url_for('main_page'))
        flash("Kurssia ei pystytty lisäämään tietokantaan. Tarkista tietokantayhteys.")
        return render_template("course-creator.html")
    
@app.route("/show-courses")
def show_courses():
    if users.get_account_type()!= "Student":
        return redirect("main")
    return render_template("joinable-courses.html", courses = students.get_joinable_courses())

@app.route("/add-tests")
def add_tests():
    testfile.create_test()
    testfile.add_attendances()
    flash("Testihenkilöt ja kurssit lisätty")
    return redirect(url_for('index'))

