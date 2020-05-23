from flask import Blueprint, render_template, session, redirect, url_for
from app.utils.role_util import *
from app.db_controllers.contributor_controller import *

contributor = Blueprint('contributor', __name__, url_prefix="/")

@contributor.route('/')
def login():
    if session.get("document_id"):
        return redirect(url_for("contributor.dashboard"))
    return render_template("/contributor/login/login.html")

@contributor.route("/dashboard")
@required_role_as_contributor()
def dashboard():
    return "<h1>Dashboard</h1>"
