from db import db
from flask import session
from sqlalchemy import text

def get_submissions(set_id):
    sql= text('SELECT ex.assignment, sub.user_id, sub.answer,ex.max_points, ex.id '
              'FROM exercises as ex JOIN exercise_submissions as sub on ex.id = sub.exercise_id '
              'WHERE ex.exercise_type = 2 AND sub.points IS NULL AND ex.set_id =:set_id')
    return db.session.execute(sql,{"set_id":set_id}).fetchall()

def add_review(ex_id, user_id, points, comment= None):
    try:
        sql= text('UPDATE exercise_submissions SET points =:points, feedback =:feedback WHERE user_id=:user_id AND exercise_id=:ex_id')
        db.session.execute(sql,{"user_id":user_id,"ex_id":ex_id,"points":points,"feedback":comment})
        db.session.commit()
    except:
        return False
    return True


