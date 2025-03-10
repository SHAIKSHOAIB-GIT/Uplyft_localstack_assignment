# LocalStack CSV Processing Assignment

## 📌 Project Overview
This project sets up a **local AWS cloud-based system** using LocalStack to process CSV files. The system includes:
- **S3 bucket** to store CSV files
- **AWS Lambda function** to process the files
- **DynamoDB or RDS** to store metadata

## 📂 Project Structure
```
|-- lambda_function/
|   |-- lambda_function.py  # Lambda function code
|   |-- requirements.txt    # Dependencies for Lambda
|
|-- iam-policy.json        # IAM policy for Lambda execution
|-- commands.sh            # CLI commands to set up the project
|-- README.md              # Documentation
```

## 🔧 Prerequisites
Before running the project, ensure you have:
- **Python 3.8+** installed
- **AWS CLI** installed (`aws --version` to check)
- **LocalStack** installed (`localstack --version` to check)
- **AWS CLI Local** installed (`pip install awscli-local`)
- **Docker** running in the background (for LocalStack services)

## 🚀 Setup Instructions
### 1️⃣ Start LocalStack
Run the following command to start LocalStack with required services:
```sh
SERVICES=s3,lambda,iam,logs dynamodb localstack start
```

### 2️⃣ Create IAM Role for Lambda
```sh
awslocal iam create-role --role-name lambda-role --assume-role-policy-document file://iam-policy.json
```

### 3️⃣ Create an S3 Bucket
```sh
awslocal s3 mb s3://my-bucket
```

### 4️⃣ Deploy the Lambda Function
```sh
zip lambda_function.zip lambda_function.py
awslocal lambda create-function \
  --function-name ProcessCSV \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip
```

### 5️⃣ Set Up S3 Event Trigger
```sh
awslocal s3api put-bucket-notification-configuration --bucket my-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [
      {
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:ProcessCSV",
        "Events": ["s3:ObjectCreated:*"]
      }
    ]
  }'
```

### 6️⃣ Upload a CSV File
```sh
awslocal s3 cp sample.csv s3://my-bucket/
```

### 7️⃣ Check Lambda Logs
```sh
awslocal logs describe-log-streams --log-group-name "/aws/lambda/ProcessCSV"
```

## 📜 Expected Output
When a CSV file is uploaded to **S3**, Lambda processes it and stores metadata in DynamoDB or RDS. Example metadata:
```json
{
  "filename": "example.csv",
  "upload_timestamp": "2024-12-14 10:00:00",
  "file_size_bytes": 1048576,
  "row_count": 1000,
  "column_count": 5,
  "column_names": ["id", "name", "age", "city", "date"]
}
```

## 🛠️ Troubleshooting
- **LocalStack not starting?** Check if Docker is running.
- **IAM role issues?** Ensure `iam-policy.json` is correctly formatted.
- **Lambda not triggering?** Check `awslocal logs` for errors.

---
✅ **Assignment Complete!** Submit your project by pushing it to GitHub:
```sh
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_GITHUB/Uplyft_localstack_assignment.git
git push -u origin main
```

