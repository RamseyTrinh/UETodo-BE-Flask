import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from flask import current_app as app


def upload_image_to_s3(file, folder="avatars"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
        region_name=app.config["AWS_REGION"],
    )
    filename = f"{folder}/{uuid.uuid4().hex}_{file.filename}"
    try:
        s3.upload_fileobj(
            file,
            app.config["AWS_S3_BUCKET_NAME"],
            filename,
            ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
        )
        return f"https://{app.config['AWS_S3_BUCKET_NAME']}.s3.{app.config['AWS_REGION']}.amazonaws.com/{filename}"
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not found")
