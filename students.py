from db import db
from sqlalchemy import text
from flask import session

def get_courses():
    sql = text('SELECT courses.id, courses.course_name FROM course_attendance LEFT JOIN courses ON courses.id = course_attendance.course_id WHERE course_attendance.account_id =:id')
    query = db.session.execute(sql, {"id":session.get("uid")})
    return query.fetchall()

def get_unattended_courses():
    sql = text('SELECT courses.id, courses.course_name, courses.description FROM course_attendance LEFT JOIN courses ON courses.id = course_attendance.course_id WHERE course_attendance.account_id !=:id')
    query = db.session.execute(sql, {"id":session.get("uid")})
    return query.fetchall()

def attend_course(course_id):
    try:
        sql = text('INSERT INTO course_attendance(course_id,account_id,completion_status) VALUES (:course_id,:account_id,"INCOMPLETE") ')
        db.session.execute(sql, {"course_id":course_id,"account_id":session.get("uid")})
        db.session.commit()
    except:
        return False
    return True
