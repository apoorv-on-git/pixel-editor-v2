import requests
from firebase_admin import firestore

firebase_db = firestore.client()

def get_user_document_data(document_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(document_id).get()
    return user_data.to_dict()

def firebase_update_profile_image(document_id, profile_image_url):
    document_ref = firebase_db.collection('users')
    update_user = document_ref.document(document_id).update({"profile_image": profile_image_url})

def get_leaderboard_data(document_id):
    document_ref = firebase_db.collection('users')
    user_data = document_ref.document(document_id).get()
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
