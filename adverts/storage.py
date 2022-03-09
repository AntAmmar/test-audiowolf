from storages.backends.s3boto3 import S3Boto3Storage


class VultrStorage(S3Boto3Storage):
    bucket_name = 'audio-wolf'
