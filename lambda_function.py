import boto3
import pandas as pd
import json
from datetime import datetime

# Initialize LocalStack clients
s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")
table = dynamodb.Table("MetadataTable")

def lambda_handler(event, context):
    try:
        # Extract S3 event details
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        # Fetch the CSV file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_size = response['ContentLength']
        csv_data = response['Body'].read().decode('utf-8')

        # Process CSV using Pandas
        df = pd.read_csv(pd.compat.StringIO(csv_data))
        row_count, column_count = df.shape
        column_names = df.columns.tolist()

        # Store metadata in DynamoDB
        metadata = {
            'filename': file_key,
            'upload_timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': file_size,
            'row_count': row_count,
            'column_count': column_count,
            'column_names': column_names
        }

        table.put_item(Item=metadata)
        return {"statusCode": 200, "body": json.dumps(metadata)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
