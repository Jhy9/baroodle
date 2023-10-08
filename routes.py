from app import app
from flask import render_template,request,redirect,url_for
import users
import courses
import teachers
import students
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
    return redirect("/")

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
        if courses.create(users.get_uid(),course_name, description):
            return render_template("teacher-main.html", username = users.get_name(), courses = teachers.get_courses(), message = "Kurssin luonti onnistui")
        return render_template("course-creator.html", message = "Kurssin luonti epäonnistui")
    
@app.route("/show-courses")
def show_courses():
    if users.get_account_type()!= "Student":
        return redirect("main")
    return render_template("joinable-courses.html", courses = students.get_joinable_courses())

@app.route("/add-tests")
def add_tests():
    testfile.create_test()
    testfile.add_attendances()
    return render_template("index.html", message = "Testihenkilöt ja kurssit lisätty")

@app.route("/course/<id>")
def show_course_page(id):
    if request.method == "GET":
        if courses.permission_check(id) == True:
            return render_template("course-main-admin.html",course = courses.load_main(id))
        return render_template("course-main.html",course= courses.load_main(id),attendance = students.check_attendance(id))
    
@app.route("/join/<cid>")
def join_course(cid):
    students.attend_course(cid,users.get_uid())
    return redirect(url_for('show_course_page', id = cid))