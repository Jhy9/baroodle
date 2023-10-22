from db import db
from flask import session
from sqlalchemy import text

def attendance_count(course_id):
    sql = text('SELECT COUNT(*) as ac FROM course_attendance WHERE course_id=:course AND privilege = 1')
    return db.session.execute(sql,{"course":course_id}).fetchone()

def course_exercise_attendees(course_id):
    sql = text('SELECT COUNT(DISTINCT ca.account_id) as exa '
               'FROM course_attendance as ca JOIN exercise_submissions as sub ON sub.user_id = ca.account_id '
               'WHERE ca.course_id =:course_id')
    return db.session.execute(sql,{"course_id":course_id}).fetchone()

def user_set_points(user_id, course_id):
    sql = text('SELECT set.set_name, SUM(sub.points) as own, (select sum(ex.max_points) from exercises as ex where ex.set_id = set.id) as max FROM '
               'exercise_set as set LEFT JOIN exercises as ex ON set.id = ex.set_id '
               'LEFT JOIN exercise_submissions as sub ON ex.id = sub.exercise_id '
               'WHERE set.course_id=:course_id AND  sub.user_id =:user_id AND set.availability_status != :status '
               'GROUP BY set.id')
    return db.session.execute(sql,{"course_id":course_id, "user_id":user_id, "status":"hidden"}).fetchall()

def user_total_points(user_id,course_id):
    sql = text('SELECT sum(sub.points) as own '
               'FROM exercise_set as set JOIN exercises as ex on ex.set_id = set.id '
               'LEFT JOIN exercise_submissions as sub on ex.id = sub.exercise_id '
               'WHERE set.availability_status != :status AND set.course_id =:course_id '
               'AND sub.user_id =:user_id')
    return db.session.execute(sql,{"course_id":course_id, "user_id":user_id, "status":"hidden"}).fetchone()

def course_max_points(course_id):
    sql= text('SELECT SUM(ex.max_points) as max FROM exercise_set as set LEFT JOIN exercises as ex ON ex.set_id = set.id WHERE set.course_id =:course_id AND set.availability_status != :status')
    return db.session.execute(sql,{"course_id":course_id, "status":"hidden"}).fetchone()

def course_student_points(course_id):
    sql = text('SELECT sum(sub.points) as points, att.account_id as id FROM course_attendance as att LEFT JOIN exercise_submissions as sub on att.account_id = sub.user_id '
               'WHERE att.course_id =:course '
               'GROUP BY att.account_id')
    return db.session.execute(sql,{"course":course_id})