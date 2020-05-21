from flask import Blueprint, render_template
# from app.utils.role_util import required_role

contributor = Blueprint('contributor', __name__, url_prefix="/")

@contributor.route('/')
def login():
    return render_template("/contributor/login/login.html")
