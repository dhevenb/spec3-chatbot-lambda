# Chatbot Lambda Function

This Lambda function handles chatbot requests and integrates with AWS Bedrock for AI-powered responses.

## Features

- Processes user messages through Bedrock knowledge base
- Fallback to direct model invocation if knowledge base is unavailable
- Session management support
- CORS-enabled API responses

## Environment Variables

- `KNOWLEDGE_BASE_ID`: ID of the Bedrock knowledge base
- `MODEL_ARN`: ARN of the Bedrock model to use

## Dependencies

- boto3: AWS SDK for Python
- botocore: Low-level, core functionality of boto3

## Deployment

This function is deployed via AWS CDK as part of the Spec3ChatbotCdkStack. 