from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.graphics_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
from app.data.formula import formula_list
from app.db_controllers.logging import *

graphics = Blueprint('graphics', __name__, url_prefix="/graphics")

@graphics.route('/')
def login():
    try:
        if session.get("graphics_id"):
            return redirect(url_for("graphics.dashboard"))
        elif session.get("admin_id"):
            return redirect(url_for("admin.dashboard"))
        elif session.get("contributor_id"):
            return redirect(url_for("contributor.dashboard"))
        elif session.get("super_admin_id"):
            return redirect(url_for("super_admin.dashboard"))
        return render_template("/graphics/login/login.html")
    except Exception as e:
        log_error("view", "graphics", str(e), "login")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@graphics.route("/dashboard")
@required_role_as_graphics()
def dashboard():
    try:
        session["question_id_list"] = None
        user_data = get_user_document_data(session.get('graphics_id'))
        sidebar_filter_based_on_requirement = firebase_get_questions_for_graphics()
        return render_template( "/graphics/dashboard/dashboard.html",
                                grade_breakdown=grade_breakdown,
                                user_data=user_data,
                                sidebar_filter_based_on_requirement=sidebar_filter_based_on_requirement
                            )
    except Exception as e:
        log_error("view", "graphics", str(e), "dashboard")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@graphics.route("/levels")
@required_role_as_graphics()
def levels():
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('graphics_id'))
    try:
        grade = request.args.get("grade")
        grade_dict = next((grade_dict for grade_dict in grade_breakdown if grade_dict.get('grade_number') == int(grade)), None)
        if not grade_dict:
            return jsonify({
                "status": "error",
                "message": "Invalid Grade!"
            }), 400
        chapter = request.args.get("chapter")
        chapter_dict = next((chapter_dict for chapter_dict in grade_dict.get("chapters") if chapter_dict.get('chapter_number') == int(chapter)), None)
        if not chapter_dict:
            return jsonify({
                "status": "error",
                "message": "Invalid Chapter!"
            }), 400
        levels = chapter_dict.get("levels")
        sidebar_filter_based_on_requirement = firebase_get_questions_for_graphics()
        questions_for_graphics = sidebar_filter_based_on_requirement.get(f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}")
        for level in levels:
            level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level.get('level_number')):02}"
            level["questions_for_graphics"] = questions_for_graphics.get(level_id) or 0
        return render_template( "/graphics/level/level.html",
                                levels=levels,
                                chapter_name=chapter_dict.get("chapter_name"),
                                grade=grade,
                                chapter=chapter,
                                grade_breakdown=grade_breakdown,
                                sidebar_filter_based_on_requirement=sidebar_filter_based_on_requirement
                            )
    except ValueError as e:
        log_error("view", "graphics", str(e), "levels")
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400

@graphics.route("edit-question")
@required_role_as_graphics()
def edit_question():
    user_data = get_user_document_data(session.get('graphics_id'))
    sidebar_filter_based_on_requirement = firebase_get_questions_for_graphics()
    try:
        grade = int(request.args.get("grade"))
        chapter = int(request.args.get("chapter"))
        level = int(request.args.get("level"))
        document_id = request.args.get("document_id")
        if not all((grade, chapter, level)):
            return jsonify({
                "status": "error",
                "message": "Do not tamper with the URL. Go to dashboard and try again!"
            })
        if not document_id:
            question_document_ids = firebase_get_questions_for_graphics_list(grade, chapter, level)
            if len(question_document_ids) == 0:
                return jsonify({
                    "status": "error",
                    "message": "No questions for graphics!"
                }), 400
            session["question_id_list"] = question_document_ids
        question_document_list = session.get("question_id_list")
        if not question_document_list:
            return redirect(url_for("graphics.dashboard"))
        elif len(question_document_list) == 0:
            return jsonify({
                "status": "error",
                "message": "No questions for review!"
            }), 400
        if not document_id:
            document_id = question_document_list[0]
        try:
            next_document_id = question_document_list[question_document_list.index(document_id) + 1]
        except IndexError:
            next_document_id = ""
        question_data = firebase_get_question(document_id, grade, chapter, level)
        grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
        return render_template( "/graphics/question/edit_question.html",
                                grade=grade,
                                chapter=chapter,
                                level=level,
                                level_name=level_dict.get("level_name"),
                                grade_breakdown=grade_breakdown,
                                next_document_id=next_document_id,
                                document_id=document_id,
                                question_data=question_data,
                                sidebar_filter_based_on_requirement=sidebar_filter_based_on_requirement
                            )
    except ValueError as e:
        log_error("view", "graphics", str(e), "edit_question")
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400