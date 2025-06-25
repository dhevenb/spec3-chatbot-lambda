# Health Check Lambda Function

This Lambda function provides a simple health check endpoint for the Spec3 Chatbot API.

## Features

- Returns a simple health status response
- CORS-enabled API responses
- No external dependencies

## Response Format

```json
{
  "status": "healthy",
  "service": "Spec3 Chatbot API"
}
```

## Deployment

This function is deployed via AWS CDK as part of the Spec3ChatbotCdkStack. 