from db import db
from flask import session
from sqlalchemy import text

def check_answer(exercise_id,answer):
    sql = text('SELECT * FROM exercises WHERE id =:id AND answer =:answer')
    query = db.session.execute(sql,{"id":exercise_id, "answer":answer})
    if query is None:
        return False
    return True

def get_submission(exercise_id, user_id):
    sql = text('SELECT answer FROM exercise_submissions WHERE exercise_id =:exercise_id AND user_id=:user_id')
    return db.session.execute(sql,{"exercise_id":exercise_id,"user_id":user_id}).fetchone()

def add_submission(exercise_id, answer,  user_id, points = None):
    try:
        sql = text('INSERT INTO exercise_submissions(exercise_id, user_id,answer,points) VALUES (:eid,:uid,:answer,:points)')
        db.session.execute(sql,{"eid":exercise_id,"uid":user_id,"answer":answer,"points":points})
        db.session.commit()
    except:
        return False
    return True

def modify_submission(exercise_id,answer, user_id):
    try:
        sql = text('UPDATE exercise_submissions SET answer =:answer WHERE exercise_id=:eid AND user_id=:uid')
        db.session.execute(sql,{"eid":exercise_id,"uid":user_id,"answer":answer})
        db.session.commit()
    except:
        return False
    return True
