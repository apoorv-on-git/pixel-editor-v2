from functools import wraps
from flask import abort
from flask_login import current_user

def required_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.user_login_type not in roles:
              abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator
