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

    #Reviewer
    reviewer_dict = dict(
                        active_grade = [3],
                        country = "India",
                        email = "reviewer@pixelmath.org",
                        name = "PixelMath Reviewer",
                        phone_number = "1234567890",
                        profile_image = "https://pixel-editor-db-v2.s3.ap-south-1.amazonaws.com/profile_images/default.png",
                        total_questions_reviewed = 0,
                        type = "Reviewer"
                    )
    firebase_db.collection("users").document("reviewer").create(reviewer_dict)

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