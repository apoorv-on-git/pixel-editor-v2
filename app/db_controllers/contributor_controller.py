import requests
from firebase_admin import firestore
import json
from app.db_controllers.helper import *
from flask import request
import datetime
from google.cloud.firestore_v1 import Increment

firebase_db = firestore.client()

def get_user_document_data(contributor_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(contributor_id).get()
    return user_data.to_dict()

def firebase_update_profile_image(contributor_id, profile_image_url):
    document_ref = firebase_db.collection('users')
    update_user = document_ref.document(contributor_id).update({"profile_image": profile_image_url})

def get_leaderboard_data(contributor_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(contributor_id).get()
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

def get_top_contributors_for_total_question():
    document_ref = firebase_db.collection("users")
    top_contributors_total_question = document_ref.order_by("total_questions", direction=firestore.Query.DESCENDING).limit(10).get()
    return [contributor.to_dict() for contributor in top_contributors_total_question]

def get_top_contributors_for_approval_rate():
    document_ref = firebase_db.collection("users")
    top_contributors_approval_rate = document_ref.order_by("approval_rate", direction=firestore.Query.DESCENDING).limit(10).get()
    return [contributor.to_dict() for contributor in top_contributors_approval_rate]

def get_star_questions():
    document_ref = firebase_db.collection("star_questions")
    star_questions_data = document_ref.order_by("marked_at", direction=firestore.Query.DESCENDING).limit(10).get()
    return [star_question_data.to_dict() for star_question_data in star_questions_data]

def get_notifications(contributor_id):
    document_ref = firebase_db.collection("users")
    notifications = document_ref.document(contributor_id).collection("notifications").order_by("created_at", direction=firestore.Query.DESCENDING).where("is_read", "==", False).limit(20).get()
    return [notification.to_dict() for notification in notifications]

def firebase_get_level_count(topic_id):
    document_ref = firebase_db.collection("total_questions")
    topic_data = document_ref.document(topic_id).get()
    return topic_data.to_dict() or {}

def check_preview_question(contributor_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(contributor_id).get()
    user_data = user_data.to_dict()
    return user_data.get("preview_question")

def firebase_save_preview_question(contributor_id):
    try:
        data = json.loads(request.form.get('json'))
        check_data(data)
        grade, chapter, level = int(data.get("grade")), int(data.get("chapter")), int(data.get("level"))
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(data, contributor_id)
        question_text = remove_style(data.get("question"))
        preview_question = dict(
                                    grade=grade,
                                    chapter=chapter,
                                    level=level,
                                    question_text=question_text,
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
        save_preview_question = document_ref.document(contributor_id).update({"preview_question": preview_question})
    except Exception as e:
        raise e

def firebase_delete_preview_question(contributor_id):
    try:
        document_ref = firebase_db.collection("users")
        document_ref.document(contributor_id).update({"preview_question": firestore.DELETE_FIELD})
    except Exception as e:
        raise e

def firebase_submit_question(contributor_id):
    try:
        data = json.loads(request.form.get('json'))
        user_data = get_user_document_data(contributor_id)
        check_data(data)
        grade, chapter, level = int(data.get("grade")), int(data.get("chapter")), int(data.get("level"))
        question_image, option_a, option_b, option_c, option_d = handle_submitted_images(data, contributor_id)
        question_image, option_a, option_b, option_c, option_d = get_files_renamed(question_image, option_a, option_b, option_c, option_d)
        question_text = remove_style(data.get("question"))
        question = dict(
                            board_type = "NCERT",
                            grade = grade,
                            chapter = chapter,
                            level = level,
                            contributor_id = contributor_id,
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
                            deployed_by = None
                    )
        level_collection_id = f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"
        document_ref = firebase_db.collection("users")
        question_document_ref = firebase_db.collection("questions")
        document_ref.document(contributor_id).update({"preview_question": firestore.DELETE_FIELD})
        question_document_ref.document(f"G{grade:02}").collection("levels").document(level_collection_id).collection("question_bank").document().create(question)
        document_ref.document(contributor_id).update({"total_questions": Increment(1)})
        updated_individual_log = user_data.get("individual_log")
        updated_individual_log[level_collection_id] += 1
        document_ref.document(contributor_id).update({"individual_log": updated_individual_log})
        firebase_db.collection("total_questions").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({level_collection_id: Increment(1)}, merge=True)
    except Exception as e:
        raise e
