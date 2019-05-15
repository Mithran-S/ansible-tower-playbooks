#!/usr/bin/env python
import boto3
import sys
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:

  try:
    getEncryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
    encryptionType = getEncryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
    print('Bucket: %s - Status: Encrypted - %s' % (bucket['Name'], encryptionType))

  except ClientError as e:
    if any(bucket['Name'] in exceptionList for exceptionList in sys.argv):
      print('Bucket: %s defined in Exception List' % (bucket['Name']))
    elif e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
      print('Bucket: %s - Status: No Server-Side Encryption' % (bucket['Name']))
    else:
      print('Bucket: %s - Status: Unexcepted Error %s' % (bucket['Name'], e))
