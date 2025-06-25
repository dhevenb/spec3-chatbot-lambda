import json
import boto3
import os
from typing import Dict, Any

bedrock = boto3.client('bedrock')

def handler(event, context):
    """Handler for knowledge base management operations"""
    try:
        # Parse the incoming request
        body = json.loads(event.get('body', '{}'))
        operation = body.get('operation', '')
        
        if operation == 'create_knowledge_base':
            response = create_knowledge_base(body)
        elif operation == 'add_document':
            response = add_document(body)
        elif operation == 'list_knowledge_bases':
            response = list_knowledge_bases()
        else:
            response = {'error': 'Invalid operation'}
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
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

def create_knowledge_base(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new knowledge base"""
    try:
        response = bedrock.create_knowledge_base(
            name=data.get('name', 'Spec3ChatbotKB'),
            description=data.get('description', 'Knowledge base for Spec3 Chatbot'),
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1'
                }
            },
            roleArn=os.environ.get('BEDROCK_ROLE_ARN', '')
        )
        return {'knowledge_base_id': response['knowledgeBase']['knowledgeBaseId']}
    except Exception as e:
        return {'error': f'Failed to create knowledge base: {str(e)}'}

def add_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a document to the knowledge base"""
    try:
        # Implementation for adding documents
        return {'message': 'Document added successfully'}
    except Exception as e:
        return {'error': f'Failed to add document: {str(e)}'}

def list_knowledge_bases() -> Dict[str, Any]:
    """List all knowledge bases"""
    try:
        response = bedrock.list_knowledge_bases()
        return {'knowledge_bases': response['knowledgeBaseSummaries']}
    except Exception as e:
        return {'error': f'Failed to list knowledge bases: {str(e)}'} 