from firebase_admin import credentials, initialize_app
from firebase_admin import firestore, auth
from app.data.grade_breakdown import data
from app.key import cred_json
import firebase_admin
from app import create_app

app = create_app()

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_json)
    default_app = initialize_app(cred)

firebase_db = firestore.client()

def empty_db():
    #Removing admin questions for review
    admin_questions_for_review_doc_ids = []
    for admin_questions_for_review in firebase_db.collection("admin_questions_for_review").stream():
        admin_questions_for_review_doc_ids.append(admin_questions_for_review.id)
    for admin_questions_for_review_id in admin_questions_for_review_doc_ids:
        firebase_db.collection("admin_questions_for_review").document(admin_questions_for_review_id).delete()

    #Removing cumulative data
    firebase_db.collection("cumulative_data").document('data').delete()

    #Removing daily question log
    daily_question_log_ids = []
    for daily_question_log in firebase_db.collection("daily_question_log").stream():
        daily_question_log_ids.append(daily_question_log.id)
    for daily_question_log_id in daily_question_log_ids:
        firebase_db.collection("daily_question_log").document(daily_question_log_id).delete()

    #Removing error logs
    error_log_ids = []
    for error_log in firebase_db.collection("error_log").stream():
        error_log_ids.append(error_log.id)
    for error_log_id in error_log_ids:
        firebase_db.collection("error_log").document(error_log_id).delete()

    #Removing question list
    question_list_ids = []
    for question_list in firebase_db.collection("question_list").stream():
        question_list_ids.append(question_list.id)
    for question_list_id in question_list_ids:
        firebase_db.collection("question_list").document(question_list_id).delete()
    
    #Removing questions
    question_ids = []
    for question in firebase_db.collection("questions").stream():
        question_ids.append(question.id)
    for question_id in question_ids:
        #Removing question levels
        level_ids = []
        for level in firebase_db.collection("questions").document(question_id).collection("levels").stream():
            level_ids.append(level.id)
        for level_id in level_ids:
            #Removing question bank
            question_bank_ids = []
            for question_bank in firebase_db.collection("questions").document(question_id).collection("levels").document(level_id).collection("question_bank").stream():
                question_bank_ids.append(question_bank.id)
            for question_bank_id in question_bank_ids:
                firebase_db.collection("questions").document(question_id).collection("levels").document(level_id).collection("question_bank").document(question_bank_id).delete()
            firebase_db.collection("questions").document(question_id).collection("levels").document(level_id).delete()
        firebase_db.collection("questions").document(question_id).delete()
    
    #Removing questions for graphics
    firebase_db.collection("questions_for_graphics").document("data").delete()

    #Removing star questions
    star_question_ids = []
    for star_question in firebase_db.collection("star_questions").stream():
        star_question_ids.append(star_question.id)
    for star_question_id in star_question_ids:
        firebase_db.collection("star_questions").document(star_question_id).delete()

    #Removing super admin questions for review
    super_admin_questions_for_review_ids = []
    for super_admin_questions_for_review in firebase_db.collection("super_admin_questions_for_review").stream():
        super_admin_questions_for_review_ids.append(super_admin_questions_for_review.id)
    for super_admin_questions_for_review_id in super_admin_questions_for_review_ids:
        firebase_db.collection("super_admin_questions_for_review").document(super_admin_questions_for_review_id).delete()

    #Removing total questions
    total_question_ids = []
    for total_questions in firebase_db.collection("total_questions").stream():
        total_question_ids.append(total_questions.id)
    for total_question_id in total_question_ids:
        firebase_db.collection("total_questions").document(total_question_id).delete()

    #Removing users
    user_ids = []
    for user in firebase_db.collection("users").stream():
        user_ids.append(user.id)
    for user_id in user_ids:
        #Removing user notifications
        notification_ids = []
        for notification in firebase_db.collection("users").document(user_id).collection("notifications").stream():
            notification_ids.append(notification.id)
        for notification_id in notification_ids:
            firebase_db.collection("users").document(user_id).collection("notifications").document(notification_id).delete()
        
        #Removing user daily logs
        daily_log_ids = []
        for daily_log in firebase_db.collection("users").document(user_id).collection("daily_log").stream():
            daily_question_log_ids.append(daily_log.id)
        for daily_log_id in daily_log_ids:
            firebase_db.collection("users").document(used_id).collection("daily_log").document(daily_log_id).delete()
        firebase_db.collection("users").document(user_id).delete()