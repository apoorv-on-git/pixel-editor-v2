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

def firebase_get_questions_for_review(topic_id):
    document_ref = firebase_db.collection("admin_questions_for_review")
    topic_data = document_ref.document(topic_id).get()
    return topic_data.to_dict() or {}

def firebase_get_questions_for_review_list(grade, chapter, level):
    document_ref = firebase_db.collection("questions")
    questions_for_review = document_ref\
                            .document(f"G{grade:02}")\
                            .collection("levels")\
                            .document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")\
                            .collection("question_bank")\
                            .where("state", "==", "under_review")\
                            .stream()
    document_id_list = []
    for question in questions_for_review:
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

def firebase_update_profile_image(admin_id, profile_image_url):
    document_ref = firebase_db.collection('users')
    update_user = document_ref.document(admin_id).update({"profile_image": profile_image_url})

def get_admin_review_stats():
    document_ref = firebase_db.collection("users").where("type", "==", "Admin")
    admin_id_list = []
    for admin in document_ref.stream():
        admin_id_list.append(admin.id)
    return_list = []
    for admin_id in admin_id_list:
        admin_data = firebase_db.collection("users").document(admin_id).get().to_dict()
        _d = dict(
                    name = admin_data.get("name"),
                    profile_image = admin_data.get("profile_image"),
                    total_questions_reviewed = admin_data.get("total_questions_reviewed"),
                    total_questions_reviewed = admin_data.get("total_questions_deployed")
                )
        return_list.append(_d)
    return return_list

def get_cumulative_chart_data():
    document_ref = firebase_db.collection("cumulative_data")
    cumulative_data = document_ref.document("data").get().to_dict()
    return cumulative_data

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
                            contributor_id = admin_id,
                            contributor_name = user_data.get("name"),
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
                            deployed_by = None,
                            is_deployed = False
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
        firebase_db.collection("admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({level_collection_id: Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"submitted": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_disapprove_question(admin_id):
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
        question_data = firebase_get_question(question_id, grade, chapter, level)
        contributor_id = question_data.get("contributor_id")
        if not contributor_id:
            raise ValueError("Contributor not identified!")
        user_data = get_user_document_data(admin_id)
        contributor_data = get_user_document_data(contributor_id)
        question_updates = dict(
                                    state = "disapproved",
                                    reviewed_by = user_data.get("email"),
                                    feedback = feedback,
                                    date_reviewed = datetime.datetime.utcnow()
                            )
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(admin_id).set({"total_questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(contributor_id).set({"total_reviewed": Increment(1)}, merge=True)
        notification_dict = dict(
                                    contributed_by = contributor_id,
                                    contributor_name = contributor_data.get("name"),
                                    correct_answer = question_data.get("correct_option"),
                                    created_at = datetime.datetime.utcnow(),
                                    options = question_data.get("options"),
                                    question_image = question_data.get("question_image"),
                                    question_text = question_data.get("question_text"),
                                    feedback = feedback,
                                    is_read = False,
                                    tags = [f"Grade {grade}", f"Chapter {chapter}", f"Level {level}"]
                                )
        firebase_db.collection("users").document(contributor_id).collection("notifications").document().create(notification_dict)
        questions_for_review = firebase_get_questions_for_review(f"NCERT_G{grade:02}_TOPIC{chapter:02}")
        current_questions_for_review = questions_for_review.get(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")
        firebase_db.collection("admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": (current_questions_for_review - 1)})
        firebase_db.collection("cumulative_data").document("data").set({"reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_approve_question(admin_id):
    try:
        graphics_required = request.json.get("graphics_required")
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if graphics_required == "":
            raise ValueError("Please tell us if this question requires graphic work or not!")
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        if graphics_required.lower() == "yes":
            graphics_required = True
        else:
            graphics_required = False
        question_data = firebase_get_question(question_id, grade, chapter, level)
        contributor_id = question_data.get("contributor_id")
        if not contributor_id:
            raise ValueError("Contributor not identified!")
        user_data = get_user_document_data(admin_id)
        new_question_data = request.json.get("question_json")
        check_data(new_question_data)
        question_text = remove_style(new_question_data.get("question"))
        question_updates = dict(
                                    approved_by = user_data.get("email"),
                                    correct_option = new_question_data.get("correct_option"),
                                    date_approved = datetime.datetime.utcnow(),
                                    options = dict(
                                                    option_a = new_question_data.get("option_a"),
                                                    option_b = new_question_data.get("option_b"),
                                                    option_c = new_question_data.get("option_c"),
                                                    option_d = new_question_data.get("option_d")
                                                ),
                                    question_text = question_text,
                                    reviewed_by = user_data.get("email"),
                                    feedback = request.json.get("feedback"),
                                    date_reviewed = datetime.datetime.utcnow()
                            )
        if graphics_required:
            question_updates["state"] = "graphics_required"
        else:
            question_updates["state"] = "approved"
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(admin_id).set({"total_questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(contributor_id).set({"total_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(contributor_id).set({"total_approved": Increment(1)}, merge=True)
        questions_for_review = firebase_get_questions_for_review(f"NCERT_G{grade:02}_TOPIC{chapter:02}")
        current_questions_for_review = questions_for_review.get(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}")
        firebase_db.collection("admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": (current_questions_for_review - 1)})
        firebase_db.collection("cumulative_data").document("data").set({"reviewed": Increment(1)}, merge=True)
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("users").document(contributor_id).collection("daily_log").document(local_date).set({"approved": Increment(1)}, merge=True)
        if graphics_required:
            graphics_dict = firebase_db.collection("questions_for_graphics").document("data").get().to_dict()
            graphics_dict[f"NCERT_G{grade:02}_TOPIC{chapter:02}"][f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"] += 1
            firebase_db.collection("questions_for_graphics").document("data").update(graphics_dict)
        else:
            firebase_db.collection("super_admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(1)})
    except Exception as e:
        raise e
