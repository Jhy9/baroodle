from db import db
from flask import session
from sqlalchemy import text

def create(teacher_id, course_name, description):
    try:
        sql = text('INSERT INTO courses(course_name,creator, course_description) VALUES (:course_name, :creator,:course_description)')
        db.session.execute(sql, {"course_name":course_name,"creator":teacher_id,"course_description":description })
        db.session.commit()
    except:
        return False
    return True

def permission_check(course_id):
    sql = text('SELECT creator FROM courses WHERE id = :id')
    query = db.session.execute(sql, {"id":course_id}).scalar()
    if query == session.get("uid"):
        return 4
    sql = text('SELECT privilege FROM course_attendance WHERE course_id = :course_id AND account_id= :account_id')
    query = db.session.execute(sql, {"course_id":course_id, "account_id":session.get("uid")}).scalar()
    if query == None:
        return 0
    return query

def load_main(id):
    sql = text('SELECT * FROM courses WHERE id = :id')
    query = db.session.execute(sql,{"id":id})
    return query.fetchone()

def check_name_availability(course_name):
    sql = text('SELECT count(*) FROM courses WHERE course_name=:course_name')
    query = db.session.execute(sql, {"course_name":course_name}).scalar()
    if query > 0:
        return False
    return True

def get_attendees(id):
    sql = text('SELECT accounts.id,accounts.username, course_attendance.privilege FROM course_attendance LEFT JOIN accounts ON accounts.id = course_attendance.account_id WHERE course_id = :id')
    query = db.session.execute(sql,{"id":id})
    return query.fetchall()

def change_privilege(uid, course_id, privilege):
    try:
        sql = text('UPDATE course_attendance SET privilege = :privilege WHERE course_id = :course_id AND account_id = :uid')
        db.session.execute(sql, {"course_id":course_id,"uid":uid, "privilege":privilege})
        db.session.commit()
    except:
        return False
    return True
