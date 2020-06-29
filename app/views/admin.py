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
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('admin_id'))
    leaderboard_data = get_admin_review_stats()
    chart_data = get_cumulative_chart_data()
    active_grade = user_data.get("active_grade")
    return render_template( "/admin/dashboard/dashboard.html",
                            grade_breakdown=grade_breakdown,
                            user_data=user_data,
                            active_grade=active_grade,
                            leaderboard_data=leaderboard_data,
                            chart_data=chart_data
                        )

@admin.route("/editor")
@required_role_as_admin()
def editor():
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('admin_id'))
    active_grade = user_data.get("active_grade")
    return render_template( "/admin/question/editor/editor.html",
                            formula_list=formula_list,
                            grade_breakdown=grade_breakdown,
                            active_grade=active_grade
                        )

@admin.route("/levels")
@required_role_as_admin()
def levels():
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('admin_id'))
    active_grade = user_data.get("active_grade")
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
        questions_for_review = firebase_get_questions_for_review(f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}")
        for level in levels:
            level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level.get('level_number')):02}"
            level["questions_for_review"] = questions_for_review.get(level_id) or 0
        return render_template( "/admin/level/level.html",
                                levels=levels,
                                chapter_name=chapter_dict.get("chapter_name"),
                                grade=grade,
                                chapter=chapter,
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade
                            )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400

@admin.route("/review-question")
@required_role_as_admin()
def review_question():
    user_data = get_user_document_data(session.get('admin_id'))
    active_grade = user_data.get("active_grade")
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
            question_document_ids = firebase_get_questions_for_review_list(grade, chapter, level)
            if len(question_document_ids) == 0:
                return jsonify({
                    "status": "error",
                    "message": "No questions for review!"
                }), 400
            session["question_id_list"] = question_document_ids
        question_document_list = session.get("question_id_list")
        if not question_document_list:
            return redirect(url_for("admin.dashboard"))
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
        return render_template( "/admin/question/review_question/review_question.html",
                                grade=grade,
                                chapter=chapter,
                                level=level,
                                level_name=level_dict.get("level_name"),
                                grade_breakdown=grade_breakdown,
                                next_document_id=next_document_id,
                                document_id=document_id,
                                question_data=question_data,
                                formula_list=formula_list,
                                pdf_url=chapter_dict.get("chapter_pdf"),
                                active_grade=active_grade
                            )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400
