from firebase_admin import firestore
import urllib.request
import requests
import json
import ssl
import os

def firebase_get_questions_student_reported():
    response = requests.get(os.environ.get('STUDENT_REPORTED_GET_URL'))
    data = response.json().get("data")
    final_list = []
    for data_obj in data:
        if not data_obj.get("graphics_issue"):
            final_list.append(data_obj)
    return data

def firebase_get_questions_teacher_reported():
    response = requests.get(os.environ.get('TEACHER_REPORTED_GET_URL'))
    data = response.json().get("data")
    final_list = []
    for data_obj in data:
        if not data_obj.get("graphics_issue"):
            final_list.append(data_obj)
    return data

def firebase_get_question_from_main(document_id):
    grade = int(document_id.split("NCERT_G")[1].split("_")[0])
    if "TOPIC" in document_id:
        chapter = int(document_id.split("_TOPIC")[1].split("_")[0])
        chapter_var = "TOPIC"
    elif "CONTEST" in document_id:
        chapter = int(document_id.split("_CONTEST")[1].split("_")[0])
        chapter_var = "CONTEST"
    else:
        raise ValueError("Invalid question ID")
    level = int(document_id.split("_LEVEL")[1].split("_")[0])
    data = {
                "question_id": document_id
        }
    url = os.environ.get("GET_QUESTION_FROM_MAIN")
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    response_data = response.read()
    response_data = response_data.decode('utf8').replace("'", '"')
    response_data = json.loads(response_data)
    return response_data, grade, chapter, level
