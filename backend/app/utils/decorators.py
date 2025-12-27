from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort
from app.utils.db import get_db

def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            db = get_db()
            user_id = get_jwt_identity()
            user = db.table("users").select("role").eq("id", user_id).execute().data

            if not user or user[0]["role"] != required_role:
                abort(403)

            return fn(*args, **kwargs)
        return decorator
    return wrapper
