from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *
from app.db_controllers.contributor_controller import *
from app.utils.s3 import *
from app.db_controllers.helper import *
from app.db_controllers.logging import *
import json

contributor_api = Blueprint('contributor_api', __name__, url_prefix="/contributor-api")

@contributor_api.route('/login', methods=['POST'])
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
        if response.get("success") and response.get("type").lower() == "contributor":
            session["contributor_id"] = response.get("document_id")
            session["email"] = response.get("email")
            session["user_type"] = response.get("type")
            return jsonify({
                "status": "success",
            }), 200
        elif response.get("success"):
            return jsonify({
                "status": "error",
                "message": "This login is only for contributors!"
            }), 400
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error")
            }), 400
    except Exception as e:
        log_error("api", "contributor", str(e), "login")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@contributor_api.route("/logout", methods=["POST"])
@required_role_as_contributor()
def logout():
    try:
        session["contributor_id"] = None
        session["email"] = None
        session["user_type"] = None
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        log_error("api", "contributor", str(e), "logout")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@contributor_api.route("/upload-profile-image", methods=["POST"])
@required_role_as_contributor()
def update_profile_image():
    try:
        profile_image = request.files.get('profile_image')
        if profile_image:
            url_endpoint = f"profile_images/{session.get('contributor_id')}.{profile_image.filename.split('.')[-1]}"
            delete_from_s3(url_endpoint)
            upload_to_s3(url_endpoint, profile_image)
            firebase_update_profile_image(session.get('contributor_id'), f"{os.environ.get('S3_URL')}{url_endpoint}")
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        log_error("api", "contributor", str(e), "update_profile_image")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@contributor_api.route("/submit-question", methods=["POST"])
@required_role_as_contributor()
def submit_question():
    try:
        firebase_submit_question(session.get('contributor_id'))
        return jsonify({
            "message": "Saved successfully!",
            "status": "success"
        }), 204
    except ValueError as e:
        log_error("api", "contributor", str(e), "submit_question")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400
