import os
import tempfile
import zipfile

import nltk
from google.cloud.storage import Client

#####


def main(storage_client: Client, bucket_name: str = "") -> None:
    """
    Uploads the NLTK vader_lexicon data to a specified Google Cloud Storage bucket.

    Args:
        storage_client (Client, optional): An instance of Google Cloud Storage Client.
            If not provided, a new client will be created.

    """

    # Specify your bucket name
    print(f"Uploading NTLK vader_lexicon to GCS [bucket={bucket_name}]...")
    bucket = storage_client.bucket(bucket_name)

    # Download NLTK data
    print("Downloading NLTK vader_lexicon...")
    nltk.download("vader_lexicon", quiet=True)

    # Get the zip file path
    zip_path = str(nltk.data.find("sentiment/vader_lexicon.zip"))

    # Extract vader_lexicon.txt from the zip
    print("Extracting vader_lexicon.txt from zip...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # The text file is inside vader_lexicon/ folder in the zip
        with zip_ref.open("vader_lexicon/vader_lexicon.txt") as txt_file:
            txt_content = txt_file.read()

    # Write to a temp file and upload
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp_file:
        temp_file.write(txt_content)
        temp_path = temp_file.name

    try:
        print("Uploading vader_lexicon.txt to GCS...")
        blob = bucket.blob("vader_lexicon.txt")
        blob.upload_from_filename(temp_path)
        print(f"✓ Uploaded to gs://{bucket_name}/vader_lexicon.txt")
    finally:
        os.unlink(temp_path)


#####

if __name__ == "__main__":
    storage_client = Client()

    # NOTE: This is centrally managed in Terraform
    bucket_name = "whiskey-ml-dataproc-staging-bucket"

    main(storage_client=storage_client, bucket_name=bucket_name)
