from google.cloud import  storage
import time
import os
import json

storage_client = storage.Client()
bucket_name = "cnd_uploads"
bucket = storage_client.bucket(bucket_name)

def get_list_of_files():
    blobs = storage_client.list_blobs(bucket_name)
    files = []
    for blob in blobs:
        files.append(blob.name.replace("files/",""))
    return files

def upload_file(file_name):
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
    return

def download_json(image_file_name):
    json_file_name = image_file_name.replace(".jpg", ".json").replace(".jpeg", ".json")
    json_blob = bucket.blob(json_file_name)
    json_blob.download_to_filename(json_file_name)
    with open(json_file_name, 'r') as json_file:
        json_content = json_file.read()
        json_data = json.loads(json_content)
    return json_data.get("title"), json_data.get("description")

def download_image(image_file_name):
    image_blob = bucket.blob(image_file_name)
    image_blob.download_to_filename(image_file_name)
