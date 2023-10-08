from db import db
from sqlalchemy import text
from flask import session

def get_courses():
    sql = text('SELECT courses.id, courses.course_name FROM course_attendance LEFT JOIN courses ON courses.id = course_attendance.course_id WHERE course_attendance.account_id =:id')
    query = db.session.execute(sql, {"id":session.get("uid")})
    return query.fetchall()

def get_joinable_courses():
    sql = text('SELECT courses.id, courses.course_name, courses.course_description FROM courses WHERE courses.id NOT IN (SELECT course_id FROM course_attendance WHERE account_id =:account_id)')
    query = db.session.execute(sql, {"account_id":session.get("uid")})
    return query.fetchall()

def attend_course(course_id, student_id):
    try:
        sql = text('INSERT INTO course_attendance(course_id,account_id,completion_status) VALUES (:course_id,:account_id, :completion_status) ')
        db.session.execute(sql, {"course_id":course_id,"account_id":student_id,"completion_status":'INCOMPLETE'})
        db.session.commit()
    except:
        return False
    return True

def check_attendance(course_id):
    sql = text('SELECT count(*) FROM course_attendance WHERE course_id = :course_id AND account_id= :account_id')
    query = db.session.execute(sql, {"course_id":course_id, "account_id":session.get("uid")}).scalar()
    if query > 0:
        return True
    return False