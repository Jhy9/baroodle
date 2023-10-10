from operator import truediv
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
        return True
    return False

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