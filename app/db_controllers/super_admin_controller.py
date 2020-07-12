from google.cloud.firestore_v1 import Increment
from firebase_admin import firestore
from app.db_controllers.helper import *
from flask import request
import datetime
import json

firebase_db = firestore.client()

def get_user_document_data(super_admin_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(super_admin_id).get()
    return user_data.to_dict()

def firebase_update_profile_image(super_admin_id, profile_image_url):
    document_ref = firebase_db.collection('users')
    update_user = document_ref.document(super_admin_id).update({"profile_image": profile_image_url})

def firebase_get_approved_question_count(topic_id):
    document_ref = firebase_db.collection("super_admin_questions_for_review")
    topic_data = document_ref.document(topic_id).get()
    return topic_data.to_dict() or {}

def firebase_get_questions_for_super_admin_list(grade, chapter, level):
    document_ref = firebase_db.collection("questions")
    questions_for_super_admin = document_ref\
                            .document(f"G{grade:02}")\
                            .collection("levels")\
                            .document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")\
                            .collection("question_bank")\
                            .where("state", "==", "approved")\
                            .where("is_deployed", "==", False)\
                            .stream()
    document_id_list = []
    for question in questions_for_super_admin:
        document_id_list.append(question.id)
    return document_id_list

def firebase_get_question(question_id, grade, chapter, level):
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

def firebase_disapprove_quality(super_admin_id):
    try:
        feedback = request.json.get("feedback")
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if not feedback:
            raise ValueError("Feedback is important!")
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        question_updates = dict(
                                    state="under_review",
                                    super_admin_feedback = feedback
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"reviewed": Increment(-1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_disapprove_graphics(super_admin_id):
    try:
        feedback = request.json.get("feedback")
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if not feedback:
            raise ValueError("Feedback is important!")
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        question_updates = dict(
                                    state="graphics_required",
                                    super_admin_feedback = feedback
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        graphics_dict = firebase_db.collection("questions_for_graphics").document("data").get().to_dict()
        graphics_dict[f"NCERT_G{grade:02}_TOPIC{chapter:02}"][f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"] += 1
        firebase_db.collection("questions_for_graphics").document("data").update(graphics_dict)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_star_question(super_admin_id):
    try:
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        question_data = firebase_get_question(question_id, grade, chapter, level)
        contributor_id = question_data.get("contributor_id")
        if not contributor_id:
            raise ValueError("Contributor not identified!")
        contributor_data = get_user_document_data(contributor_id)
        question_updates = dict(
                                    is_star_question = True
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(contributor_id).set({"total_star_questions": Increment(1)}, merge=True)
        star_question_log = dict(
                                    contributed_by = contributor_id,
                                    contributor_name = contributor_data.get("name"),
                                    correct_option = question_data.get("correct_option"),
                                    marked_at = datetime.datetime.utcnow(),
                                    options = question_data.get("options"),
                                    question_image = question_data.get("question_image"),
                                    question_text = question_data.get("question_text")
                                )
        firebase_db.collection("star_questions").document().create(star_question_log)
    except Exception as e:
        raise e

def firebase_deploy_question(super_admin_id):
    try:
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        question_data = firebase_get_question(question_id, grade, chapter, level)
        admin_email = question_data.get("approved_by")
        if not admin_email:
            raise ValueError("Admin not identified!")
        for admin in firebase_db.collection("users").where("email", "==", admin_email).stream():
            admin_id = admin.id
        question_updates = dict(
                                    is_deployed = True
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(admin_id).set({"total_questions_deployed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_deployed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e