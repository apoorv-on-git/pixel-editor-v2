from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.contributor_controller import *
from app.data.level_breakdown import data
from app.data.formula import formula_list

contributor = Blueprint('contributor', __name__, url_prefix="/")

@contributor.route('/')
def login():
    if session.get("document_id"):
        return redirect(url_for("contributor.dashboard"))
    return render_template("/contributor/login/login.html")

@contributor.route("/dashboard")
@required_role_as_contributor()
def dashboard():
    return render_template("/contributor/dashboard/dashboard.html")

@contributor.route("/levels")
@required_role_as_contributor()
def levels():
    grade = request.args.get("grade")
    grade_dict = data.get(f"grade_{grade}")
    if not grade_dict:
        return jsonify({
            "status": "error",
            "message": "Invalid Grade!"
        }), 400
    chapter = request.args.get("chapter")
    chapter_dict = grade_dict.get(f"chapter_{chapter}")
    if not chapter_dict:
        return jsonify({
            "status": "error",
            "message": "Invalid Chapter!"
        }), 400
    return render_template("/contributor/level/level.html", levels=chapter_dict, grade=grade, chapter=chapter)

@contributor.route("create-question")
@required_role_as_contributor()
def create_question():
    grade = request.args.get("grade")
    chapter = request.args.get("chapter")
    level = request.args.get("level")
    level_name = data.get(f"grade_{grade}").get(f"chapter_{chapter}").get(f"level_{level}")
    return render_template("/contributor/create_question/create_question.html", grade=grade, chapter=chapter, level=level, level_name=level_name, formula_list=formula_list)
