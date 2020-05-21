import requests

def login_user(email, password):
    url = "https://us-central1-pixel-editor-test.cloudfunctions.net/login"
    post_json = {
                "email": email,
                "password": password
            }
    request = requests.post(url, data=post_json)
    breakpoint()
