import boto3
from os import getenv
import logging
from botocore.exceptions import ClientError

def list_buckets(aws_s3_client, verbose = False) -> list:
    buckets = aws_s3_client.list_buckets()['Buckets']

    if verbose:
        for index, bucket in enumerate(buckets):
            print(f'Bucket #{index + 1}: {bucket["Name"]}')

    return buckets


def bucket_exists(aws_s3_client, bucket_name) -> bool:
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
    except ClientError:
        return False

def create_bucket(aws_s3_client, bucket_name, region = getenv("aws_region_name")) -> bool:
    exists = bucket_exists(aws_s3_client, bucket_name)

    if exists:
        logging.error(f'{bucket_name} already exists')
        return False
    
    if region == 'us-east-1':
        response = aws_s3_client.create_bucket(
            Bucket=bucket_name,
        )
    else:
        response = aws_s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def delete_bucket(aws_s3_client, bucket_name) -> bool:
    try:
        # Delete all objects in the bucket
        response = aws_s3_client.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        while objects:
            delete_keys = [{'Key': obj['Key']} for obj in objects]
            aws_s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})
            response = aws_s3_client.list_objects_v2(Bucket=bucket_name)
            objects = response.get('Contents', [])
            
        # Delete the bucket
        response = aws_s3_client.delete_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 204:
            return True
        return False
        
    except aws_s3_client.exceptions.NoSuchBucket:
        # The bucket doesn't exist, so it can be considered deleted
        return True


def delete_object(s3_client, bucket_name, object_name) -> bool:
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        return True
    except Exception as e:
        print(f"Error deleting object '{object_name}' from bucket '{bucket_name}': {e}")
        return False

def list_bucket_objects(s3_client, bucket_name, debug = False) -> list:
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if "Contents" not in response:
        return []

    objects = response["Contents"]

    while response["IsTruncated"]:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            ContinuationToken=response["NextContinuationToken"],
        )
        objects.extend(response["Contents"])

    if debug:
        for obj in objects:
            print(obj["Key"])
    return objects