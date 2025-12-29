import base64
import io
import tempfile
import time
from datetime import timedelta

import PyPDF2
from fastapi import UploadFile
from google.cloud import storage

from app.config.config import GCS_BUCKET_NAME


async def stream_pdf_to_gcs(user_id, document_id, file: UploadFile):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    destination_blob_name = f"{user_id}/{document_id}/{file.filename}"

    blob = bucket.blob(destination_blob_name)

    # Upload in chunks (streaming)
    with blob.open("wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1MB at a time
            f.write(chunk)

    return destination_blob_name


def upload_pdf_to_gcs(user_id, document_id, file_path):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        destination_blob_name = f"{user_id}/{document_id}/{str(time.time())}.pdf"

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        print(f"Uploaded {file_path} to gs://{GCS_BUCKET_NAME}/{destination_blob_name}")
        return destination_blob_name
    except Exception as e:
        print(f"Failed to upload to GCS: {e}")
        return None


def upload_base64_to_gcs(user_id, document_id, image_id, base64_string):
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    destination_blob_name = f"{user_id}/{document_id}/{image_id}"
    base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)

    image_file = io.BytesIO(image_bytes)

    content_type = "image/jpeg"

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(image_file, content_type=content_type)

    return blob.public_url


def upload_md_to_gcs(user_id, document_id, text):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    destination_blob_name = f"{user_id}/{document_id}/{str(time.time())}.md"

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(text, content_type="text/markdown")
    return destination_blob_name


def upload_txt_to_gcs(user_id, document_id, text):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    destination_blob_name = f"{user_id}/{document_id}/{str(time.time())}.txt"

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(text)
    return destination_blob_name


def upload_markdown_to_gcs(user_id, document_id, text):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    destination_blob_name = f"{user_id}/{document_id}/{str(time.time())}.md"

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(text, content_type="text/markdown")
    return destination_blob_name


def generate_signed_url(blob_name, expiration_minutes=60):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )

    return url


def get_content(blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)
    content = blob.download_as_text()

    return content


def get_files(user_id, document_id):
    prefix = f"{user_id}/{document_id}/"
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=prefix)

    return [blob.name for blob in blobs]


def generate_md_from_gcs_pdf(user_id, document_id, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    text = ""
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        # Download PDF from GCS into the temp file
        blob.download_to_file(tmp)
        tmp.flush()

        # Extract text using PyPDF2
        with open(tmp.name, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for i, page in enumerate(reader.pages):
                text += f"\n\n### Page {i + 1}\n\n"
                text += page.extract_text() or ""

    destination_blob_name = upload_txt_to_gcs(user_id, document_id, text)
    return destination_blob_name


def generate_md_text_from_gcs_pdf(user_id, document_id, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    first_two_pages_text = ""
    text = ""
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        # Download PDF from GCS into the temp file
        blob.download_to_file(tmp)
        tmp.flush()

        # Extract text using PyPDF2
        with open(tmp.name, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for i, page in enumerate(reader.pages):
                if i >= 2:
                    break
                first_two_pages_text += page.extract_text() + "\n"

            for i, page in enumerate(reader.pages):
                text += f"\n\n### Page {i + 1}\n\n"
                text += page.extract_text() or ""

    destination_blob_name = upload_markdown_to_gcs(user_id, document_id, text)
    return destination_blob_name, first_two_pages_text
