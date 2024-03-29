from app.data.grade_breakdown import data as grade_breakdown
from app.utils.s3 import *
from flask import request
import os
from random import randint
import bs4

def remove_style(html):
    try:
        soup = bs4.BeautifulSoup(html, features="html.parser")
        for match in soup.findAll('span'):
            match.unwrap()
        for match in soup.findAll('font'):
            match.unwrap()
        for match in soup.findAll('a'):
            match.unwrap()
        for match in soup.findAll('nobr'):
            match.unwrap()
        for match in soup.findAll('img'):
            match.decompose()
        for match in soup.findAll('script'):
            match.decompose()
        for match in soup.findAll('math'):
            match.decompose()
        for tag in soup():
            for attribute in ["class", "id", "name", "style"]:
                del tag[attribute]
        question_text = str(soup)
        question_text = question_text.replace(u'\xa0', u' ')
        return question_text
    except Exception as e:
        raise e

def get_grade_breakdown_dict(grade, chapter, level):
    try:
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
    except Exception as e:
        raise e

def check_data(data):
    try:
        if data.get("correct_option") not in ["option_a", "option_b", "option_c", "option_d"]:
            raise ValueError("Invalid Correct Answer")
        if data.get("correct_option") == "option_" or not all((data.get("question"), data.get("option_a"), data.get("option_b"))):
            raise ValueError("At least 2 options, question and the correct answer is mandatory!")
        option_c = data.get('option_c')
        if not data.get("option_c"):
            option_c = "#"
        option_d = data.get('option_d')
        if not data.get("option_d"):
            option_d = "#"
        if (option_c == "#" and data.get("correct_option") == "option_c") or (option_d == "#" and data.get("correct_option") == "option_d"):
            raise ValueError("Correct Option cannot be left empty!")
    except Exception as e:
        raise e

def handle_submitted_images(data, contributor_id):
    try:
        if not data.get("question_image"):
            data["question_image"] = "#"
        if data.get("question_image") != "#" and 'amazonaws' not in data.get("question_image"):
            question_image = handle_image_upload('question_image', contributor_id)
        elif 'amazonaws' in data.get("question_image"):
            question_image = data.get("question_image")
        else:
            question_image = "#"
        option_a = handle_image_upload('option_a', contributor_id) or data.get('option_a')
        option_b = handle_image_upload('option_b', contributor_id) or data.get('option_b')
        option_c = handle_image_upload('option_c', contributor_id) or data.get('option_c') or "#"
        option_d = handle_image_upload('option_d', contributor_id) or data.get('option_d') or "#"
        return question_image, option_a, option_b, option_c, option_d
    except Exception as e:
        raise e

def get_files_renamed(question_image, option_a, option_b, option_c, option_d):
    try:
        question_image = question_image.split(' ')[-1]
        if "amazonaws" in question_image:
            question_image = rename_image(question_image)
        if "amazonaws" in option_a:
            option_a = rename_image(option_a)
        if "amazonaws" in option_b:
            option_b = rename_image(option_b)
        if "amazonaws" in option_c:
            option_c = rename_image(option_c)
        if "amazonaws" in option_d:
            option_d = rename_image(option_d)
        return question_image, option_a, option_b, option_c, option_d
    except Exception as e:
        raise e

def file_allowed(extension):
    try:
        if extension.lower() not in ["jpg", "jpeg", "png"]:
            raise ValueError("Only JPG, JPEG and PNG images allowed!")
        return True
    except Exception as e:
        raise e

def handle_image_upload(key, contributor_id):
    try:
        image = request.files.get(key)
        if image and file_allowed(image.filename.split('.')[-1].lower()):
            if key == 'question_image':
                url_endpoint = f"preview_images/{contributor_id}_preview.{image.filename.split('.')[-1].lower()}"
                upload_to_s3(url_endpoint, image)
                return f"{os.environ.get('S3_URL')}{url_endpoint}"
            elif key == 'option_a':
                url_endpoint = f"preview_images/{contributor_id}_preview_OPTION_A.{image.filename.split('.')[-1].lower()}"
                upload_to_s3(url_endpoint, image)
                return f"{os.environ.get('S3_URL')}{url_endpoint}"
            elif key == 'option_b':
                url_endpoint = f"preview_images/{contributor_id}_preview_OPTION_B.{image.filename.split('.')[-1].lower()}"
                upload_to_s3(url_endpoint, image)
                return f"{os.environ.get('S3_URL')}{url_endpoint}"
            elif key == 'option_c':
                url_endpoint = f"preview_images/{contributor_id}_preview_OPTION_C.{image.filename.split('.')[-1].lower()}"
                upload_to_s3(url_endpoint, image)
                return f"{os.environ.get('S3_URL')}{url_endpoint}"
            elif key == 'option_d':
                url_endpoint = f"preview_images/{contributor_id}_preview_OPTION_D.{image.filename.split('.')[-1].lower()}"
                upload_to_s3(url_endpoint, image)
                return f"{os.environ.get('S3_URL')}{url_endpoint}"
    except Exception as e:
        raise e

def get_total_images_uploaded():
    try:
        counter = 0
        if request.files.get("question_image"):
            counter += 1
        if request.files.get("option_a"):
            counter += 1
        if request.files.get("option_b"):
            counter += 1
        if request.files.get("option_c"):
            counter += 1
        if request.files.get("option_d"):
            counter += 1
        return counter
    except Exception as e:
        raise e

def delete_question_image(old_image):
    try:
        url_endpoint = old_image.split("amazonaws.com/")[-1]
        delete_from_s3(url_endpoint)
    except Exception as e:
        raise e
