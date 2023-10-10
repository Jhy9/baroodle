from db import db
from flask import session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, password, account_type):
    try:
        sql = text('INSERT INTO accounts(username,passw, account_type) VALUES (:username,:password,:account_type)')
        db.session.execute(sql, {"username":username,"password":generate_password_hash(password),"account_type":account_type})
        db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = text('SELECT id, passw, account_type FROM accounts WHERE username=:username')
    query = db.session.execute(sql, {"username":username})
    result = query.fetchone()
    if not result:
        return False
    if check_password_hash(result.passw,password):
        session["username"] = username
        session["uid"] = result.id
        session["account_type"]= result.account_type
        return True
    return False

def logout():
    del session["uid"]
    del session["account_type"]

def get_name():
    return session.get("username")

def get_uid():
    return session.get("uid", False)

def get_account_type():
    return session.get("account_type")

def check_name_availability(username):
    sql = text('SELECT count(*) FROM accounts WHERE username=:username')
    query = db.session.execute(sql, {"username":username}).scalar()
    if query > 0:
        return False
    return True