from flask import Blueprint, jsonify, request, session
# from flask_login import login_required, login_user, current_user, logout_user
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
    response = login_user(email, password)
    # admin = Admin.query.filter_by(email=email).first()
    # if admin and password==admin.password:
    #     login_user(admin)
    #     session['user_login_type']='admin'
    #     return jsonify({
    #             'status': 'success',
    #     }), 200
    # elif not admin:
    #     return jsonify({
    #             'status': 'error',
    #             'message': 'User does not exist',
    #     }), 404
    # else:
    #     return jsonify({
    #             'status': 'error',
    #             'message': 'Wrong credentials.',
    #     }), 400
