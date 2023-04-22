import boto3


def toggle_versioning(s3_client, bucket_name, enable=True) -> bool:
    try:
        # Get the current versioning status for the bucket
        response = s3_client.get_bucket_versioning(Bucket=bucket_name)
        status = response.get('Status')

        # Enable or disable versioning based on the 'enable' argument
        if enable and status != 'Enabled':
            s3_client.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
            print(f"Versioning enabled for bucket '{bucket_name}'")
        elif not enable and status == 'Enabled':
            s3_client.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Suspended'})
            print(f"Versioning suspended for bucket '{bucket_name}'")
        else:
            print(f"Versioning for bucket '{bucket_name}' already {'enabled' if enable else 'suspended'}")

        return True
    except Exception as e:
        print(f"Error toggling versioning for bucket '{bucket_name}': {e}")
        return False

def show_versions(s3_client, bucket_name, object_name, debug = False) -> list:
    versions = []
    response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=object_name)

    for version in response.get("Versions", []):
        data = {"VersionId": version["VersionId"], "LastModified": version["LastModified"]}
        versions.append(data)
        if debug:
            print(data)

    return versions


def rankup_version(s3_client, bucket_name, object_name, version_id) -> bool:
    # Create a new key with the same object data
    response = s3_client.copy_object(
        Bucket=bucket_name,
        Key=object_name,
        CopySource={"Bucket": bucket_name, "Key": object_name, "VersionId": version_id},
        MetadataDirective="COPY",
        TaggingDirective="COPY"
    )

    # Check if the copy operation succeeded
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Delete the old version
        s3_client.delete_object(Bucket=bucket_name, Key=object_name, VersionId=version_id)
        return True
    else:
        return False