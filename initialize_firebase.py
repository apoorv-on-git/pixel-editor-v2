from firebase_admin import credentials, initialize_app, firestore
from app.key import cred_json

if __name__ == "__main__":
    cred = credentials.Certificate(cred_json)
    db_app = initialize_app(cred)
    db = firestore.client()
