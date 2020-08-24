from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *
from app.db_controllers.super_admin_controller import *
from app.utils.s3 import *
from app.db_controllers.helper import *
import json

super_admin_api = Blueprint('super_admin_api', __name__, url_prefix="/super-admin-api")

@super_admin_api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not all((email, password)):
        return jsonify({
                'status': 'error',
                'message': 'Both email and password are required!'
        }), 400
    response = login_firebase_user(email, password)
    if response.get("success") and response.get("type").lower() == "super admin":
        session["super_admin_id"] = response.get("document_id")
        session["email"] = response.get("email")
        session["user_type"] = response.get("type")
        return jsonify({
            "status": "success",
        }), 200
    elif response.get("success"):
        return jsonify({
            "status": "error",
            "message": "This login is only for super admins!"
        }), 400
    else:
        return jsonify({
            "status": "error",
            "message": response.get("error")
        }), 400

@super_admin_api.route("/logout", methods=["POST"])
@required_role_as_super_admin()
def logout():
    session["super_admin_id"] = None
    session["email"] = None
    session["user_type"] = None
    return jsonify(
        {
            "status": "success",
        }, 200
    )

@super_admin_api.route("/upload-profile-image", methods=["POST"])
@required_role_as_super_admin()
def update_profile_image():
    try:
        profile_image = request.files.get('profile_image')
        if profile_image:
            url_endpoint = f"profile_images/{session.get('super_admin_id')}.{profile_image.filename.split('.')[-1]}"
            delete_from_s3(url_endpoint)
            upload_to_s3(url_endpoint, profile_image)
            firebase_update_profile_image(session.get('super_admin_id'), f"{os.environ.get('S3_URL')}{url_endpoint}")
        return jsonify(
            {
                "status": "success",
            }, 200
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@super_admin_api.route("/disapprove-quality", methods=["POST"])
@required_role_as_super_admin()
def disapprove_quality():
    try:
        firebase_disapprove_quality(session.get('super_admin_id'))
        return jsonify({
            "message": "Question disapproved successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@super_admin_api.route("/disapprove-graphics", methods=["POST"])
@required_role_as_super_admin()
def disapprove_graphics():
    try:
        firebase_disapprove_graphics(session.get('super_admin_id'))
        return jsonify({
            "message": "Question disapproved successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@super_admin_api.route("/star-question", methods=["POST"])
@required_role_as_super_admin()
def star_question():
    try:
        firebase_star_question(session.get('super_admin_id'))
        return jsonify({
            "message": "Question marked as star successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@super_admin_api.route("/deploy-question", methods=["POST"])
@required_role_as_super_admin()
def deploy_question():
    try:
        firebase_deploy_question(session.get('super_admin_id'))
        return jsonify({
            "message": "Question marked as deployed successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@super_admin_api.route("/discard-question", methods=["POST"])
@required_role_as_super_admin()
def discard_question():
    try:
        firebase_discard_question(session.get('super_admin_id'))
        return jsonify({
            "message": "Question discarded!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400

@super_admin_api.route("/delete-image", methods=["POST"])
@required_role_as_super_admin()
def delete_image():
    try:
        firebase_delete_image(session.get('super_admin_id'))
        return jsonify({
            "message": "Image deleted successfully!",
            "status": "success"
        }), 204
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 400