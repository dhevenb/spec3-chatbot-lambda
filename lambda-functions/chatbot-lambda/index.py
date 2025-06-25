import json
import boto3
import os
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bedrock_runtime = boto3.client('bedrock-runtime')
bedrock_agent = boto3.client('bedrock-agent-runtime')

def handler(event, context):
    """Main handler for chatbot requests"""
    logger.info(f"Received event: {event}")
    try:
        # Parse the incoming request
        body = json.loads(event.get('body', '{}'))
        user_message = body.get('message', '')
        session_id = body.get('session_id', 'default')
        
        # If message is not in body, try to get it from the event directly
        if not user_message and 'messages' in event:
            user_message = event.get('messages', '')
        
        logger.info(f"Extracted user_message: '{user_message}'")
        
        # Process the message through Bedrock
        response = process_message(user_message, session_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'response': response,
                'session_id': session_id
            })
        }
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }

def process_message(message: str, session_id: str) -> str:
    """Process user message through Bedrock knowledge base"""
    try:
        model_arn = os.environ.get('MODEL_ARN', '')
        knowledge_base_id = os.environ.get('KNOWLEDGE_BASE_ID', '')
        
        logger.info(f"Processing message with model_arn: {model_arn}")
        logger.info(f"Using knowledge_base_id: {knowledge_base_id}")
        
        # Extract model ID from ARN if it's a full ARN
        if model_arn.startswith('arn:aws:bedrock:'):
            # For inference profiles, we need to use the model ID part
            if 'inference-profile' in model_arn:
                model_id = 'us.amazon.nova-premier-v1:0'
            else:
                # Extract model ID from standard ARN
                model_id = model_arn.split('/')[-1]
        else:
            model_id = model_arn
        
        logger.info(f"Extracted model_id: {model_id}")
        
        # Check if knowledge base ID is provided
        if not knowledge_base_id or knowledge_base_id == '':
            logger.warning("No knowledge base ID provided, falling back to direct model invocation")
            return fallback_response(message)
        
        # Use Bedrock Retrieve and Generate for knowledge base queries
        response = bedrock_agent.retrieve_and_generate(
            input={
                'text': message
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': 5
                        }
                    },
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': 'Based on the following search results, answer the user question: $search_results$\\n\\nQuestion: {question}\\n\\nAnswer:'
                        }
                    }
                }
            }
        )
        
        logger.info("Successfully retrieved response from knowledge base")
        return response['output']['text']
    except Exception as e:
        # Fallback to direct model invocation
        logger.error(f"Error in process_message: {str(e)}")
        logger.info("Falling back to direct model invocation")
        return fallback_response(message)

def fallback_response(message: str) -> str:
    """Fallback response using direct Bedrock model invocation"""
    try:
        model_arn = os.environ.get('MODEL_ARN', '')
        logger.info(f"Fallback: Using model_arn: {model_arn}")
        
        # Extract model ID from ARN if it's a full ARN
        if model_arn.startswith('arn:aws:bedrock:'):
            # For inference profiles, we need to use the model ID part
            if 'inference-profile' in model_arn:
                model_id = 'us.amazon.nova-premier-v1:0'
            else:
                # Extract model ID from standard ARN
                model_id = model_arn.split('/')[-1]
        else:
            model_id = model_arn
        
        logger.info(f"Fallback: Using model_id: {model_id}")
        
        # Use different request format based on model
        if 'nova-premier' in model_id:
            # Nova Premier format - use messages array like Claude
            request_body = {
                'messages': [
                    {
                        'role': 'user',
                        'content': message
                    }
                ],
                'maxTokens': 1000,
                'temperature': 0.7,
                'topP': 0.9
            }
            logger.info("Fallback: Using Nova Premier request format")
        else:
            # Claude format
            request_body = {
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 1000,
                'messages': [
                    {
                        'role': 'user',
                        'content': message
                    }
                ]
            }
            logger.info("Fallback: Using Claude request format")
        
        logger.info(f"Fallback: Invoking model with request body: {json.dumps(request_body)}")
        
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        logger.info(f"Fallback: Received response: {json.dumps(response_body)}")
        
        # Parse response based on model type
        if 'nova-premier' in model_id:
            # Nova Premier response format
            if 'content' in response_body and len(response_body['content']) > 0:
                result = response_body['content'][0]['text']
            elif 'completion' in response_body:
                result = response_body['completion']
            else:
                result = str(response_body)
        else:
            result = response_body['content'][0]['text']
        
        logger.info(f"Fallback: Returning result: {result}")
        return result
            
    except Exception as e:
        logger.error(f"Fallback: Error in direct model invocation: {str(e)}")
        return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}" 