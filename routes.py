from app import app
from flask import render_template,request,redirect,url_for, flash
import users
import courses
import teachers
import students
import inputCheck
import testfile
import coursePages

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

@app.route("/course/<id>")
def show_course_page(id):
    if request.method == "GET":
        return render_template("course-main.html",course= courses.load_main(id),privilege = courses.permission_check(id), pages = coursePages.get_pages(id))
    
@app.route("/join/<cid>")
def join_course(cid):
    students.attend_course(cid,users.get_uid())
    return redirect(url_for('show_course_page', id = cid))

@app.route("/course/<cid>/permissions", methods = ["GET","POST"])
def modify_privileges(cid):
    if request.method == "GET":
        if courses.permission_check(cid) != 4:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('show_course_page', id = cid))
        return render_template("privileges.html", attendees = courses.get_attendees(cid), course_id = cid)
    if request.method == "POST":
        user_id = request.form["user"]
        new_privilege = request.form["privilege"]
        if courses.change_privilege(user_id,cid,new_privilege) == True:
            flash("Oikeuksien muuttaminen onnistui")
        else:
            flash("Oikeuksien muuttaminen epäonnistui")
        return render_template("privileges.html", attendees = courses.get_attendees(cid), course_id = cid)
    
@app.route("/course/<cid>/create-page", methods = ["GET", "POST"])
def create_page(cid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('show_course_page', id = cid))
        return render_template("page-creator.html", course = cid)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        page_check = inputCheck.page_checker(title,content)
        if page_check != True:
            flash(page_check)
            render_template("page-creator.html", course = cid ,title = title, content = content)
        if coursePages.add_page(cid,title,content) == True:
            flash("Sivun lisäys onnistui")
            return redirect(url_for('show_course_page', id = cid))
        flash("Sivun lisäys epäonnistui")
        return render_template("page-creator.html", course = cid, title = title, content = content)
        
    
@app.route("/course/<cid>/<pid>/modify", methods = ["GET","POST"])
def modify_page(cid,pid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('show_course_page', id = cid))
        page = coursePages.get_page(pid)
        return render_template("page-modifyer.html", course = cid, page = pid,title = page.title, content = page.content)
    if request.method == "POST":
        new_title = request.form["title"]
        new_content = request.form["content"]
        page_check = inputCheck.page_checker(new_title,new_content)
        if page_check != True:
            flash(page_check)
            return render_template("page-modifyer.html", course = cid, page = pid, title = new_title, content = new_content)
        if coursePages.edit_page(pid,new_title,new_content) == True:
            flash("Kurssin muokkaus onnistui")
            return redirect(url_for('show_page', cid = cid, pid = pid))
        flash("Kurssin muokkaus epäonnistui")
        return render_template("page-modifyer.html", course = cid, page = pid, title = new_title, content = new_content)
    
@app.route("/course/<cid>/<pid>")
def show_page(cid,pid):
    page = coursePages.get_page(pid)
    return render_template("page.html", course = cid,pid = pid, page = page, privilege = courses.permission_check(cid))

@app.route("/course/<cid>/<pid>/delete")
def delete_page(cid,pid):
    if courses.permission_check(cid) < 3:
        return redirect(url_for('show_page', cid = cid, pid = pid))
    if coursePages.delete_page(pid) == True:
        flash("Sivun poisto onnistui")
        return redirect(url_for('show_course_page', id = cid))
    flash("Sivun poisto epäonnistui")
    return redirect(url_for('show_page', cid = cid, pid = pid))