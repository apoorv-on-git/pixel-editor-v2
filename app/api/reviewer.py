from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *
from app.db_controllers.reviewer_controller import *
from app.utils.s3 import *
from app.db_controllers.helper import *
from app.db_controllers.logging import *
import json

reviewer_api = Blueprint('reviewer_api', __name__, url_prefix="/reviewer-api")

@reviewer_api.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        if not all((email, password)):
            return jsonify({
                    'status': 'error',
                    'message': 'Both email and password are required!'
            }), 400
        response = login_firebase_user(email, password)
        if response.get("success") and response.get("type").lower() == "reviewer":
            session["reviewer_id"] = response.get("document_id")
            session["email"] = response.get("email")
            session["user_type"] = response.get("type")
            return jsonify({
                "status": "success",
                "document_id": response.get("document_id")
            }), 200
        elif response.get("success"):
            return jsonify({
                "status": "error",
                "message": "This login is only for reviewers!"
            }), 400
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error")
            }), 400
    except Exception as e:
        log_error("api", "reviewer", str(e), "login")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@reviewer_api.route("/logout", methods=["POST"])
def logout():
    try:
        session["reviewer_id"] = None
        session["email"] = None
        session["user_type"] = None
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        log_error("api", "reviewer", str(e), "logout")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@reviewer_api.route("/get-question-list")
def get_question_list():
    try:
        document_id = request.args.get("reviewer_id")
        question_id_list = firebase_get_reviewer_question_list(document_id)
        if len(question_id_list) == 0:
            question_id_list = firebase_assign_questions_to_reviewer(document_id)
            if not question_id_list:
                return jsonify({
                    "message": "No questions to assign",
                    "status": "error"
                }), 400
        return jsonify({
            "data": question_id_list,
            "status": "success"
        }), 200
    except Exception as e:
        log_error("api", "reviewer", str(e), "get_question_list")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@reviewer_api.route("/get-question")
def get_question():
    try:
        question_id = request.args.get("question_id")
        question_meta_data = firebase_get_question_meta_data(question_id)
        question_data = firebase_get_question(question_meta_data.get("question_doc_id"))
        return jsonify({
            "data": question_data,
            "status": "success"
        }), 200
    except Exception as e:
        log_error("api", "reviewer", str(e), "get_question")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@reviewer_api.route("/mark-question-good", methods=["POST"])
def mark_question_good():
    try:
        question_id = request.json.get("question_id")
        reviewer_id = request.json.get("reviewer_id")
        firebase_mark_question_good(question_id, reviewer_id)
        return jsonify({
            "status": "success"
        }), 200
    except Exception as e:
        log_error("api", "reviewer", str(e), "mark_question_good")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@reviewer_api.route("/mark-question-bad", methods=["POST"])
def mark_question_bad():
    try:
        question_id = request.json.get("question_id")
        reviewer_id = request.json.get("reviewer_id")
        bad_type = request.json.get("bad_type")
        feedback = request.json.get("feedback")
        firebase_mark_question_bad(question_id, reviewer_id, bad_type, feedback)
        return jsonify({
            "status": "success"
        }), 200
    except Exception as e:
        log_error("api", "reviewer", str(e), "mark_question_bad")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400
