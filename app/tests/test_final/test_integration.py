import time

#Contributor
'''
Contributor Submit Question
'''
def test_contributor_submit_question(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_contributor_submit_question_without_grade(contributor_requests):
    question_dict = {
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_chapter(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_level(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_grade_int(contributor_requests):
    question_dict = {
                            "grade": "Three",
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_question(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_question_image(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_contributor_submit_question_without_question_option_a(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_question_option_b(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_question_option_c(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_submit_question_without_question_option_d(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "correct_option": "option_c"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_contributor_submit_question_with_two_options(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "correct_option": "option_a"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_contributor_submit_question_with_invalid_answer(contributor_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "correct_option": "option_e"
                    }
    resp = contributor_requests.post('/contributor-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_contributor_total_question_count(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert user_document.get("total_questions") == 4

def test_contributor_individual_log(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert user_document.get("individual_log").get("NCERT_G03_TOPIC01_LEVEL01") == 4

def test_contributor_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("users").document("contributor").collection("daily_log").document(local_date).get().to_dict()
    assert daily_log_document.get("count") == 4

def test_daily_log_count_after_contributor(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert daily_log_document.get("count") == 4

def test_contributor_total_questions_count(firebase_db_ins):
    total_questions_document = firebase_db_ins.collection("total_questions").document("NCERT_G03_TOPIC01").get().to_dict()
    assert total_questions_document.get("NCERT_G03_TOPIC01_LEVEL01") == 4

def test_contributor_admin_questions_for_review_count(firebase_db_ins):
    admin_questions_for_review_document = firebase_db_ins.collection("admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 4

def test_contributor_cumulative_data_count(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("submitted") == 4


#Admin
'''
Admin Submit Question
'''
def test_admin_submit_question(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_admin_submit_question_without_grade(admin_requests):
    question_dict = {
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_chapter(admin_requests):
    question_dict = {
                            "grade": 3,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_level(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_grade_int(admin_requests):
    question_dict = {
                            "grade": "Three",
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_question(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_question_image(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_admin_submit_question_without_question_option_a(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_question_option_b(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_c": "Option C",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_question_option_c(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_d": "Option D",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_submit_question_without_question_option_d(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "option_c": "Option C",
                            "correct_option": "option_c"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_admin_submit_question_with_two_options(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "correct_option": "option_a"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 204

def test_admin_submit_question_with_invalid_answer(admin_requests):
    question_dict = {
                            "grade": 3,
                            "chapter": 1,
                            "level": 1,
                            "question": "Testing Question",
                            "question_image": "#",
                            "option_a": "Option A",
                            "option_b": "Option B",
                            "correct_option": "option_e"
                    }
    resp = admin_requests.post('/admin-api/submit-question', data={"json": str(question_dict).replace("\'", "\"")})
    assert resp.status_code == 400

def test_admin_total_question_count(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("admin").get().to_dict()
    assert user_document.get("total_questions") == 4

def test_admin_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert daily_log_document.get("count") == 8

def test_admin_total_questions_count(firebase_db_ins):
    total_questions_document = firebase_db_ins.collection("total_questions").document("NCERT_G03_TOPIC01").get().to_dict()
    assert total_questions_document.get("NCERT_G03_TOPIC01_LEVEL01") == 8

def test_admin_admin_questions_for_review_count(firebase_db_ins):
    admin_questions_for_review_document = firebase_db_ins.collection("admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 8

def test_admin_cumulative_data_count(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("submitted") == 8

'''
Admin Disapprove Question
'''

def test_admin_disapprove_question(admin_requests, firebase_db_ins):
    json = {
                "feedback": "Testing Disapprove",
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json["document_id"] = document_id
    resp = admin_requests.post('/admin-api/disapprove-question', json=json)
    assert resp.status_code == 204

def test_admin_disapprove_question_without_grade(admin_requests, firebase_db_ins):
    json = {
                "feedback": "Testing Disapprove",
                "chapter": 1,
                "level": 1
        }
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json["document_id"] = document_id
    resp = admin_requests.post('/admin-api/disapprove-question', json=json)
    assert resp.status_code == 400

def test_admin_disapprove_question_without_chapter(admin_requests, firebase_db_ins):
    json = {
                "feedback": "Testing Disapprove",
                "grade": 3,
                "level": 1
        }
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json["document_id"] = document_id
    resp = admin_requests.post('/admin-api/disapprove-question', json=json)
    assert resp.status_code == 400

def test_admin_disapprove_question_without_level(admin_requests, firebase_db_ins):
    json = {
                "feedback": "Testing Disapprove",
                "grade": 3,
                "chapter": 1
        }
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json["document_id"] = document_id
    resp = admin_requests.post('/admin-api/disapprove-question', json=json)
    assert resp.status_code == 400

def test_admin_disapprove_question_without_document_id(admin_requests, firebase_db_ins):
    json = {
                "feedback": "Testing Disapprove",
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = admin_requests.post('/admin-api/disapprove-question', json=json)
    assert resp.status_code == 400

def test_admin_disapprove_question_admin_total_questions_reviewed(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("admin").get().to_dict()
    assert user_document.get("total_questions_reviewed") == 1

def test_admin_disapprove_question_contributor_reviewed(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert user_document.get("total_reviewed") == 1

def test_admin_disapprove_question_notification(firebase_db_ins):
    notification_id = ""
    for notification in firebase_db_ins.collection("users").document("contributor").collection("notifications").stream():
        notification_id = notification.id
    notitification_document = firebase_db_ins.collection("users").document("contributor").collection("notifications").document(notification_id).get().to_dict()
    if notitification_document:
        assert True
    else:
        assert False

def test_admin_disapprove_question_questions_for_review_admin(firebase_db_ins):
    admin_questions_for_review_document = firebase_db_ins.collection("admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 7

def test_admin_disapprove_question_cumulative_data(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("reviewed") == 1

def test_admin_disapprove_question_daily_log(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("users").document("admin").collection("daily_log").document(local_date).get().to_dict()
    assert daily_log_document.get("count") == 1

def test_admin_disapprove_question_daily_question_log(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert daily_log_document.get("admin_reviewed") == 1

'''
Admin Approve Question
'''

def test_admin_approve_question_graphics_required(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 204

def test_admin_approve_question_graphics_not_required(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "no",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 204

def test_admin_approve_question_graphics_required_none(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_question_without_document_id(admin_requests, firebase_db_ins):
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_question_without_grade(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_question_without_chapter(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_question_without_level(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_question_without_question_json(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "yes",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 400

def test_admin_approve_total_questions_reviewed(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("admin").get().to_dict()
    assert user_document.get("total_questions_reviewed") == 3

def test_admin_approve_contributor_total_approved(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert user_document.get("total_approved") == 2

def test_admin_approve_contributor_total_reviewed(firebase_db_ins):
    user_document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert user_document.get("total_questions") == 4

def test_admin_approve_admin_questions_for_review(firebase_db_ins):
    admin_questions_for_review_document = firebase_db_ins.collection("admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 5

def test_admin_approve_cumulative_data_reviewed(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("reviewed") == 3

def test_admin_approve_cumulative_data_admin_approved(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("admin_approved") == 1

def test_admin_approve_contributor_daily_log_approved(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("users").document("contributor").collection("daily_log").document(local_date).get().to_dict()
    assert daily_log_document.get("approved") == 2

def test_admin_approve_admin_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("users").document("admin").collection("daily_log").document(local_date).get().to_dict()
    assert daily_log_document.get("count") == 3

def test_admin_approve_daily_question_log_admin_approved(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    daily_log_document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert daily_log_document.get("admin_reviewed") == 3

def test_admin_approve_super_admin_questions_for_review(firebase_db_ins):
    super_admin_questions_for_review_document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert super_admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 1

def test_admin_approve_questions_for_graphics(firebase_db_ins):
    questions_for_graphics_document = firebase_db_ins.collection("questions_for_graphics").document("data").get().to_dict()
    assert questions_for_graphics_document.get("NCERT_G03_TOPIC01").get("NCERT_G03_TOPIC01_LEVEL01") == 1

#Graphics
'''
Graphics Submit Question
'''

def test_graphics_submit_question(graphics_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "graphics_required").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question Graphics",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 204

def test_graphics_submit_question_without_document_id(graphics_requests, firebase_db_ins):
    json = {
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question Graphics",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 400

def test_graphics_submit_question_without_grade(graphics_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "graphics_required").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question Graphics",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 400

def test_graphics_submit_question_without_chapter(graphics_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "graphics_required").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question Graphics",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 400

def test_graphics_submit_question_without_level(graphics_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "graphics_required").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question Graphics",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 400

def test_graphics_submit_question_without_question_json(graphics_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "graphics_required").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = graphics_requests.post('/graphics-api/save-question', data={"json": str(json).replace("\'", "\"")})
    assert resp.status_code == 400

def test_graphics_submit_questions_for_graphics(firebase_db_ins):
    questions_for_graphics_document = firebase_db_ins.collection("questions_for_graphics").document("data").get().to_dict()
    assert questions_for_graphics_document.get("NCERT_G03_TOPIC01").get("NCERT_G03_TOPIC01_LEVEL01") == 0

def test_graphics_submit_super_admin_questions_for_review(firebase_db_ins):
    super_admin_questions_for_review_document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert super_admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 2

def test_graphics_submit_cumulative_admin_approved(firebase_db_ins):
    cumulative_data_document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert cumulative_data_document.get("admin_approved") == 2

#Super Admin
'''
Super Admin Disapprove Quality
'''

def test_super_admin_disapprove_quality(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Quality Testing",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 204

def test_super_admin_disapprove_quality_without_feedback(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_quality_without_document_id(super_admin_requests, firebase_db_ins):
    json = {
                "feedback": "Super Admin Disapprove Quality Testing",
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_quality_without_grade(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Quality Testing",
                "document_id": document_id,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_quality_without_chapter(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Quality Testing",
                "document_id": document_id,
                "grade": 3,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_quality_without_level(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Quality Testing",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-quality', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_quality_admin_total_questions_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("admin").get().to_dict()
    assert document.get("total_questions_reviewed") == 2

def test_super_admin_disapprove_quality_contributor_total_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert document.get("total_reviewed") == 2

def test_super_admin_disapprove_quality_contributor_total_approved(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert document.get("total_approved") == 1

def test_super_admin_disapprove_quality_admin_questions_for_review(firebase_db_ins):
    document = firebase_db_ins.collection("admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert document.get("NCERT_G03_TOPIC01_LEVEL01") == 6

def test_super_admin_disapprove_quality_cumulative_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert document.get("reviewed") == 2

def test_super_admin_disapprove_quality_cumulative_admin_approved(firebase_db_ins):
    document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert document.get("admin_approved") == 1

def test_super_admin_disapprove_quality_contributor_daily_log_approved(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("users").document("contributor").collection("daily_log").document(local_date).get().to_dict()
    assert document.get("approved") == 1

def test_super_admin_disapprove_quality_super_admin_questions_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("super_admin").get().to_dict()
    assert document.get("questions_reviewed") == 1

def test_super_admin_disapprove_quality_super_admin_questions_for_review(firebase_db_ins):
    document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert document.get("NCERT_G03_TOPIC01_LEVEL01") == 1

def test_super_admin_disapprove_quality_super_admin_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("users").document("super_admin").collection("daily_log").document(local_date).get().to_dict()
    assert document.get("count") == 1

def test_super_admin_disapprove_quality_daily_question_log_super_admin_reviewed(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert document.get("super_admin_reviewed") == 1

'''
Super Admin Disapprove Graphics
'''

def test_super_admin_disapprove_graphics(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Graphics Testing",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 204

def test_super_admin_disapprove_graphics_without_feedback(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_graphics_without_document_id(super_admin_requests, firebase_db_ins):
    json = {
                "feedback": "Super Admin Disapprove Graphics Testing",
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_graphics_without_grade(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Graphics Testing",
                "document_id": document_id,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_graphics_without_chapter(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Graphics Testing",
                "document_id": document_id,
                "grade": 3,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_graphics_without_level(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "feedback": "Super Admin Disapprove Graphics Testing",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1
        }
    resp = super_admin_requests.post('/super-admin-api/disapprove-graphics', json=json)
    assert resp.status_code == 400

def test_super_admin_disapprove_graphics_questions_for_graphics(firebase_db_ins):
    document = firebase_db_ins.collection("questions_for_graphics").document("data").get().to_dict()
    assert document.get("NCERT_G03_TOPIC01").get("NCERT_G03_TOPIC01_LEVEL01") == 1

def test_super_admin_disapprove_graphics_super_admin_questions_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("super_admin").get().to_dict()
    assert document.get("questions_reviewed") == 2

def test_super_admin_disapprove_graphics_super_admin_questions_for_review(firebase_db_ins):
    document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert document.get("NCERT_G03_TOPIC01_LEVEL01") == 0

def test_super_admin_disapprove_graphics_cumulative_admin_approved(firebase_db_ins):
    document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert document.get("admin_approved") == 0

def test_super_admin_disapprove_graphics_super_admin_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("users").document("super_admin").collection("daily_log").document(local_date).get().to_dict()
    assert document.get("count") == 2

def test_super_admin_disapprove_graphics_daily_question_log_super_admin_reviewed(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert document.get("super_admin_reviewed") == 2

'''
Preparing for more tests (Approving 2 questions)
'''

def test_super_admin_question_prepare_1(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "no",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 204

def test_super_admin_question_prepare_2(admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "under_review").where("contributor_id", "==", "contributor").stream():
        document_id = question.id
    json = {
                "graphics_required": "no",
                "feedback": "Testing Admin Approve Question (Graphics Required)",
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = admin_requests.post('/admin-api/approve-question', json=json)
    assert resp.status_code == 204

'''
Super Admin Mark Question as Star
'''

def test_super_admin_star_question(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Mark Questions As Star"
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 204

def test_super_admin_star_question_without_document_id(super_admin_requests, firebase_db_ins):
    json = {
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Mark Questions As Star"
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 400

def test_super_admin_star_question_without_feedback(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 400

def test_super_admin_star_question_without_grade(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Mark Questions As Star"
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 400

def test_super_admin_star_question_without_chapter(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "level": 1,
                "feedback": "Super Admin Mark Questions As Star"
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 400

def test_super_admin_star_question_without_level(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "feedback": "Super Admin Mark Questions As Star"
        }
    resp = super_admin_requests.post('/super-admin-api/star-question', json=json)
    assert resp.status_code == 400

def test_super_admin_star_question_contributor_total_star_question(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("contributor").get().to_dict()
    assert document.get("total_star_questions") == 1

def test_super_admin_star_question_star_question_created(firebase_db_ins):
    star_question_document_id = ""
    for star_question in firebase_db_ins.collection("star_questions").where("contributed_by", "==", "contributor").where("feedback", "==", "Super Admin Mark Questions As Star").stream():
        star_question_document_id = star_question.id
    document = firebase_db_ins.collection("star_questions").document(star_question_document_id).get().to_dict()
    if document:
        assert True
    else:
        assert False

'''
Super Admin Discard Question
'''

def test_super_admin_discard_question(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Discard Question"
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 204

def test_super_admin_discard_question_without_document_id(super_admin_requests, firebase_db_ins):
    json = {
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Discard Question"
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 400

def test_super_admin_discard_question_without_feedback(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 400

def test_super_admin_discard_question_without_grade(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "chapter": 1,
                "level": 1,
                "feedback": "Super Admin Discard Question"
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 400

def test_super_admin_discard_question_without_chapter(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "level": 1,
                "feedback": "Super Admin Discard Question"
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 400

def test_super_admin_discard_question_without_level(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "feedback": "Super Admin Discard Question"
        }
    resp = super_admin_requests.post('/super-admin-api/discard-question', json=json)
    assert resp.status_code == 400

def test_super_admin_discard_question_super_admin_questions_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("super_admin").get().to_dict()
    assert document.get("questions_reviewed") == 3

def test_super_admin_discard_question_super_admin_questions_for_review(firebase_db_ins):
    document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert document.get("NCERT_G03_TOPIC01_LEVEL01") == 1

def test_super_admin_discard_question_super_admin_daily_log(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("users").document("super_admin").collection("daily_log").document(local_date).get().to_dict()
    assert document.get("count") == 3

def test_super_admin_discard_question_daily_question_log_super_admin_reviewed(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert document.get("super_admin_reviewed") == 3

'''
Super Admin Deploy Question
'''

def test_super_admin_deploy_question(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 204

def test_super_admin_deploy_question_without_document_id(super_admin_requests, firebase_db_ins):
    json = {
                "grade": 3,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 400

def test_super_admin_deploy_question_without_grade(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "chapter": 1,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 400

def test_super_admin_deploy_question_without_chapter(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "level": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 400

def test_super_admin_deploy_question_without_level(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "question_json": {
                                    "question": "Testing Question Admin Approve Question (Graphics Required)",
                                    "question_image": "#",
                                    "option_a": "Option A Testing",
                                    "option_b": "Option B Testing",
                                    "option_c": "Option C Testing",
                                    "option_d": "Option D Testing",
                                    "correct_option": "option_c"
                                }
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 400

def test_super_admin_deploy_question_without_question_json(super_admin_requests, firebase_db_ins):
    document_id = ""
    for question in firebase_db_ins.collection("questions").document("G03").collection("levels").document("NCERT_G03_TOPIC01_LEVEL01").collection("question_bank").where("state", "==", "approved").stream():
        document_id = question.id
    json = {
                "document_id": document_id,
                "grade": 3,
                "chapter": 1,
                "level": 1
        }
    resp = super_admin_requests.post('/super-admin-api/deploy-question', json=json)
    assert resp.status_code == 400

def test_super_admin_deploy_question_admin_questions_deployed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("admin").get().to_dict()
    assert document.get("total_questions_deployed") == 1

def test_super_admin_deploy_question_super_admin_questions_deployed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("super_admin").get().to_dict()
    assert document.get("questions_deployed") == 1

def test_super_admin_deploy_question_super_admin_questions_reviewed(firebase_db_ins):
    document = firebase_db_ins.collection("users").document("super_admin").get().to_dict()
    assert document.get("questions_reviewed") == 4

def test_super_admin_deploy_question_super_admin_questions_for_review(firebase_db_ins):
    super_admin_questions_for_review_document = firebase_db_ins.collection("super_admin_questions_for_review").document("NCERT_G03_TOPIC01").get().to_dict()
    assert super_admin_questions_for_review_document.get("NCERT_G03_TOPIC01_LEVEL01") == 0

def test_super_admin_deploy_question_cumulative_super_admin_deployed(firebase_db_ins):
    document = firebase_db_ins.collection("cumulative_data").document("data").get().to_dict()
    assert document.get("super_admin_deployed") == 1

def test_super_admin_deploy_question_super_admin_daily_log_count(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("users").document("super_admin").collection("daily_log").document(local_date).get().to_dict()
    assert document.get("count") == 4

def test_super_admin_deploy_question_daily_question_log_super_admin_reviewed(firebase_db_ins):
    local_date = time.localtime()
    local_date = f"{local_date.tm_mday:02}_{local_date.tm_mon:02}_{local_date.tm_year:04}"
    document = firebase_db_ins.collection("daily_question_log").document(local_date).get().to_dict()
    assert document.get("super_admin_reviewed") == 4