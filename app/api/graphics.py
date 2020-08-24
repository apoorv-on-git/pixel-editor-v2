from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *
from app.db_controllers.graphics_controller import *
from app.utils.s3 import *
from app.db_controllers.helper import *
from app.db_controllers.logging import *
import json

graphics_api = Blueprint('graphics_api', __name__, url_prefix="/graphics-api")

@graphics_api.route('/login', methods=['POST'])
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
        if response.get("success") and response.get("type").lower() == "graphics":
            session["graphics_id"] = response.get("document_id")
            session["email"] = response.get("email")
            session["user_type"] = response.get("type")
            return jsonify({
                "status": "success",
            }), 200
        elif response.get("success"):
            return jsonify({
                "status": "error",
                "message": "This login is only for graphics!"
            }), 400
        else:
            return jsonify({
                "status": "error",
                "message": response.get("error")
            }), 400
    except Exception as e:
        log_error("api", "graphics", str(e), "login")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@graphics_api.route("/logout", methods=["POST"])
@required_role_as_graphics()
def logout():
    try:
        session["graphics_id"] = None
        session["email"] = None
        session["user_type"] = None
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        log_error("api", "graphics", str(e), "logout")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@graphics_api.route("/upload-profile-image", methods=["POST"])
@required_role_as_graphics()
def update_profile_image():
    try:
        profile_image = request.files.get('profile_image')
        if profile_image:
            url_endpoint = f"profile_images/{session.get('graphics_id')}.{profile_image.filename.split('.')[-1]}"
            delete_from_s3(url_endpoint)
            upload_to_s3(url_endpoint, profile_image)
            firebase_update_profile_image(session.get('graphics_id'), f"{os.environ.get('S3_URL')}{url_endpoint}")
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        log_error("api", "graphics", str(e), "update_profile_image")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@graphics_api.route("/save-question", methods=["POST"])
@required_role_as_graphics()
def save_question():
    try:
        firebase_save_question(session.get('graphics_id'))
        return jsonify({
            "message": "Question edited successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        log_error("api", "graphics", str(e), "save_question")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400