from db import db
from flask import session
from sqlalchemy import text

def get_pages(course_id):
    sql = text('SELECT id,title,content FROM pages WHERE course_id = :id ORDER BY position ASC')
    query = db.session.execute(sql, {"id":course_id})
    return query.fetchall()

def get_page(id):
    sql = text('SELECT title,content FROM pages WHERE id = :id')
    query = db.session.execute(sql, {"id":id})
    return query.fetchone()

def add_page(course_id, title, content):
    sql = text('SELECT position FROM pages WHERE course_id = :id ORDER BY position DESC LIMIT 1')
    last = db.session.execute(sql, {"id":course_id}).scalar()
    if last == None:
        position = 1
    else:
        position = last + 1
    try:
        sql = text('INSERT INTO pages(course_id, title, content,position) VALUES (:course_id, :title,:content,:position)')
        db.session.execute(sql,{"course_id":course_id,"title":title,"content":content,"position":position})
        db.session.commit()
    except:
        return False
    return True

def edit_page(id, title, content):
    try:
        sql = text('UPDATE pages SET title = :title, content =:content WHERE id = :id')
        db.session.execute(sql,{"id":id, "title":title,"content":content})
        db.session.commit()
    except:
        return False
    return True

def delete_page(id):
    try:
        sql = text('DELETE FROM pages WHERE id = :id')
        db.session.execute(sql,{"id":id})
        db.session.commit()
    except:
        return False
    return True