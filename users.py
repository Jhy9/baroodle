from db import db
from flask import session
from sqlalchemy import text
def register(username, password, account_type):
    try:
        sql = text('INSERT INTO accounts(username,passw, account_type) VALUES (:username,:password,:account_type)')
        db.session.execute(sql, {"username":username,"password":password,"account_type":account_type})
        db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = text('SELECT id, passw FROM accounts WHERE username=:username')
    query = db.session.execute(sql, {"username":username})
    result = query.fetchone()
    if not result:
        return False
    else:
        if result.passw ==password:
            return result.id
        else:
            return False
        