#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

response = s3.list_buckets()

for bucket in response['Buckets']:
  try:
    enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
    rules = enc['ServerSideEncryptionConfiguration']['Rules']
    print "1"
  except ClientError as e:
    if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
      print "2"
    else:
      print "3"
