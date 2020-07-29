from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.super_admin_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
from app.data.formula import formula_list

super_admin = Blueprint('super_admin', __name__, url_prefix="/super-admin")

@super_admin.route('/')
def login():
    if session.get("super_admin_id"):
        return redirect(url_for("super_admin.dashboard"))
    elif session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    elif session.get("contributor_id"):
        return redirect(url_for("contributor.dashboard"))
    elif session.get("graphics_id"):
        return redirect(url_for("graphics.dashboard"))
    return render_template("/super_admin/login/login.html")

@super_admin.route("/dashboard")
@required_role_as_super_admin()
def dashboard():
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('super_admin_id'))
    leaderboard_data = get_admin_review_stats()
    chart_data = get_cumulative_chart_data()
    return render_template( "/super_admin/dashboard/dashboard.html",
                            grade_breakdown=grade_breakdown,
                            user_data=user_data,
                            leaderboard_data=leaderboard_data,
                            chart_data=chart_data
                        )

@super_admin.route("/levels")
@required_role_as_super_admin()
def levels():
    session["question_id_list"] = None
    user_data = get_user_document_data(session.get('super_admin_id'))
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
        questions_for_super_admin = firebase_get_approved_question_count(f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}")
        for level in levels:
            level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level.get('level_number')):02}"
            level["questions_for_super_admin"] = questions_for_super_admin.get(level_id) or 0
        return render_template( "/super_admin/level/level.html",
                                levels=levels,
                                chapter_name=chapter_dict.get("chapter_name"),
                                grade=grade,
                                chapter=chapter,
                                grade_breakdown=grade_breakdown
                            )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400

@super_admin.route("/review-question")
@required_role_as_super_admin()
def review_question():
    user_data = get_user_document_data(session.get('super_admin_id'))
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
            question_document_ids = firebase_get_questions_for_super_admin_list(grade, chapter, level)
            if len(question_document_ids) == 0:
                return jsonify({
                    "status": "error",
                    "message": "No questions for super admin!"
                }), 400
            session["question_id_list"] = question_document_ids
        question_document_list = session.get("question_id_list")
        if not question_document_list:
            return redirect(url_for("super_admin.dashboard"))
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
        admin_name = question_data.get("approved_by")
        grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
        return render_template( "/super_admin/question/review_question.html",
                                grade=grade,
                                chapter=chapter,
                                level=level,
                                level_name=level_dict.get("level_name"),
                                grade_breakdown=grade_breakdown,
                                next_document_id=next_document_id,
                                document_id=document_id,
                                question_data=question_data,
                                pdf_url=chapter_dict.get("chapter_pdf"),
                                admin_name=admin_name
                            )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400