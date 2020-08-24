from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.contributor_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
from app.data.formula import formula_list
from app.db_controllers.logging import *

contributor = Blueprint('contributor', __name__, url_prefix="/")

@contributor.route('/')
def login():
    try:
        if session.get("contributor_id"):
            return redirect(url_for("contributor.dashboard"))
        elif session.get("admin_id"):
            return redirect(url_for("admin.dashboard"))
        elif session.get("graphics_id"):
            return redirect(url_for("graphics.dashboard"))
        elif session.get("super_admin_id"):
            return redirect(url_for("super_admin.dashboard"))
        return render_template("/contributor/login/login.html")
    except Exception as e:
        log_error("view", "contributor", str(e), "login")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@contributor.route("/dashboard")
@required_role_as_contributor()
def dashboard():
    try:
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
        chart_data = get_chart_data(session.get('contributor_id'))
        return render_template( "/contributor/dashboard/dashboard.html",
                                grade_breakdown=grade_breakdown,
                                user_data=user_data,
                                chart_data=chart_data,
                                active_grade=active_grade
                            )
    except Exception as e:
        log_error("view", "contributor", str(e), "dashboard")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@contributor.route("/leaderboard")
@required_role_as_contributor()
def leaderboard():
    try:
        top_contributors_total_question = get_top_contributors_for_total_question()
        top_contributors_approval_rate = get_top_contributors_for_approval_rate()
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
        return render_template( "/contributor/leaderboard/leaderboard.html",
                                top_contributors_total_question=top_contributors_total_question,
                                top_contributors_approval_rate=top_contributors_approval_rate,
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade
                            )
    except Exception as e:
        log_error("view", "contributor", str(e), "leaderboard")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@contributor.route("/notifications")
@required_role_as_contributor()
def notifications():
    try:
        notifications = get_notifications(session.get("contributor_id"))
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
        return render_template( "/contributor/notifications/notifications.html",
                                notifications=notifications,
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade
                            )
    except Exception as e:
        log_error("view", "contributor", str(e), "notifications")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@contributor.route("/star-questions")
@required_role_as_contributor()
def star_questions():
    try:
        star_questions = get_star_questions()
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
        return render_template( "/contributor/star_questions/star_questions.html",
                                star_questions=star_questions,
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade
                            )
    except Exception as e:
        log_error("view", "contributor", str(e), "star_questions")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@contributor.route("/levels")
@required_role_as_contributor()
def levels():
    try:
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
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
        level_question_count = firebase_get_level_count(f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}")
        individual_log = user_data.get("individual_log")
        for level in levels:
            level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level.get('level_number')):02}"
            total_contributions_by_contributor = individual_log.get(level_id)
            level["total_count"] = level_question_count.get(level_id) or 0
            level["total_contributions_by_contributor"] = total_contributions_by_contributor
        return render_template( "/contributor/level/level.html",
                                levels=levels,
                                chapter_name=chapter_dict.get("chapter_name"),
                                grade=grade,
                                chapter=chapter,
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade
                            )
    except ValueError:
        log_error("view", "contributor", str(e), "levels")
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400

@contributor.route("create-question")
@required_role_as_contributor()
def create_question():
    try:
        user_data = get_user_document_data(session.get('contributor_id'))
        active_grade = user_data.get("active_grade")
        grade = request.args.get("grade")
        chapter = request.args.get("chapter")
        level = request.args.get("level")
        grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
        level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level):02}"
        individual_log = user_data.get("individual_log")
        total_contributions_by_contributor = individual_log.get(level_id)
        if total_contributions_by_contributor >= 5:
            return redirect(url_for("contributor.levels", grade=grade, chapter=chapter))
        return render_template(
                                "/contributor/question/submit_question/submit_question.html",
                                grade=grade,
                                chapter=chapter,
                                level=level,
                                level_name=level_dict.get("level_name"),
                                formula_list=formula_list,
                                pdf_url=chapter_dict.get("chapter_pdf"),
                                grade_breakdown=grade_breakdown,
                                active_grade=active_grade,
                                total_contributions_by_contributor=total_contributions_by_contributor
                            )
    except ValueError:
        log_error("view", "contributor", str(e), "create_question")
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400
