from google.cloud.firestore_v1 import Increment
from firebase_admin import firestore
from app.db_controllers.helper import *
from flask import request
import json

firebase_db = firestore.client()

def get_user_document_data(graphics_id):
    try:
        document_ref = firebase_db.collection('users')
        user_data = document_ref.document(graphics_id).get()
        return user_data.to_dict()
    except Exception as e:
        raise e

def firebase_update_profile_image(graphics_id, profile_image_url):
    try:
        document_ref = firebase_db.collection('users')
        update_user = document_ref.document(graphics_id).update({"profile_image": profile_image_url})
    except Exception as e:
        raise e

def firebase_get_questions_for_graphics():
    try:
        document_ref = firebase_db.collection("questions_for_graphics")
        topic_data = document_ref.document("data").get()
        return topic_data.to_dict() or {}
    except Exception as e:
        raise e

def firebase_get_questions_for_graphics_list(grade, chapter, level):
    try:
        document_ref = firebase_db.collection("questions")
        questions_for_graphics = document_ref\
                                .document(f"G{grade:02}")\
                                .collection("levels")\
                                .document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")\
                                .collection("question_bank")\
                                .where("state", "==", "graphics_required")\
                                .stream()
        document_id_list = []
        for question in questions_for_graphics:
            document_id_list.append(question.id)
        return document_id_list
    except Exception as e:
        raise e

def firebase_get_question(question_id, grade, chapter, level):
    try:
        document_ref = firebase_db.collection("questions")
        question_data = document_ref\
                        .document(f"G{grade:02}")\
                        .collection("levels")\
                        .document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")\
                        .collection("question_bank")\
                        .document(question_id)\
                        .get()\
                        .to_dict() or {}
        if not question_data:
            raise ValueError("No such question")
        return question_data
    except Exception as e:
        raise e

def firebase_save_question(graphics_id):
    try:
        data = json.loads(request.form.get('json'))
        question_id = data.get("document_id")
        grade = int(data.get("grade"))
        chapter = int(data.get("chapter"))
        level = int(data.get("level"))
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        question_data = firebase_get_question(question_id, grade, chapter, level)
        user_data = get_user_document_data(graphics_id)
        new_question_data = data.get("question_json")
        if not new_question_data:
            raise ValueError("Question is required!")
        check_data(new_question_data)
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(new_question_data, graphics_id)
        question_image, option_a, option_b, option_c, option_d = get_files_renamed(question_image, option_a, option_b, option_c, option_d)
        get_total_images_uploaded_count = get_total_images_uploaded()
        question_updates = dict(
                                    graphics_by = user_data.get("email"),
                                    options = dict(
                                                    option_a = option_a,
                                                    option_b = option_b,
                                                    option_c = option_c,
                                                    option_d = option_d
                                                ),
                                    question_image = question_image,
                                    state = "approved"
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(graphics_id).set({"total_images_submitted": Increment(get_total_images_uploaded_count)}, merge=True)
        graphics_dict = firebase_db.collection("questions_for_graphics").document("data").get().to_dict()
        graphics_dict[f"NCERT_G{grade:02}_TOPIC{chapter:02}"][f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"] -= 1
        firebase_db.collection("questions_for_graphics").document("data").update(graphics_dict)
        super_admin_questions_for_review_dict = firebase_db.collection("super_admin_questions_for_review").document("data").get().to_dict()
        super_admin_questions_for_review_dict[f"NCERT_G{grade:02}_TOPIC{chapter:02}"][f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"] += 1
        firebase_db.collection("super_admin_questions_for_review").document("data").update(super_admin_questions_for_review_dict)
        firebase_db.collection("cumulative_data").document("data").set({"admin_approved": Increment(1)}, merge=True)
    except Exception as e:
        raise e