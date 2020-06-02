from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from app.utils.role_util import *
from app.db_controllers.contributor_controller import *
from app.db_controllers.helper import *
from app.data.grade_breakdown import data as grade_breakdown
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
    user_data = get_user_document_data(session.get('document_id'))
    return render_template( "/contributor/dashboard/dashboard.html",
                            grade_breakdown=grade_breakdown,
                            user_data=user_data
                        )

@contributor.route("/leaderboard")
@required_role_as_contributor()
def leaderboard():
    leaderboard_data_1, leaderboard_data_2 = get_leaderboard_data(session.get('document_id'))
    return render_template( "/contributor/leaderboard/leaderboard.html",
                            leaderboard_data_1=leaderboard_data_1,
                            leaderboard_data_2=leaderboard_data_2,
                            grade_breakdown=grade_breakdown
                        )

@contributor.route("/star-questions")
@required_role_as_contributor()
def star_questions():
    star_questions = get_star_questions()
    return render_template( "/contributor/star_questions/star_questions.html",
                            star_questions=star_questions,
                            grade_breakdown=grade_breakdown
                        )

@contributor.route("/levels")
@required_role_as_contributor()
def levels():
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
        return render_template( "/contributor/level/level.html",
                                levels=chapter_dict.get("levels"),
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

@contributor.route("create-question")
@required_role_as_contributor()
def create_question():
    try:
        preview_question = check_preview_question(session.get('document_id'))
        if not preview_question:
            grade = request.args.get("grade")
            chapter = request.args.get("chapter")
            level = request.args.get("level")
            grade_dict, chapter_dict, level_dict = get_grade_breakdown_dict(grade, chapter, level)
            return render_template( "/contributor/question/create_question/create_question.html",
                                    grade=grade,
                                    chapter=chapter,
                                    level=level,
                                    level_name=level_dict.get("level_name"),
                                    formula_list=formula_list,
                                    pdf_url=chapter_dict.get("chapter_pdf"),
                                    grade_breakdown=grade_breakdown,
                                    preview_question={},
                                    is_preview=False
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
                                    is_preview=True
                                )
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Do not tamper with the URL. Go to dashboard and try again!"
        }), 400
