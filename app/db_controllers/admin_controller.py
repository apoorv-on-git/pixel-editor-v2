import requests
from firebase_admin import firestore
import json
from app.db_controllers.helper import *
from flask import request
import datetime
from google.cloud.firestore_v1 import Increment
import time

firebase_db = firestore.client()

def get_user_document_data(admin_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(admin_id).get()
    return user_data.to_dict()

def firebase_submit_question(admin_id):
    try:
        data = json.loads(request.form.get('json'))
        user_data = get_user_document_data(admin_id)
        check_data(data)
        grade, chapter, level = int(data.get("grade")) if data.get("grade") else None, int(data.get("chapter")) if data.get("chapter") else None, int(data.get("level")) if data.get("level") else None
        if not all((grade, chapter, level)):
            raise ValueError("Grade, Chapter and Level are mandatory!")
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(data, admin_id)
        question_image, option_a, option_b, option_c, option_d = get_files_renamed(question_image, option_a, option_b, option_c, option_d)
        question_text = remove_style(data.get("question"))
        question = dict(
                            board_type = "NCERT",
                            grade = grade,
                            chapter = chapter,
                            level = level,
                            admin_id = admin_id,
                            admin_name = user_data.get("name"),
                            is_star_question = False,
                            state = "under_review",
                            date_created = datetime.datetime.utcnow(),
                            date_approved = None,
                            question_text = question_text,
                            question_image = question_image,
                            options = dict(
                                                option_a = option_a,
                                                option_b = option_b,
                                                option_c = option_c,
                                                option_d = option_d
                                        ),
                            correct_option = data.get("correct_option"),
                            question_type = "MCQ",
                            feedback = None,
                            approved_by = None,
                            deployed_by = None
                    )
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        level_collection_id = f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"
        document_ref = firebase_db.collection("users")
        question_document_ref = firebase_db.collection("questions")
        question_document_ref.document(f"G{grade:02}").collection("levels").document(level_collection_id).collection("question_bank").document().create(question)
        document_ref.document(admin_id).set({"total_questions": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("total_questions").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({level_collection_id: Increment(1)}, merge=True)
    except Exception as e:
        raise e
