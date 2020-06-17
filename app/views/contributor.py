from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.contributor_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
from app.data.formula import formula_list

contributor = Blueprint('contributor', __name__, url_prefix="/")

@contributor.route('/')
def login():
    if session.get("contributor_id"):
        return redirect(url_for("contributor.dashboard"))
    elif session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    return render_template("/contributor/login/login.html")

@contributor.route("/dashboard")
@required_role_as_contributor()
def dashboard():
    user_data = get_user_document_data(session.get('contributor_id'))
    active_grade = user_data.get("active_grade")
    chart_data = get_chart_data(session.get('contributor_id'))
    return render_template( "/contributor/dashboard/dashboard.html",
                            grade_breakdown=grade_breakdown,
                            user_data=user_data,
                            chart_data=chart_data,
                            active_grade=active_grade
                        )

@contributor.route("/leaderboard")
@required_role_as_contributor()
def leaderboard():
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

@contributor.route("/notifications")
@required_role_as_contributor()
def notifications():
    notifications = get_notifications(session.get("contributor_id"))
    user_data = get_user_document_data(session.get('contributor_id'))
    active_grade = user_data.get("active_grade")
    return render_template( "/contributor/notifications/notifications.html",
                            notifications=notifications,
                            grade_breakdown=grade_breakdown,
                            active_grade=active_grade
                        )

@contributor.route("/star-questions")
@required_role_as_contributor()
def star_questions():
    star_questions = get_star_questions()
    user_data = get_user_document_data(session.get('contributor_id'))
    active_grade = user_data.get("active_grade")
    return render_template( "/contributor/star_questions/star_questions.html",
                            star_questions=star_questions,
                            grade_breakdown=grade_breakdown,
                            active_grade=active_grade
                        )

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
        preview_question = user_data.get("preview_question")
        if not preview_question:
            grade = request.args.get("grade")
            chapter = request.args.get("chapter")
            level = request.args.get("level")
            grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
            level_id = f"NCERT_G{int(grade):02}_TOPIC{int(chapter):02}_LEVEL{int(level):02}"
            individual_log = user_data.get("individual_log")
            total_contributions_by_contributor = individual_log.get(level_id)
            if total_contributions_by_contributor >= 5:
                return redirect(url_for("contributor.levels", grade=grade, chapter=chapter))
            return render_template( "/contributor/question/create_question/create_question.html",
                                    grade=grade,
                                    chapter=chapter,
                                    level=level,
                                    level_name=level_dict.get("level_name"),
                                    formula_list=formula_list,
                                    pdf_url=chapter_dict.get("chapter_pdf"),
                                    grade_breakdown=grade_breakdown,
                                    preview_question={},
                                    is_preview=False,
                                    total_contributions_by_contributor=total_contributions_by_contributor,
                                    active_grade=active_grade
                                )
        else:
            grade=preview_question.get("grade")
            chapter=preview_question.get("chapter")
            level=preview_question.get("level")
            grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
            return render_template(
                                    "/contributor/question/submit_question/submit_question.html",
                                    grade=grade,
                                    chapter=chapter,
                                    level=level,
                                    level_name=level_dict.get("level_name"),
                                    formula_list=formula_list,
                                    pdf_url=chapter_dict.get("chapter_pdf"),
                                    grade_breakdown=grade_breakdown,
                                    preview_question=preview_question,
                                    is_preview=True,
                                    active_grade=active_grade
                                )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400
