import boto3
from botocore.exceptions import ClientError
from botocore.client import Config


class AWSS3:
    """
    This class is used to:
        1. upload file from local to AWS S3 bucket using access key, secret key and bucket name
        2. generate presigned URL for file in AWS S3 bucket using access key, secret key and bucket name
        3. download file from AWS S3 bucket using S3 presigned URL and save it to local
    """

    def __init__(self, config: dict):
        """
        This function is used to initialize AWS S3 client
        :param aws_access_key_id: AWS access key ID
        :param aws_secret_access_key: AWS secret access key
        :param bucket_name: AWS S3 bucket name
        """
        self.aws_access_key_id = config['aws_access_key_id']
        self.aws_secret_access_key = config['aws_secret_access_key']
        self.bucket_name = config['bucket_name']
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key,
                                      config=Config(signature_version='s3v4'))

    def upload(self, file_name):
        """
        This function is used to upload file from local to AWS S3 bucket
        :param file_path: file path on local
        :param file_name: file name on local
        :return: True if file is uploaded successfully, otherwise False
        """
        try:
            self.s3_client.upload_file("", self.bucket_name, file_name)
            return True
        except ClientError as e:
            print(e)
            return False

    def get_signed_url(self, file_name, expiration=3600):
        """
        This function is used to generate presigned URL for file in AWS S3 bucket
        :param file_name: file name in AWS S3 bucket
        :param expiration: expiration time of presigned URL, default is 3600 seconds
        :return: presigned URL for file in AWS S3 bucket
        """
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': self.bucket_name,
                                                                     'Key': file_name},
                                                             ExpiresIn=expiration)
            return response
        except ClientError as e:
            print(e)
            return None

    def delete_file(self, file_name):
        """
        This function is used to delete file from AWS S3 bucket
        :param file_name: file name in AWS S3 bucket
        :return: True if file is deleted successfully, otherwise False
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)
            return True
        except ClientError as e:
            print(e)
            return False

