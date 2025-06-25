# Knowledge Base Lambda Function

This Lambda function manages AWS Bedrock knowledge bases for the Spec3 Chatbot.

## Features

- Create new knowledge bases
- Add documents to knowledge bases
- List existing knowledge bases
- Vector-based knowledge base configuration

## Environment Variables

- `BEDROCK_ROLE_ARN`: ARN of the IAM role for Bedrock operations

## Dependencies

- boto3: AWS SDK for Python
- botocore: Low-level, core functionality of boto3

## Operations

- `create_knowledge_base`: Creates a new knowledge base
- `add_document`: Adds a document to an existing knowledge base
- `list_knowledge_bases`: Lists all available knowledge bases

## Deployment

This function is deployed via AWS CDK as part of the Spec3ChatbotCdkStack. 