from db import db
from flask import session
from sqlalchemy import text

def get_sets(course_id):
    sql = text('SELECT id, set_name, availability_status FROM exercise_set WHERE course_id =:cid ORDER BY id ASC')
    return db.session.execute(sql,{"cid":course_id}).fetchall()

def create_set(course_id, name):
    try:
        sql = text('INSERT INTO exercise_set(course_id, set_name, availability_status) VALUES (:course_id, :name, :status)')
        db.session.execute(sql,{"course_id":course_id, "name":name, "status":"hidden"})
        db.session.commit()
    except:
        return False
    return True

def modify_set_availability(set_id, status):
    try:
        sql = text('UPDATE exercise_set SET availability_status =:status WHERE id =:id')
        db.session.execute(sql,{"id":set_id,"status":status})
        db.session.commit()
    except:
        return False
    return True

def add_exercise(set_id,description, max_points):
    try:
        sql = text('INSERT INTO exercises(set_id, assignment, max_points, exercise_type) VALUES (:set_id, :description,:max_points,:exercise_type)')
        db.session.execute(sql,{"set_id":set_id, "description":description,"max_points":max_points,"exercise_type":2})
        db.session.commit()
    except:
        return False
    return True

def add_exercise_multi(set_id,description, max_points,option1,option2,option3,answer):
    try:
        sql = text('INSERT INTO exercises(set_id, assignment, max_points, exercise_type,answer,option1,option2,option3) VALUES (:set_id, :description,:max_points,:exercise_type,:answer,:option1,:option2,:option3)')
        db.session.execute(sql,{"set_id":set_id, "description":description,"max_points":max_points,"exercise_type":1, "answer":answer,"option1":option1,"option2":option2,"option3":option3})
        db.session.commit()
    except:
        return False
    return True

def get_set(set_id, user_id):
    sql = text('SELECT ex.id,ex.assignment, ex.exercise_type,ex.option1,ex.option2,ex.option3, submission.answer FROM exercise_set JOIN exercises as ex ON exercise_set.id = ex.set_id '
               'LEFT JOIN exercise_submissions as submission ON submission.exercise_id = ex.id '
               'WHERE exercise_set.id =:set_id AND (submission.user_id =:user_id OR submission.user_id IS NULL)')
    return db.session.execute(sql,{"set_id":set_id, "user_id":user_id}).fetchall()

def get_max_points(exercise_id):
    sql = text('SELECT max_points FROM exercises WHERE id =:id')
    return db.session.execute(sql,{"id":exercise_id}).scalar()