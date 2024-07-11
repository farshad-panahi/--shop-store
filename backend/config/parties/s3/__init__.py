
from decouple import config as E
from storages.backends.s3boto3 import S3Boto3Storage
from decouple import config  




class Liara(S3Boto3Storage):
    def __init__(self, **settings):
        super().__init__( **settings)

        self.bucket_name      = config('S3_BUCKET')
        self.endpoint_url     = config('S3_ENDPOINT')
        self.access_key       = config('S3_ACCESS_KEY')
        self.secret_key       = config('S3_SECRET_KEY')
        self.querystring_auth =  False


LIARA_STORAGE = Liara

