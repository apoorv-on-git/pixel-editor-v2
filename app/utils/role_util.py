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

def required_role_as_admin():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("user_type") or session.get("user_type").lower() != "admin":
              abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def required_role_as_graphics():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("user_type") or session.get("user_type").lower() != "graphics":
              abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def required_role_as_super_admin():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("user_type") or session.get("user_type").lower() != "super admin":
              abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator
