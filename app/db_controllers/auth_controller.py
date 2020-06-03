import requests
import json
import os

def login_firebase_user(email, password):
    url = os.environ.get("CONTRIBUTOR_LOGIN_URL")
    post_json = {
                "email": email,
                "password": password
            }
    request = requests.post(url, data=post_json)
    return json.loads(request.text)
