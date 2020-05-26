import boto3
import os

def upload_to_s3(file_name, file):
    s3 = boto3.resource('s3')
    s3.Bucket(os.environ.get('S3_BUCKET_NAME')).put_object(Key=file_name, Body=file, ACL='public-read')

def delete_from_s3(file_name):
    s3 = boto3.resource('s3')
    s3.Object(os.environ.get('S3_BUCKET_NAME'), file_name).delete()
