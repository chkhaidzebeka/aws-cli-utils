import json


def generate_public_read_policy(bucket_name):
  policy = {
    "Version":
    "2012-10-17",
    "Statement": [{
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": f"arn:aws:s3:::{bucket_name}/*",
    }],
  }

  return json.dumps(policy)


def generate_multiple_policy(bucket_name):
  policy = {
    "Version":
    "2012-10-17",
    "Statement": [{
      "Action": [
        "s3:PutObject", "s3:PutObjectAcl", "s3:GetObject", "s3:GetObjectAcl",
        "s3:DeleteObject"
      ],
      "Resource":
      [f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*"],
      "Effect":
      "Allow",
      "Principal":
      "*"
    }]
  }

  return json.dumps(policy)


def assign_policy(aws_s3_client, policy_function, bucket_name):
  policy = None
  if policy_function == "public_read_policy":
    policy = generate_public_read_policy(bucket_name)
  elif policy_function == "multiple_policy":
    policy = generate_multiple_policy(bucket_name)

  if (not policy):
    print('please provide policy')
    return

  aws_s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
  print("Bucket policy assigned successfully")


def read_bucket_policy(aws_s3_client, bucket_name):
  policy = aws_s3_client.get_bucket_policy(Bucket=bucket_name)

  status_code = policy["ResponseMetadata"]["HTTPStatusCode"]
  if status_code == 200:
    return policy["Policy"]
  return False

def put_bucket_lifecycle_configuration(aws_s3_client):
  lfc = {
    "Rules": [{
      "Expiration": {"Days": 120},
      "ID": "devobjects",
      "Filter": {"Prefix": "dev"},
      "Status": "Enabled",
    }]
  }

  aws_s3_client.put_bucket_lifecycle_configuration(
    Bucket="bucket",
    LifecycleConfiguration=lfc
  )

def reset_to_default_policy(s3_client, bucket_name) -> bool:
    try:
        s3_client.delete_bucket_policy(Bucket=bucket_name)
        return True
    except Exception as e:
        print(e)
        return False