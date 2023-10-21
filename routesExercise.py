from flask import render_template,request,redirect,url_for, flash, Blueprint
import users
import courses
import inputCheck
import exercises
import exerciseReviews
import exerciseSubmissions

exercise = Blueprint('exercise_routes',__name__,template_folder='templates/exercise')

@exercise.route("/course/<cid>/exercises", methods=["GET","POST"])
def exercise_main(cid):
    if request.method == "GET":
        if courses.permission_check(cid) < 1:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("exercise-main.html",privilege = courses.permission_check(cid), exercise_sets= exercises.get_sets(cid), course_id = cid)
    if request.method == "POST":
        status = request.form["visibility"]
        id = request.form["set"]
        if exercises.modify_set_availability(id,status) == True:
            flash("Tehtävien näkyvyyttä muokattu")
            return redirect(url_for('exercise_routes.exercise_main', cid = cid))
        flash("Näkyvyyden muokkaus epäonnistui")
        return redirect(url_for('exercise_routes.exercise_main', cid = cid))

@exercise.route("/course/<cid>/exercises/create-set",methods=["GET","POST"])
def exercise_set_create(cid,name = ""):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("set-create.html",course_id = cid,name=name)
    if request.method == "POST":
        set_name = request.form["name"]
        input_check = inputCheck.set_name_check(set_name)
        if input_check != True:
            flash(input_check)
            return render_template("set-create.html",course_id = cid)
        if exercises.create_set(cid,set_name) == True:
            flash("Tehtäväsarja luotu")
            return redirect(url_for('exercise_routes.exercise_main',cid = cid))
        flash("Tehtäväsarjan luominen epäonnistui")
        return render_template("set-create.html",course_id = cid,name=name)
    
@exercise.route("/course/<cid>/exercises/<sid>", methods=["GET","POST"])
def exercise_set(cid,sid):
    if request.method == "GET":
        if courses.permission_check(cid) < 1:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("set-main.html", exercises = exercises.get_set(sid,users.get_uid()), course = cid, set =sid, privilege = courses.permission_check(cid))
    if request.method == "POST":
        ex_id = request.form["ex_id"]
        answer = request.form["answer"]
        ex_type = int(request.form["type"])
        if ex_type == 1:
            flash("wow")
            if exerciseSubmissions.check_answer(ex_id,answer) == True:
                points = exercises.get_max_points(ex_id)     
            else:
                points = 0
            if exerciseSubmissions.add_submission(ex_id,answer,users.get_uid(),points) == True:
                flash("Palautus onnistui")
            else:
                flash("Palautus epäonnistui")
        else:
            if exerciseSubmissions.get_submission(ex_id,users.get_uid()) != None:
                if exerciseSubmissions.modify_submission(ex_id,answer,users.get_uid()) == True:
                    flash("Palautus onnistui")
                else:
                    flash("Palautus epäonnistui")
            else:
                if exerciseSubmissions.add_submission(ex_id,answer,users.get_uid()) == True:
                    flash("Palautus onnistui")
                else:
                    flash("Palautus epäonnistui")
        return render_template("set-main.html", exercises = exercises.get_set(sid,users.get_uid()), course = cid, set =sid, privilege = courses.permission_check(cid))
        


@exercise.route("/course/<cid>/exercises/<sid>/add-text", methods=["GET","POST"])
def add_exercise(cid,sid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("exercise-text.html",course = cid, set=sid)
    if request.method == "POST":
        assignment = request.form["assignment"]
        max_points = int(request.form["max_points"])
        if inputCheck.exercise_check(assignment,max_points) != True:
            flash(inputCheck.exercise_check(assignment,max_points))
            return render_template("exercise-text.html",course = cid, set=sid)
        if exercises.add_exercise(sid, assignment,max_points) == True:
            flash("Tehtävä lisätty")
            return redirect(url_for('exercise_routes.exercise_set',cid = cid,sid = sid))
        flash("Tehtävän lisääminen epäonnistui")
        return render_template("exercise-text.html",course = cid, set=sid)
        

        
@exercise.route("/course/<cid>/exercises/<sid>/add-multi", methods=["GET","POST"])
def add_exercise_multi(cid,sid):
    if request.method == "GET":
        if courses.permission_check(cid) < 3:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("exercise-multi.html",course = cid, set=sid)
    if request.method == "POST":
        assignment = request.form["assignment"]
        answer = request.form["answer"]
        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        max_points = int(request.form["max_points"])
        if inputCheck.exercise_multi_check(assignment,answer,option1,option2,option3, max_points) != True:
            flash(inputCheck.exercise_multi_check(assignment,answer,option1,option2,option3, max_points))
            return render_template("exercise-multi.html",course = cid, set=sid)
        if exercises.add_exercise_multi(sid,assignment,max_points, option1,option2,option3,answer)== True:
            flash("Tehtävä lisätty")
            return redirect(url_for('exercise_routes.exercise_set',cid = cid,sid = sid))
        flash("Tehtävän lisääminen epäonnistui")
        return render_template("exercise-multi.html",course = cid, set=sid)
    
@exercise.route("/course/<cid>/exercises/<sid>/review",methods= ["GET","POST"])
def add_reviews(cid,sid):
    if request.method == "GET":
        if courses.permission_check(cid) < 2:
            flash("Sinulla ei ole oikeuksia nähdä sivua")
            return redirect(url_for('course_routes.show_course_page', id = cid))
        return render_template("exercise-review.html",course=cid,set=sid,submissions = exerciseReviews.get_submissions(sid))
    if request.method == "POST":
        user = request.form["user_id"]
        exercise = request.form["ex_id"]
        points = int(request.form["points"])
        comment = request.form["comment"]
        if points < 0:
            flash("Pisteet eivät saa olla negatiivisia")
            return render_template("exercise-review.html",course=cid,set=sid,submissions = exerciseReviews.get_submissions(sid))
        elif points > exercises.get_max_points(exercise):
            flash("Pisteet eivät saa ylittää maksimimäärää")
            return render_template("exercise-review.html",course=cid,set=sid,submissions = exerciseReviews.get_submissions(sid))
        elif exerciseReviews.add_review(exercise,user,points,comment) == True:
            flash("Arviointi lisätty")
        else:
            flash("Arviointia ei voitu lisätä")
        return render_template("exercise-review.html",course=cid,set=sid,submissions = exerciseReviews.get_submissions(sid))
    