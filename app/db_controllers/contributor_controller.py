from firebase_admin import firestore
import json
from app.db_controllers.helper import *
from flask import request
import datetime
from google.cloud.firestore_v1 import Increment
import uuid
import time

firebase_db = firestore.client()

def get_user_document_data(contributor_id):
    try:
        document_ref = firebase_db.collection('users')
        user_data = document_ref.document(contributor_id).get()
        return user_data.to_dict()
    except Exception as e:
        raise e

def get_chart_data(contributor_id):
    try:
        document_ref = firebase_db.collection("users")
        last_7_days = []
        for days in range(1, 8):
            last_7_days.append(datetime.datetime.strftime(datetime.datetime.fromtimestamp(time.mktime(time.localtime())) - datetime.timedelta(days=days), "%d_%m_%Y"))
        return_list = [["date", "Total", "Individual"]]
        for day in last_7_days[::-1]:
            temp_list = [day.replace("_", "/")]
            total_contributions_on_day = firebase_db.collection("daily_question_log").document(day).get().to_dict()
            if total_contributions_on_day:
                temp_list.append(total_contributions_on_day.get("count"))
            else:
                temp_list.append(0)
            individual_contribution_on_day = document_ref.document(contributor_id).collection("daily_log").document(day).get().to_dict()
            if individual_contribution_on_day:
                temp_list.append(individual_contribution_on_day.get("count"))
            else:
                temp_list.append(0)
            if len(temp_list) == 3:
                return_list.append(temp_list)
        return return_list
    except Exception as e:
        raise e

def firebase_update_profile_image(contributor_id, profile_image_url):
    try:
        document_ref = firebase_db.collection('users')
        update_user = document_ref.document(contributor_id).update({"profile_image": profile_image_url})
    except Exception as e:
        raise e

def get_leaderboard_data(contributor_id):
    try:
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
    except Exception as e:
        raise e

def get_top_contributors_for_total_question():
    try:
        document_ref = firebase_db.collection("users")
        top_contributors_total_question = document_ref.order_by("total_questions", direction=firestore.Query.DESCENDING).limit(10).get()
        return [contributor.to_dict() for contributor in top_contributors_total_question]
    except Exception as e:
        raise e

def get_top_contributors_for_approval_rate():
    try:
        document_ref = firebase_db.collection("users")
        top_contributors_approval_rate = document_ref.order_by("approval_rate", direction=firestore.Query.DESCENDING).limit(10).get()
        return [contributor.to_dict() for contributor in top_contributors_approval_rate]
    except Exception as e:
        raise e

def get_star_questions():
    try:
        document_ref = firebase_db.collection("star_questions")
        star_questions_data = document_ref.order_by("marked_at", direction=firestore.Query.DESCENDING).limit(10).get()
        return [star_question_data.to_dict() for star_question_data in star_questions_data]
    except Exception as e:
        raise e

def get_notifications(contributor_id):
    try:
        document_ref = firebase_db.collection("users")
        notifications = document_ref.document(contributor_id).collection("notifications").order_by("created_at", direction=firestore.Query.DESCENDING).where("is_read", "==", False).limit(20).get()
        return [notification.to_dict() for notification in notifications]
    except Exception as e:
        raise e

def firebase_get_level_count(topic_id):
    try:
        document_ref = firebase_db.collection("total_questions")
        topic_data = document_ref.document(topic_id).get()
        return topic_data.to_dict() or {}
    except Exception as e:
        raise e

def firebase_submit_question(contributor_id):
    try:
        data = json.loads(request.form.get('json'))
        grade = data.get("grade")
        chapter = data.get("chapter")
        level = data.get("level")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, Chapter and Level are mandatory!")
        grade, chapter, level = int(grade), int(chapter), int(level)
        user_data = get_user_document_data(contributor_id)
        check_data(data)
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
                            is_paid = False,
                            state = "created",
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
                            is_deployed = False,
                            is_olympiad = False
                    )
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        level_collection_id = f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"
        document_ref = firebase_db.collection("users")
        question_document_ref = firebase_db.collection("questions")
        document_ref.document(contributor_id).update({"preview_question": firestore.DELETE_FIELD})
        question_document_id = str(uuid.uuid4())
        question_obj_ref = question_document_ref.document(f"G{grade:02}").collection("levels").document(level_collection_id).collection("question_bank").document(question_document_id).create(question)
        document_ref.document(contributor_id).update({"total_questions": Increment(1)})
        updated_individual_log = user_data.get("individual_log")
        updated_individual_log[level_collection_id] += 1
        document_ref.document(contributor_id).update({"individual_log": updated_individual_log})
        document_ref.document(contributor_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("total_questions").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({level_collection_id: Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"submitted": Increment(1)}, merge=True)
        question_obj_for_list = dict(
                                        question_id = question_document_id,
                                        assigned_to = None,
                                        grade = grade,
                                        chapter = chapter,
                                        level = level
                                    )
        firebase_db.collection("question_list").document().create(question_obj_for_list)
    except Exception as e:
        raise e
