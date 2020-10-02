from google.cloud.firestore_v1 import Increment
from firebase_admin import firestore
import datetime
import time

firebase_db = firestore.client()

def get_user_document_data(document_id):
    try:
        document_ref = firebase_db.collection('users')
        user_data = document_ref.document(document_id).get()
        return user_data.to_dict()
    except Exception as e:
        raise e

def firebase_get_reviewer_question_list(document_id):
    try:
        question_ids = []
        for question in firebase_db.collection("question_list").where("assigned_to", "==", document_id).where("reviewed", "==", False).stream():
            question_ids.append(question.id)
        return question_ids
    except Exception as e:
        raise e

def firebase_assign_questions_to_reviewer(document_id):
    try:
        reviewer = get_user_document_data(document_id)
        question_ids = []
        for question in firebase_db.collection("question_list").where("assigned_to", "==", None).where("grade", "in", reviewer.get("active_grade")).limit(20).stream():
            question_ids.append(question.id)
        if len(question_ids) == 0:
            return False
        for question_id in question_ids:
            update = dict(
                            assigned_to=document_id
                        )
            firebase_db.collection("question_list").document(question_id).update(update)
        return firebase_get_reviewer_question_list(document_id)
    except Exception as e:
        raise e

def firebase_get_question_meta_data(question_id):
    try:
        question_list_obj = firebase_db.collection("question_list").document(question_id).get().to_dict()
        if question_list_obj:
            return question_list_obj
        else:
            raise ValueError("Invalid question ID")
    except Exception as e:
        raise e

def firebase_get_question(question_id):
    try:
        question_obj = firebase_db.collection("questions").document(question_id).get().to_dict()
        if question_obj:
            return question_obj
        else:
            raise ValueError("Invalid question ID")
    except Exception as e:
        raise e

def firebase_mark_question_good(question_id, reviewer_id):
    print(question_id)
    try:
        reviewer = get_user_document_data(reviewer_id)
        question_meta_data = firebase_get_question_meta_data(question_id)
        question_data = firebase_db.collection("questions").document(question_meta_data.get("question_doc_id")).get().to_dict()
        contributor_id = question_data.get("contributor_id")
        # question_data = firebase_get_question(question_meta_data.get("question_id"), question_meta_data.get("grade"), question_meta_data.get("chapter"), question_meta_data.get("level"))
        question_updates = dict(
                                        approved_by = reviewer.get("email"),
                                        date_approved = datetime.datetime.utcnow(),
                                        reviewed_by = reviewer.get("email"),
                                        date_reviewed = datetime.datetime.utcnow(),
                                        state = "approved"
                                )
        local_date = time.localtime()
        grade = question_meta_data.get("grade")
        chapter = question_meta_data.get("chapter")
        level = question_meta_data.get("level")
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(question_meta_data.get("question_doc_id")).update(question_updates)
        firebase_db.collection("users").document(reviewer_id).set({"total_questions_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"total_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(reviewer_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"reviewer_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("cumulative_data").document("data").set({"admin_approved": Increment(1)}, merge=True)
        question_list_update = dict(
                                        reviewed = True
                                    )
        firebase_db.collection("question_list").document(question_id).update(question_list_update)
    except Exception as e:
        raise e

def firebase_mark_question_bad(question_id, reviewer_id, bad_type, feedback):
    '''
    Bad Type 1 - Bad Question
    Bad Type 2 - Spelling Mistake
    Bad Type 3 - Bad Graphics
    '''
    try:
        reviewer = get_user_document_data(reviewer_id)
        question_meta_data = firebase_get_question_meta_data(question_id)
        grade = question_meta_data.get("grade")
        chapter = question_meta_data.get("chapter")
        level = question_meta_data.get("level")
        question_data = firebase_db.collection("questions").document(question_meta_data.get("question_doc_id")).get().to_dict()
        contributor_id = question_data.get("contributor_id")
        if bad_type == 3:
            question_updates = dict(
                                        state = "graphics_required",
                                        reviewer_feedback = feedback
                                    )
        elif bad_type in [1, 2]:
            question_updates = dict(
                                        state = "under_review",
                                        reviewer_feedback = feedback
                                    )
        else:
            raise ValueError("bad_type should be an Integer. It's value can only be 1, 2 or 3")
        local_date = time.localtime()
        local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
        firebase_db.collection("questions").document(question_meta_data.get("question_doc_id")).update(question_updates)
        firebase_db.collection("users").document(reviewer_id).set({"total_questions_reviewed": Increment(1)}, merge=True)
        if bad_type not in [1, 2]:
            firebase_db.collection("cumulative_data").document("data").set({"total_reviewed": Increment(1)}, merge=True)
        firebase_db.collection("users").document(reviewer_id).collection("daily_log").document(local_date).set({"count": Increment(1)}, merge=True)
        firebase_db.collection("daily_question_log").document(local_date).set({"reviewer_reviewed": Increment(1)}, merge=True)
        question_list_update = dict(
                                        reviewed = True
                                    )
        firebase_db.collection("question_list").document(question_id).update(question_list_update)

    except Exception as e:
        raise e