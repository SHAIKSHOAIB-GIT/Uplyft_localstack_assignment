import boto3
import pandas as pd
import json
import os

def lambda_handler(event, context):
    s3 = boto3.client("s3", endpoint_url="http://localhost:4566")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Download CSV file
    local_file = "/tmp/" + file_key
    s3.download_file(bucket_name, file_key, local_file)

    # Read CSV and extract metadata
    df = pd.read_csv(local_file)
    metadata = {
        "filename": file_key,
        "row_count": df.shape[0],
        "column_count": df.shape[1],
        "column_names": list(df.columns)
    }

    print("Extracted Metadata:", json.dumps(metadata, indent=2))
    return {"statusCode": 200, "body": json.dumps(metadata)}
