import requests
from firebase_admin import firestore
import json
from app.db_controllers.helper import *
from flask import request

firebase_db = firestore.client()

def get_user_document_data(document_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(document_id).get()
    return user_data.to_dict()

def firebase_update_profile_image(document_id, profile_image_url):
    document_ref = firebase_db.collection('users')
    update_user = document_ref.document(document_id).update({"profile_image": profile_image_url})

def get_leaderboard_data(document_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(document_id).get()
    leaderboard_data_1 = [
                            {
                                "position": 1,
                                "name": user_data.get("name"),
                                "questions": user_data.get("total_questions")
                            }
                        ]
    leaderboard_data_2 = [
                            {
                                "position": 1,
                                "name": user_data.get("name"),
                                "approval_rate": user_data.get("approval_rate"),
                                "questions_reviewed": user_data.get("total_reviewed"),
                                "total_questions": user_data.get("total_questions")
                            }
                        ]
    return leaderboard_data_1, leaderboard_data_2

def get_star_questions():
    document_ref = firebase_db.collection("star_questions")
    star_questions_data = document_ref.order_by("marked_at", direction=firestore.Query.DESCENDING).limit(10).get()
    return [star_question_data.to_dict() for star_question_data in star_questions_data]

def check_preview_question(document_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(document_id).get()
    user_data = user_data.to_dict()
    return user_data.get("preview_question")

def save_preview_question(document_id):
    data = json.loads(request.form.get('json'))
    grade, chapter, level = int(data.get("grade")), int(data.get("chapter")), int(data.get("level"))
    question_image = handle_image_upload('question_image', document_id) or "#"
    option_a = handle_image_upload('option_a', document_id) or data.get('option_a')
    option_b = handle_image_upload('option_b', document_id) or data.get('option_b')
    option_c = handle_image_upload('option_c', document_id) or data.get('option_c')
    option_d = handle_image_upload('option_d', document_id) or data.get('option_d')
    preview_question = dict(
                                grade=grade,
                                chapter=chapter,
                                level=level,
                                question_text=data.get("question_text"),
                                question_image=question_image,
                                options=dict(
                                                option_a=option_a,
                                                option_b=option_b,
                                                option_c=option_c,
                                                option_d=option_d
                                            ),
                                correct_option=data.get("correct_option")
                        )
    save_preview_question = document_ref.document(document_id).update({"preview_question": preview_question})
