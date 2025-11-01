import boto3
import logging
from io import BytesIO
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level (DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = "tester"
AWS_SECRET_ACCESS_KEY = "test"
S3_BUCKET_NAME = "my-new-bucket"
LOCALSTACK_HOST = "http://localhost:4566"  # Default LocalStack endpoint


def upload_to_s3(file_bytes, filename, mimetype, object_name=None):
    """
    Uploads a file to an S3 bucket

    :param file_bytes: Bytes object of the file to be uploaded
    :param filename: Name of the file
    :param mimetype: MIME type of the file
    :param object_name: Name of the object in the bucket

    :return: True if the file was uploaded, else False
    """

    s3_client = create_S3_client()

    if object_name is None:
        object_name = filename

    try:
        # Wrap the bytes object in a BytesIO object
        file_obj = BytesIO(file_bytes)

        # Upload the file object to S3 bucket
        response = s3_client.upload_fileobj(
            file_obj, S3_BUCKET_NAME, object_name, ExtraArgs={"ContentType": mimetype}
        )
        logger.info(f"{object_name} uploaded to {S3_BUCKET_NAME} bucket")
        logger.info(response)
        return True
    except ClientError as e:
        logger.error(e)
        logger.exception(e)
        return False


def create_S3_client():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=LOCALSTACK_HOST,  # Point to LocalStack endpoint
    )
    return s3_client


def read_file():
    file_bytes = None
    filename = None
    mimetype = None
    with open("file.pdf", "rb") as file:
        file_bytes = file.read()
        filename = f"images/{file.name}"
        mimetype = "application/pdf"

    return file_bytes, filename, mimetype


def main():
    file_bytes, filename, mimetype = read_file()

    status = upload_to_s3(file_bytes, filename, mimetype)

    if status:
        logger.info("File uploaded successfully!")
    else:
        logger.error("File upload failed.")


if __name__ == "__main__":
    main()