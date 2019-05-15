#!/usr/bin/env python

import boto3
import sys
from botocore.exceptions import ClientError

exc_bucket = sys.argv[1]
s3 = boto3.client('s3')

print exc_bucket
response = s3.list_buckets()

for bucket in response['Buckets']:
  try:
    enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
    rules = enc['ServerSideEncryptionConfiguration']['Rules']
    print('Bucket: %s - Status: Encrypted - Encryption: %s' % (bucket['Name'], rules))
  except ClientError as e:
    if (bucket['Name']  == exc_bucket):
      print('Bucket: %s is in Exception List' % (bucket['Name']))
    elif e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
      print('Bucket: %s - Status: No Server-Side Encryption' % (bucket['Name']))
    else:
      print('Bucket: %s - Status: Unexcepted Error %s' % (bucket['Name'], e))
