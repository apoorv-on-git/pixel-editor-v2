from firebase_admin import firestore
import datetime

firebase_db = firestore.client()

def log_error(request_type, platform, error, function):
    log_dict = dict(
                        request_type = request_type,
                        platform = platform,
                        error = error,
                        function = function,
                        logged_at = datetime.datetime.utcnow()
                )
    firebase_db.collection("error_log").document().create(log_dict)