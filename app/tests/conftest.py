from firebase_admin import credentials, initialize_app
from firebase_admin import firestore, auth
from app.data.grade_breakdown import data
from app.key import cred_json
from app import create_app
import firebase_admin
import pytest
import os

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_json)
    default_app = initialize_app(cred)

firebase_db = firestore.client()

#App Context Fixture
@pytest.fixture(scope='session')
def app():
  os.environ.update(
    dict(
      APP_SETTINGS='app.config.TestConfig',
    )
  )
  app = create_app()
  with app.app_context():
    return app

#Site Wide Testing
@pytest.fixture(scope='session')
def contributor_requests(app):
  with app.app_context():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["contributor_id"] = "contributor"
            session["email"] = "contributor@pixelmath.org"
            session["user_type"] = "Contributor"
        yield client

@pytest.fixture(scope='session')
def admin_requests(app):
  with app.app_context():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["admin_id"] = "admin"
            session["email"] = "admin@pixelmath.org"
            session["user_type"] = "Admin"
        yield client

@pytest.fixture(scope='session')
def graphics_requests(app):
  with app.app_context():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["graphics_id"] = "graphics"
            session["email"] = "graphics@pixelmath.org"
            session["user_type"] = "Graphics"
        yield client

@pytest.fixture(scope='session')
def super_admin_requests(app):
  with app.app_context():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["super_admin_id"] = "super_admin"
            session["email"] = "super_admin@pixelmath.org"
            session["user_type"] = "Super Admin"
        yield client



#Fixture for firebase db
@pytest.fixture(scope="session")
def firebase_db_ins():
    yield firestore.client()

#Function to reset the db before performing the tests
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


#Function to create the users before the tests
def seed_users():
    #Contributor
    individual_log = {}
    for grade_dict in data:
        for chapter_dict in grade_dict.get("chapters"):
            for level_dict in chapter_dict.get("levels"):
                individual_log[f"NCERT_G{grade_dict.get('grade_number'):02}_TOPIC{chapter_dict.get('chapter_number'):02}_LEVEL{level_dict.get('level_number'):02}"] = 0
    contributor_dict = dict(
                                active_grade = None,
                                approval_rate = 0,
                                country = "India",
                                daily_goal = "Submit at least 10 questions for today",
                                email = "contributor@pixelmath.org",
                                name = "PixelMath Contributor",
                                phone_number = "1234567890",
                                profile_image = "https://pixel-editor-db-v2.s3.ap-south-1.amazonaws.com/profile_images/default.png",
                                total_approved = 0,
                                total_questions = 0,
                                total_reviewed = 0,
                                total_star_questions = 0,
                                type = "Contributor",
                                individual_log = individual_log
                        )
    firebase_db.collection("users").document("contributor").create(contributor_dict)

    #Admin
    admin_dict = dict(
                        country = "India",
                        email = "admin@pixelmath.org",
                        name = "PixelMath Admin",
                        phone_number = "1234567890",
                        profile_image = "https://pixel-editor-db-v2.s3.ap-south-1.amazonaws.com/profile_images/default.png",
                        total_questions = 0,
                        total_questions_reviewed = 0,
                        type = "Admin"
                    )
    firebase_db.collection("users").document("admin").create(admin_dict)

    #Graphics
    graphics_dict = dict(
                            country = "India",
                            email = "graphics@pixelmath.org",
                            name = "PixelMath Graphics",
                            phone_number = "1234567890",
                            profile_image = "https://pixel-editor-db-v2.s3.ap-south-1.amazonaws.com/profile_images/default.png",
                            total_images_submitted = 0,
                            type = "Graphics"
                        )
    firebase_db.collection("users").document("graphics").create(graphics_dict)

    #Super Admin
    super_admin_dict = dict(
                                country = "India",
                                email = "super_admin@pixelmath.org",
                                name = "PixelMath Super Admin",
                                phone_number = "1234567890",
                                profile_image = "https://pixel-editor-db-v2.s3.ap-south-1.amazonaws.com/profile_images/default.png",
                                questions_deployed = 0,
                                questions_reviewed = 0,
                                type = "Super Admin"
                        )
    firebase_db.collection("users").document("super_admin").create(super_admin_dict)

    #Questions for graphics placeholder
    final_dict = {}
    for grade_dict in data:
        for chapter_dict in grade_dict.get("chapters"):
            chapter_id = f"NCERT_G{grade_dict.get('grade_number'):02}_TOPIC{chapter_dict.get('chapter_number'):02}"
            temp_chapter_dict = {}
            for level_dict in chapter_dict.get("levels"):
                questions_for_review = firebase_db.collection("questions").document(f"G{grade_dict.get('grade_number'):02}").collection("levels").document(f"NCERT_G{grade_dict.get('grade_number'):02}_TOPIC{chapter_dict.get('chapter_number'):02}_LEVEL{level_dict.get('level_number'):02}").collection("question_bank").where("state", "==", "graphics_required").stream()
                len_list = []
                for question in questions_for_review:
                    len_list.append(question.id)
                temp_chapter_dict[f"{chapter_id}_LEVEL{level_dict.get('level_number'):02}"] = len(len_list)
            final_dict[chapter_id] = temp_chapter_dict
    firebase_db.collection("questions_for_graphics").document("data").create(final_dict)

    #Questions for Super Admin Placeholder
    final_dict_super_admin = {}
    for grade_dict in data:
        for chapter_dict in grade_dict.get("chapters"):
            chapter_id = f"NCERT_G{grade_dict.get('grade_number'):02}_TOPIC{chapter_dict.get('chapter_number'):02}"
            temp_chapter_dict = {}
            for level_dict in chapter_dict.get("levels"):
                questions_for_review = firebase_db.collection("questions").document(f"G{grade_dict.get('grade_number'):02}").collection("levels").document(f"NCERT_G{grade_dict.get('grade_number'):02}_TOPIC{chapter_dict.get('chapter_number'):02}_LEVEL{level_dict.get('level_number'):02}").collection("question_bank").where("state", "==", "approved").where("is_deployed", "==", False).stream()
                len_list = []
                for question in questions_for_review:
                    len_list.append(question.id)
                temp_chapter_dict[f"{chapter_id}_LEVEL{level_dict.get('level_number'):02}"] = len(len_list)
            final_dict_super_admin[chapter_id] = temp_chapter_dict
    firebase_db.collection("super_admin_questions_for_review").document("data").create(final_dict_super_admin)


#Initialising Test Suite
if cred_json.get("project_id") == "pixel-editor-test":
    empty_db()
    seed_users()
else:
    print("Can only perform tests on Testing DB")