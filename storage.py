from google.cloud import datastore, storage
import time

datastore_client = datastore.Client()
storage_client = storage.Client()

def list_db_entries():
    query = datastore_client.query(kind="photos")

    for photo in query.fetch():
        print(photo.items())

def add_db_entry(object):
    entity = datastore.Entity(key=datastore_client.key('photos'))
    entity.update(object)

    datastore_client.put(entity)


def fetch_db_entry(object):

    query = datastore_client.query(kind='photos')

    for attr in object.keys():
        query.add_filter(attr, "=", object[attr])

    obj = list(query.fetch())
    return obj

def get_list_of_files(bucket_name):
    """Lists all the blobs in the bucket."""

    blobs = storage_client.list_blobs(bucket_name)
    files = []
    for blob in blobs:
        files.append(blob.name)

    return files

def upload_file(bucket_name, file_name):

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    return blob.public_url

def download_file(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.download_to_filename(file_name)
    blob.reload()
    return
