from google.cloud.firestore_v1 import Increment
from firebase_admin import firestore
from app.db_controllers.helper import *
from flask import request
import datetime
import time
import json

firebase_db = firestore.client()

def get_chart_data(super_admin_id):
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
                temp_list.append(total_contributions_on_day.get("super_admin_reviewed") or 0)
            else:
                temp_list.append(0)
            individual_contribution_on_day = document_ref.document(super_admin_id).collection("daily_log").document(day).get().to_dict()
            if individual_contribution_on_day:
                temp_list.append(individual_contribution_on_day.get("count") or 0)
            else:
                temp_list.append(0)
            if len(temp_list) == 3:
                return_list.append(temp_list)
        return return_list
    except Exception as e:
        raise e

def get_user_document_data(super_admin_id):
    try:
        document_ref = firebase_db.collection('users')
        user_data = document_ref.document(super_admin_id).get()
        return user_data.to_dict()
    except Exception as e:
        raise e

def firebase_update_profile_image(super_admin_id, profile_image_url):
    try:
        document_ref = firebase_db.collection('users')
        update_user = document_ref.document(super_admin_id).update({"profile_image": profile_image_url})
    except Exception as e:
        raise e

def get_admin_review_stats():
    try:
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
                        total_questions_deployed = admin_data.get("total_questions_deployed")
                    )
            return_list.append(_d)
        return return_list
    except Exception as e:
        raise e

def get_cumulative_chart_data():
    try:
        document_ref = firebase_db.collection("cumulative_data")
        cumulative_data = document_ref.document("data").get().to_dict()
        return cumulative_data
    except Exception as e:
        raise e

def firebase_get_approved_question_count(topic_id):
    try:
        document_ref = firebase_db.collection("super_admin_questions_for_review")
        topic_data = document_ref.document(topic_id).get()
        return topic_data.to_dict() or {}
    except Exception as e:
        raise e

def firebase_get_questions_for_super_admin_list(grade, chapter, level):
    try:
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
        question_data = firebase_get_question(question_id, grade, chapter, level)
        admin_email = question_data.get("approved_by")
        if not admin_email:
            raise ValueError("Admin not identified!")
        for admin in firebase_db.collection("users").where("email", "==", admin_email).stream():
            admin_id = admin.id
        contributor_id = question_data.get("contributor_id")
        if not contributor_id:
            raise ValueError("Contributor not identified!")
        contributor_data = get_user_document_data(contributor_id)
        question_updates = dict(
                                    state="under_review",
                                    super_admin_feedback = feedback
                            )
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(admin_id).set({"total_questions_reviewed": Increment(-1)}, merge=True)
        firebase_db.collection("users").document(contributor_id).set({"total_reviewed": Increment(-1)}, merge=True)
        firebase_db.collection("users").document(contributor_id).set({"total_approved": Increment(-1)}, merge=True)
        firebase_db.collection("admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").set({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"reviewed": Increment(-1), "admin_approved": Increment(-1)}, merge=True)
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("users").document(contributor_id).collection("daily_log").document(local_date).set({"approved": Increment(-1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("super_admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(-1)})
        firebase_db.collection("users").document(super_admin_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"super_admin_reviewed": Increment(1)}, merge=True)
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
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        graphics_dict = firebase_db.collection("questions_for_graphics").document("data").get().to_dict()
        graphics_dict[f"NCERT_G{grade:02}_TOPIC{chapter:02}"][f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}"] += 1
        firebase_db.collection("questions_for_graphics").document("data").update(graphics_dict)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("super_admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(-1)})
        firebase_db.collection("cumulative_data").document("data").set({"admin_approved": Increment(-1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"super_admin_reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_star_question(super_admin_id):
    try:
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        feedback = request.json.get("feedback")
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        if not feedback:
            raise ValueError("Feedback is important!")
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
                                    question_text = question_data.get("question_text"),
                                    tags = [
                                                f"Grade {grade}",
                                                f"Chapter {chapter}",
                                                f"Level {level}"
                                            ],
                                    feedback = feedback
                                )
        firebase_db.collection("star_questions").document().create(star_question_log)
    except Exception as e:
        raise e

def firebase_discard_question(super_admin_id):
    try:
        question_id = request.json.get("document_id")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        feedback = request.json.get("feedback")
        if not question_id:
            raise ValueError("Invalid Question")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        if not feedback:
            raise ValueError("Feedback is important!")
        question_updates = dict(
                                    state = "disapproved",
                                    super_admin_feedback = feedback
                            )
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("super_admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(-1)})
        firebase_db.collection("users").document(super_admin_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"super_admin_reviewed": Increment(1)}, merge=True)
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
        new_question_data = request.json.get("question_json")
        check_data(new_question_data)
        question_text = remove_style(new_question_data.get("question"))
        question_updates = dict(
                                    is_deployed = True,
                                    question_text = question_text,
                                    options = dict(
                                                    option_a = new_question_data.get("option_a"),
                                                    option_b = new_question_data.get("option_b"),
                                                    option_c = new_question_data.get("option_c"),
                                                    option_d = new_question_data.get("option_d")
                                                ),
                                    correct_option = new_question_data.get("correct_option")
                            )
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
        firebase_db.collection("users").document(admin_id).set({"total_questions_deployed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_deployed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).set({"questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("super_admin_questions_for_review").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}").update({f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}": Increment(-1)})
        firebase_db.collection("cumulative_data").document("data").set({"super_admin_deployed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(super_admin_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"super_admin_reviewed": Increment(1)}, merge=True)
    except Exception as e:
        raise e

def firebase_delete_image(super_admin_id):
    try:
        question_id = request.json.get("document_id")
        image_type = request.json.get("image_type")
        grade = int(request.json.get("grade"))
        chapter = int(request.json.get("chapter"))
        level = int(request.json.get("level"))
        if not question_id or not image_type:
            raise ValueError("Invalid Request")
        if not all((grade, chapter, level)):
            raise ValueError("Grade, chapter or level unidentified!")
        if image_type == "question_image":
            question_obj = firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).get().to_dict()
            old_question_image = question_obj.get("question_image")
            delete_question_image(old_question_image)
            question_updates = dict(
                                        question_image = "#"
                                    )
            firebase_db.collection("questions").document(f"G{grade:02}").collection("levels").document(f"NCERT_G{grade:02}_TOPIC{chapter:02}_LEVEL{level:02}").collection("question_bank").document(question_id).update(question_updates)
    except Exception as e:
        raise e