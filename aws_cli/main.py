from auth import init_client
from bucket.crud import *
from bucket.versioning import *
from bucket.policy import *

def main():
    s3 = init_client()
    bucket_name = "something-very-very-random"
    
    # list = list_buckets(s3)
    # exists = bucket_exists(s3, "demo-static-site")
    # create_bucket(s3, bucket_name)

    # for bucket in list:
    #     print(f'delete {bucket["Name"]}')
    #     delete_bucket(s3,bucket["Name"])


    # create_bucket(s3, bucket_name)
    # delete_object(s3, bucket_name, "test.txt")
    # toggle_versioning(s3, bucket_name)
    # show_versions(s3, bucket_name, "test.txt", True)
    # rankup_version(s3, bucket_name, "test.txt", "x7mweC7dI1PXCSUBi61wKuJmcRDjwylq")
    # list_bucket_objects(s3, bucket_name)
    # assign_policy(s3, "public_read_policy", bucket_name)
    # reset_to_default_policy(s3, bucket_name)

if __name__ == '__main__':
    main()