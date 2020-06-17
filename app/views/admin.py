from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.admin_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
from app.data.formula import formula_list

admin = Blueprint('admin', __name__, url_prefix="/admin")

@admin.route('/')
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    elif session.get("contributor_id"):
        return redirect(url_for("contributor.dashboard"))
    return render_template("/admin/login/login.html")

@admin.route("/dashboard")
@required_role_as_admin()
def dashboard():
    user_data = get_user_document_data(session.get('admin_id'))
    return render_template( "/admin/dashboard/dashboard.html",
                            grade_breakdown=grade_breakdown,
                            user_data=user_data
                        )

@admin.route("/editor")
@required_role_as_admin()
def editor():
    # grade = int(request.args.get("grade")) if request.args.get("grade") else None
    # chapter = int(request.args.get("chapter")) if request.args.get("chapter") else None
    # level = int(request.args.get("level")) if request.args.get("level") else None
    return render_template( "/admin/question/editor/editor.html",
                            # grade=grade,
                            # chapter=chapter,
                            # level=level,
                            formula_list=formula_list,
                            grade_breakdown=grade_breakdown
                        )

@admin.route("/levels")
@required_role_as_admin()
def levels():
    return "Levels"
