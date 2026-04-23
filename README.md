# Smart-Serverless-automation-pipeline-using-lambda-cloud-project2
Designed an event-driven serverless architecture to process files uploaded to S3 using AWS Lambda.
## Overview
This project implements an event-driven serverless pipeline using AWS services. It automatically processes files uploaded to Amazon S3, validates and analyzes them using AWS Lambda, stores results in DynamoDB, and monitors the system using CloudWatch and SNS alerts.
## Architecture
S3 (uploads/) → Lambda → DynamoDB → CloudWatch → SNS Alerts

## Workflow
1. User uploads a file to S3 under the `uploads/` prefix
2. S3 triggers the Lambda function automatically
3. Lambda processes the file:
   - Text file → word count & line count
   - JSON file → validation + analysis
4. Results are stored in DynamoDB
5. File is moved to:
   - `processed/` → if successful
   - `failed/` → if error occurs
6. Logs are stored in CloudWatch
7. Alerts are sent via SNS if any failure occurs

## AWS Services Used
- Amazon S3 – File storage & event trigger
- AWS Lambda – Serverless compute
- Amazon DynamoDB – NoSQL database
- Amazon CloudWatch – Logs & monitoring
- Amazon SNS – Email notifications
- IAM – Access control

## Features

- Event-driven architecture
- Automated file processing
- JSON validation
- Error handling & failure tracking
- File organization using S3 prefixes
- CloudWatch monitoring
- SNS alerting system
- CI/CD pipeline using GitHub Actions


## Testing Scenarios

| Test Case | Expected Result |
|----------|---------------|
| Valid .txt file | Processed successfully |
| Valid .json file | JSON validated & processed |
| Invalid JSON | Moved to failed/ |
| Unsupported file (.pdf) | Error triggered |
| Large file | Rejected |
| Empty file | Processed with 0 values |


## CI/CD Pipeline

Implemented using GitHub Actions:

### Flow:
VS Code → GitHub Push → GitHub Actions → Upload to S3 → Lambda Trigger → Processing

### Description:
- On every push to the repository, GitHub Actions uploads test files to S3
- This automatically triggers the Lambda function
- Enables continuous and automated pipeline execution


## Outcome

- Built a scalable serverless pipeline
- Automated file processing workflow
- Implemented monitoring and alerting
- Integrated CI/CD for automation
- Improved understanding of AWS event-driven systems


## Future Enhancements

- Implement Infrastructure as Code using Terraform
- Add image processing using Lambda Layers
- Use AWS Step Functions for workflow orchestration
- Integrate API Gateway for external triggering
- Build a dashboard for monitoring processed data
- Add AI-based file analysis using AWS services


## Author
Anil Shetty
