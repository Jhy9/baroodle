from db import db
from sqlalchemy import text
from flask import session

def create(teacher_id, course_name, description):
    try:
        sql = text('INSERT INTO courses(course_name,creator, course_description) VALUES (:name, :teacher_id,:descriptions)')
        db.session.execute(sql, {"name":course_name,"teacher_id":teacher_id,"description":description })
        db.session.commit()
    except:
        return False
    return True
