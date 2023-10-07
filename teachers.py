from db import db
from sqlalchemy import text
from flask import session

def get_courses():
    sql = text('SELECT id, course_name FROM courses WHERE creator =:uid')
    query = db.session.execute(sql,{"uid":session.get("uid")})
    return query.fetchall()
