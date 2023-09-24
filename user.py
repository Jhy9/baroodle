from db import db
from flask import session
def register(username, password, account_type):
    try:
        sql = "INSERT INTO accounts(username,password, account_type) VALUES (:username,:password,:account_type)"
        db.session.execute(sql, {"username":username,"password":password,"account_type":account_type})
        db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = "SELECT id, password FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    if not result:
        return False
    else:
        if result.password ==password:
            return result.id
        else:
            return False
        