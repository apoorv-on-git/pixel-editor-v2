from app.data.grade_breakdown import data as grade_breakdown
from app.utils.s3 import *
from flask import request
import os

def get_grade_breakdown_dict(grade, chapter, level):
    grade_dict = next((grade_dict for grade_dict in grade_breakdown if grade_dict.get('grade_number') == int(grade)), None)
    if not grade_dict:
        raise ValueError("Invalid Grade!")
    chapter_dict = next((chapter_dict for chapter_dict in grade_dict.get("chapters") if chapter_dict.get('chapter_number') == int(chapter)), None)
    if not chapter_dict:
        raise ValueError("Invalid Chapter!")
    level_dict = next((level_dict for level_dict in chapter_dict.get("levels") if level_dict.get('level_number') == int(level)), None)
    if not level_dict:
        raise ValueError("Invalid Level!")
    return grade_dict, chapter_dict, level_dict

def file_allowed(extension):
    if extension.lower() not in ["jpg", "jpeg", "png"]:
        raise ValueError("Only JPG, JPEG and PNG images allowed!")
    return True

def handle_image_upload(key, document_id):
    image = request.files.get(key)
    if image and file_allowed(image.filename.split('.')[-1]):
        if key == 'question_image':
            url_endpoint = f"images/{document_id}_preview.{image.filename.split('.')[-1]}"
            upload_to_s3(url_endpoint, image)
            return f"{os.environ.get('S3_URL')}{url_endpoint}"
        elif key == 'option_a':
            url_endpoint = f"images/{document_id}_preview_OPTION_A.{image.filename.split('.')[-1]}"
            upload_to_s3(url_endpoint, image)
            return f"{os.environ.get('S3_URL')}{url_endpoint}"
        elif key == 'option_b':
            url_endpoint = f"images/{document_id}_preview_OPTION_B.{image.filename.split('.')[-1]}"
            upload_to_s3(url_endpoint, image)
            return f"{os.environ.get('S3_URL')}{url_endpoint}"
        elif key == 'option_c':
            url_endpoint = f"images/{document_id}_preview_OPTION_C.{image.filename.split('.')[-1]}"
            upload_to_s3(url_endpoint, image)
            return f"{os.environ.get('S3_URL')}{url_endpoint}"
        elif key == 'option_d':
            url_endpoint = f"images/{document_id}_preview_OPTION_D.{image.filename.split('.')[-1]}"
            upload_to_s3(url_endpoint, image)
            return f"{os.environ.get('S3_URL')}{url_endpoint}"
