from functools import wraps
from flask import abort, session

def required_role_as_contributor():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("user_type") or session.get("user_type").lower() != "contributor":
              abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator
