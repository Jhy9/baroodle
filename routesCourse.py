from os import abort
from flask import render_template,request,redirect,url_for, flash, Blueprint, session
import users
import courses
import students
import inputCheck
import coursePages
import courseStats
course = Blueprint('course_routes',__name__,template_folder='templates/course')
@course.route("/course/<id>")
def show_course_page(id):
    if request.method == "GET":
        return render_template("course-main.html",course= courses.load_main(id),privilege = courses.permission_check(id), pages = coursePages.get_pages(id),token = session["csrf_token"])
    
@course.route("/course/<cid>/modify", methods = ["GET","POST"])
def modify_description(cid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("course-modify.html",course = cid , desc = courses.get_description(cid),token = session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort()
        new_desc = request.form["description"]
        if inputCheck.course_description_checker(new_desc) != True:
            flash(inputCheck.course_description_checker(new_desc))            
        else:
            if courses.change_description(cid,new_desc) == True:
                flash("Kuvauksen muokkaus onnistui")
                return redirect(url_for('course_routes.show_course_page', id = cid))
            flash("Kuvauksen muokkaus epäonnistui")
        return render_template("course-modify.html",course = cid, desc = new_desc,token = session["csrf_token"])
          
@course.route("/join/<cid>",methods =["POST"])
def join_course(cid):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort()
    students.attend_course(cid,users.get_uid())
    return redirect(url_for('course_routes.show_course_page', id = cid))

@course.route("/course/<cid>/permissions", methods = ["GET","POST"])
def modify_privileges(cid):
    if request.method == "GET":
        if courses.permission_check(cid) != 4:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("privileges.html", attendees = courses.get_attendees(cid), course_id = cid,token = session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort()
        user_id = request.form["user"]
        new_privilege = request.form["privilege"]
        if courses.change_privilege(user_id,cid,new_privilege) == True:
            flash("Oikeuksien muuttaminen onnistui")
        else:
            flash("Oikeuksien muuttaminen epäonnistui")
        return render_template("privileges.html", attendees = courses.get_attendees(cid), course_id = cid,token = session["csrf_token"])
    
@course.route("/course/<cid>/create-page", methods = ["GET", "POST"])
def create_page(cid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("page-creator.html", course = cid,token = session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort()
        title = request.form["title"]
        content = request.form["content"]
        page_check = inputCheck.page_checker(title,content)
        if page_check != True:
            flash(page_check)
            return render_template("page-creator.html", course = cid ,title = title, content = content,token = session["csrf_token"])
        if coursePages.add_page(cid,title,content) == True:
            flash("Sivun lisäys onnistui")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        flash("Sivun lisäys epäonnistui")
        return render_template("page-creator.html", course = cid, title = title, content = content,token = session["csrf_token"])
        
    
@course.route("/course/<cid>/<pid>/modify", methods = ["GET","POST"])
def modify_page(cid,pid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä pyydettyä sivua.")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        page = coursePages.get_page(pid)
        return render_template("page-modifyer.html", course = cid, page = pid,title = page.title, content = page.content,token = session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort()
        new_title = request.form["title"]
        new_content = request.form["content"]
        page_check = inputCheck.page_checker(new_title,new_content)
        if page_check != True:
            flash(page_check)
            return render_template("page-modifyer.html", course = cid, page = pid, title = new_title, content = new_content,token = session["csrf_token"])
        if coursePages.edit_page(pid,new_title,new_content) == True:
            flash("Kurssin muokkaus onnistui")
            return redirect(url_for('course_routes.show_page', cid = cid, pid = pid))
        flash("Kurssin muokkaus epäonnistui")
        return render_template("page-modifyer.html", course = cid, page = pid, title = new_title, content = new_content,token = session["csrf_token"])
    
@course.route("/course/<cid>/<pid>")
def show_page(cid,pid):
    page = coursePages.get_page(pid)
    return render_template("page.html", course = cid,pid = pid, page = page, privilege = courses.permission_check(cid),token = session["csrf_token"])

@course.route("/course/<cid>/<pid>/delete", methods = ["POST"])
def delete_page(cid,pid):
    if session["csrf_token"] != request.form["csrf_token"]:
            abort()
    if courses.permission_check(cid) < 3:
        return redirect(url_for('course_routes.show_page', cid = cid, pid = pid))
    if coursePages.delete_page(pid) == True:
        flash("Sivun poisto onnistui")
        return redirect(url_for('course_routes.show_course_page', id = cid))
    flash("Sivun poisto epäonnistui")
    return redirect(url_for('course_routes.show_page', cid = cid, pid = pid))

@course.route("/course/<cid>/statistics")
def course_stats(cid):
    if courses.permission_check(cid) == 0:
        return redirect(url_for('course_routes.show_course_page', id = cid))
    if courses.permission_check(cid) == 1:  
        return render_template("course-stats-student.html",course = cid , course_max = courseStats.course_max_points(cid),total_points = courseStats.user_total_points(users.get_uid(),cid),series = courseStats.user_set_points(users.get_uid(),cid))
    return render_template("course-stats-admin.html",course = cid, attendees = courseStats.attendance_count(cid), actives = courseStats.course_exercise_attendees(cid), students = courseStats.course_student_points(cid))
