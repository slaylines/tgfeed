import magic
import mimetypes
import boto3, botocore
from botocore.client import Config

class S3Storage:
  def __init__(self, config):
    self.bucket_name = config['bucket']
    self.client = boto3.client('s3', **self._s3_options(config))
    self.resource = boto3.resource('s3', **self._s3_options(config))
    self.create_bucket(config['bucket'], config['region'])

  def bucket(self):
    return self.resource.Bucket(self.bucket_name)

  def create_bucket(self, name, region):
    try:
      self.resource.create_bucket(Bucket=name,
                                  CreateBucketConfiguration={'LocationConstraint': region})
    except self.client.exceptions.BucketAlreadyOwnedByYou:
      pass

  def upload_fileobj(self, fileobj, name):
    fileobj.seek(0)
    self.bucket().upload_fileobj(fileobj, name)

    return '/%s/%s' % (self.bucket_name, name)

  def _s3_options(self, config):
    return {'endpoint_url': config['endpoint'],
            'aws_access_key_id': config['access_key'],
            'aws_secret_access_key': config['secret_key'],
            'config': Config(signature_version='s3v4'),
            'region_name': config['region']}
