from botocore.exceptions import ClientError
import os
import boto3
import traceback
import os.path
from pathlib import Path


def extract_file_name(path):
    file_name = path.split("/")[-1]
    return file_name


def extract_identifier(path_name):
    path_name = path_name.split('_')[1]
    return path_name


def compose_local_file(s3_path_filename):
    filename = extract_file_name(s3_path_filename)
    return './tmp/' + extract_identifier(filename) + '/' + filename


RECORDINGS_BUCKET_NAME = '<REPLACE WITH S3 BUCKET>'

class Downloader:
    def __init__(self, comparisons):
        self.comparisons = comparisons
    def _download_file(self, file_s3_path):
        os.environ["AWS_DEFAULT_REGION"] = '<REPLACE_WITH_REGION>'
        os.environ["AWS_ACCESS_KEY_ID"] = '<REPLACE WITH ACCESS_KEY_ID THAT HAS ACCESS TO THE ABOVE BUCKET>'
        os.environ["AWS_SECRET_ACCESS_KEY"] = '<REPLACE WITH SECRET_ACCESS_KEY>'
        s3 = boto3.client('s3')
        identifier = extract_identifier(extract_file_name(file_s3_path))
        source_file_to_download = './tmp/' + identifier + '/' + extract_file_name(file_s3_path)
        if not os.path.isfile(source_file_to_download):
            filename = Path(source_file_to_download)
            filename.parent.mkdir(parents=True, exist_ok=True)
            with open(source_file_to_download, 'wb+') as source_file:
                s3.download_fileobj(RECORDINGS_BUCKET_NAME, file_s3_path, source_file)

    def download_video_files(self):
        for comparison in self.comparisons:
            try:
                self._download_file(comparison.source_file_s3_path)
                self._download_file(comparison.encoded_file_s3_path)
            except ClientError as e:
                print("Error downloading: " + comparison.source_file_s3_path + ", " + comparison.encoded_file_s3_path)
                traceback.print_exc(e)