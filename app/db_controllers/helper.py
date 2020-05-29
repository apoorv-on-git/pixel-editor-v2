from app.utils.s3 import upload_to_s3
from flask import request
import os

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
