# Lambda Functions for Spec3 Chatbot

This directory contains the AWS Lambda functions used by the Spec3 Chatbot CDK stack.

## Structure

```
lambda-functions/
├── chatbot-lambda/           # Main chatbot processing function
│   ├── index.py
│   ├── requirements.txt
│   └── README.md
├── knowledge-base-lambda/    # Knowledge base management function
│   ├── index.py
│   ├── requirements.txt
│   └── README.md
├── health-check-lambda/      # Health check endpoint function
│   ├── index.py
│   ├── requirements.txt
│   └── README.md
└── README.md                 # This file
```

## Functions Overview

### 1. Chatbot Lambda (`chatbot-lambda/`)
- **Purpose**: Processes user messages and generates AI responses
- **Features**: 
  - Integration with AWS Bedrock knowledge base
  - Fallback to direct model invocation
  - Session management
  - CORS support

### 2. Knowledge Base Lambda (`knowledge-base-lambda/`)
- **Purpose**: Manages AWS Bedrock knowledge bases
- **Features**:
  - Create new knowledge bases
  - Add documents to knowledge bases
  - List existing knowledge bases
  - Vector-based configuration

### 3. Health Check Lambda (`health-check-lambda/`)
- **Purpose**: Provides health check endpoint for API monitoring
- **Features**:
  - Simple status response
  - CORS support
  - No external dependencies

## Development

Each Lambda function is a self-contained package with its own:
- Python source code (`index.py`)
- Dependencies (`requirements.txt`)
- Documentation (`README.md`)

## Deployment

These functions are deployed via AWS CDK as part of the `Spec3ChatbotCdkStack`. The CDK stack references these directories using `lambda.Code.fromAsset()`.

## Local Testing

To test these functions locally, you can:

1. Install dependencies:
   ```bash
   cd lambda-functions/chatbot-lambda
   pip install -r requirements.txt
   ```

2. Run the function locally (example for chatbot):
   ```python
   import json
   from index import handler
   
   event = {
       'body': json.dumps({
           'message': 'Hello, how are you?',
           'session_id': 'test-session'
       })
   }
   
   response = handler(event, None)
   print(response)
   ```

## Environment Variables

Each function has specific environment variables that need to be configured in the CDK stack:

- **Chatbot Lambda**: `KNOWLEDGE_BASE_ID`, `MODEL_ARN`
- **Knowledge Base Lambda**: `BEDROCK_ROLE_ARN`
- **Health Check Lambda**: None required 