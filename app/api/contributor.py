from flask import Blueprint, jsonify, request, session
from app.utils.role_util import *
from app.db_controllers.auth_controller import *

contributor_api = Blueprint('contributor_api', __name__, url_prefix="/contributor-api")

@contributor_api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not all((email, password)):
        return jsonify({
                'status': 'error',
                'message': 'Both email and password are required!'
        }), 400
    response = login_firebase_user(email, password)
    if response.get("success") and response.get("type").lower() == "contributor":
        session["document_id"] = response.get("document_id")
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

@contributor_api.route("/logout", methods=["POST"])
@required_role_as_contributor()
def logout():
    session["document_id"] = None
    session["email"] = None
    session["user_type"] = None
    return jsonify(
        {
            "status": "success",
        }, 200
    )
