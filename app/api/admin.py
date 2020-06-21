from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *
from app.db_controllers.admin_controller import *
from app.utils.s3 import *
from app.db_controllers.helper import *
import json

admin_api = Blueprint('admin_api', __name__, url_prefix="/admin-api")

@admin_api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not all((email, password)):
        return jsonify({
                'status': 'error',
                'message': 'Both email and password are required!'
        }), 400
    response = login_firebase_user(email, password)
    if response.get("success") and response.get("type").lower() == "admin":
        session["admin_id"] = response.get("document_id")
        session["email"] = response.get("email")
        session["user_type"] = response.get("type")
        return jsonify({
            "status": "success",
        }), 200
    elif response.get("success"):
        return jsonify({
            "status": "error",
            "message": "This login is only for admins!"
        }), 400
    else:
        return jsonify({
            "status": "error",
            "message": response.get("error")
        }), 400

@admin_api.route("/logout", methods=["POST"])
@required_role_as_admin()
def logout():
    session["admin_id"] = None
    session["email"] = None
    session["user_type"] = None
    return jsonify(
        {
            "status": "success",
        }, 200
    )

@admin_api.route("/get-chapter-list")
@required_role_as_admin()
def get_chapter_list():
    try:
        grade = int(request.args.get("grade")) if request.args.get("grade") else None
        if not grade:
            return jsonify({
                "data": [],
                "status": "success"
            }), 200
        grade_dict = next((grade_dict for grade_dict in grade_breakdown if grade_dict.get('grade_number') == int(grade)), None)
        chapter_list = [chapter_dict.get("chapter_number") for chapter_dict in grade_dict.get("chapters")]
        return jsonify({
            "data": chapter_list,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@admin_api.route("/get-level-list")
@required_role_as_admin()
def get_level_list():
    try:
        grade = int(request.args.get("grade")) if request.args.get("grade") else None
        chapter = int(request.args.get("chapter")) if request.args.get("chapter") else None
        if not chapter or not grade:
            return jsonify({
                "data": [],
                "status": "success"
            }), 200
        grade_dict = next((grade_dict for grade_dict in grade_breakdown if grade_dict.get('grade_number') == int(grade)), None)
        chapter_dict = next((chapter_dict for chapter_dict in grade_dict.get("chapters") if chapter_dict.get('chapter_number') == int(chapter)), None)
        level_list = [level_dict.get("level_number") for level_dict in chapter_dict.get("levels")]
        return jsonify({
            "data": level_list,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@admin_api.route("/submit-question", methods=["POST"])
@required_role_as_admin()
def submit_question():
    try:
        firebase_submit_question(session.get('admin_id'))
        return jsonify({
            "message": "Saved successfully!",
            "status": "success"
        }), 204
    except ValueError as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@admin_api.route("/disapprove-question", methods=["POST"])
@required_role_as_admin()
def disapprove_question():
    try:
        firebase_disapprove_question(session.get('admin_id'))
        return jsonify({
            "message": "Question disapproved successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@admin_api.route("/approve-question", methods=["POST"])
@required_role_as_admin()
def approve_question():
    try:
        firebase_approve_question(session.get('admin_id'))
        return jsonify({
            "message": "Question approved successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400
