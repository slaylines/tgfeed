import boto3, botocore
from botocore.client import Config

class Storage:
  def __init__(self, config):
    self.bucket = config['bucket']
    self.client = boto3.client('s3')
    self.resource = boto3.resource('s3',
                                   endpoint_url=config['endpoint'],
                                   aws_access_key_id=config['access_key'],
                                   aws_secret_access_key=config['secret_key'],
                                   config=Config(signature_version='s3v4'),
                                   region_name=config['region'])
    self.create_bucket(config['bucket'], config['region'])

  def create_bucket(self, name, region):
    try:
      self.resource.create_bucket(Bucket=name,
                                  CreateBucketConfiguration={'LocationConstraint': region})
    except self.client.exceptions.BucketAlreadyOwnedByYou:
      pass

  def upload_file(self, path, name):
    self.resource.Bucket(self.bucket).upload_file(path, name)
