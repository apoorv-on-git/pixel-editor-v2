import boto3
import os
import uuid

def upload_to_s3(file_name, file):
    s3 = boto3.resource('s3')
    s3.Bucket(os.environ.get('S3_BUCKET_NAME')).put_object(Key=file_name, Body=file, ACL='public-read')

def delete_from_s3(file_name):
    s3 = boto3.resource('s3')
    s3.Object(os.environ.get('S3_BUCKET_NAME'), file_name).delete()

def rename_image(file_name):
    s3 = boto3.resource('s3')
    unique_id = str(uuid.uuid4())
    new_file_name = f"images/{unique_id}.{file_name.split('.')[-1].split('?')[0].lower()}"
    copy_source = {
                        'Bucket': os.environ.get('S3_BUCKET_NAME'),
                        'Key': f"{file_name.split('amazonaws.com/')[-1].split('.')[0]}.{file_name.split('amazonaws.com/')[-1].split('.')[-1].split('?')[0].lower()}"
                }
    s3.meta.client.copy(copy_source, os.environ.get('S3_BUCKET_NAME'), new_file_name)
    s3.Object(os.environ.get('S3_BUCKET_NAME'), f"{file_name.split('amazonaws.com/')[-1].split('?')[0]}").delete()
    return f"{os.environ.get('S3_URL')}{new_file_name}"
