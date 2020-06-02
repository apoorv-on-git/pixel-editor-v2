import requests
from firebase_admin import firestore
import json
from app.db_controllers.helper import *
from flask import request
import datetime
from google.cloud.firestore_v1 import Increment

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

def firebase_save_preview_question(document_id):
    try:
        data = json.loads(request.form.get('json'))
        grade, chapter, level = int(data.get("grade")), int(data.get("chapter")), int(data.get("level"))
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(data, document_id)
        preview_question = dict(
                                    grade=grade,
                                    chapter=chapter,
                                    level=level,
                                    question_text=data.get("question"),
                                    question_image=question_image,
                                    options=dict(
                                                    option_a=option_a,
                                                    option_b=option_b,
                                                    option_c=option_c,
                                                    option_d=option_d
                                                ),
                                    correct_option=data.get("correct_option")
                            )
        document_ref = firebase_db.collection('users')
        save_preview_question = document_ref.document(document_id).update({"preview_question": preview_question})
    except Exception as e:
        raise e

def firebase_submit_question(document_id):
    try:
        data = json.loads(request.form.get('json'))
        grade, chapter, level = int(data.get("grade")), int(data.get("chapter")), int(data.get("level"))
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(data, document_id)
        question_image, option_a, option_b, option_c, option_d = get_files_renamed(question_image, option_a, option_b, option_c, option_d)
        question = dict(
                            board_type = "NCERT",
                            contributor_id = document_id,
                            state = "under_review",
                            date_created = datetime.datetime.utcnow(),
                            date_approved = "",
                            question_text = data.get("question"),
                            question_image = question_image,
                            options = dict(
                                                option_a = option_a,
                                                option_b = option_b,
                                                option_c = option_c,
                                                option_d = option_d
                                        ),
                            correct_option = data.get("correct_option"),
                            question_type = "MCQ",
                            feedback = "",
                            approved_by = "",
                            deployed_by = ""
                    )
        level_collection_id = f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"
        document_ref = firebase_db.collection("users")
        document_ref.document(document_id).update({"preview_question": firestore.DELETE_FIELD})
        document_ref.document(document_id).collection("levels").document(level_collection_id).collection("question_bank").document().create(question)
        document_ref.document(document_id).update({"total_questions": Increment(1)})
    except Exception as e:
        raise e
