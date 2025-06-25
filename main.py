# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import boto3
import json
import asyncio
from typing import Dict, Any
import os
from datetime import datetime

app = FastAPI(title="Spec3 Racing Chatbot")

# Models
class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    sources: list = []
    timestamp: str = None

# Initialize AWS Bedrock client
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

class Spec3Chatbot:
    def __init__(self):
        self.knowledge_base_id = os.getenv('BEDROCK_KB_ID')
        self.mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        
    async def process_message(self, message: str, session_id: str) -> ChatResponse:
        """Main message processing logic"""
        
        # Determine which data source(s) to query
        query_type = self._classify_query(message)
        
        if query_type == "rules":
            response = await self._query_knowledge_base(message)
        elif query_type == "parts_or_schedule":
            response = await self._query_mcp_server(message)
        elif query_type == "hybrid":
            response = await self._query_both_sources(message)
        else:
            response = await self._handle_general_query(message)
            
        return ChatResponse(
            response=response.get('answer', 'Sorry, I could not find an answer.'),
            sources=response.get('sources', []),
            timestamp=datetime.now().isoformat()
        )
    
    def _classify_query(self, message: str) -> str:
        """Simple classification logic - you can make this smarter"""
        message_lower = message.lower()
        
        # Keywords that suggest rules/knowledge base query
        rules_keywords = ['rulebook', 'regulation', 'legal', 'allowed', 'requirement', 'spec', 'rule']
        
        # Keywords that suggest dynamic data query
        dynamic_keywords = ['part', 'price', 'schedule', 'race', 'event', 'upcoming', 'cost']
        
        # Keywords that might need both
        hybrid_keywords = ['build', 'car', 'setup', 'recommend']
        
        if any(word in message_lower for word in hybrid_keywords):
            return "hybrid"
        elif any(word in message_lower for word in rules_keywords):
            return "rules"
        elif any(word in message_lower for word in dynamic_keywords):
            return "parts_or_schedule"
        else:
            return "general"
    
    async def _query_knowledge_base(self, message: str) -> Dict[str, Any]:
        """Query Bedrock Knowledge Base for rules/static content"""
        try:
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user", 
                            "content": f"Based on the Spec3 racing rulebook and documentation, please answer: {message}"
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read())
            return {
                "answer": result['content'][0]['text'],
                "sources": ["Spec3 Rulebook"]
            }
            
        except Exception as e:
            return {
                "answer": f"Error querying knowledge base: {str(e)}",
                "sources": []
            }
    
    async def _query_mcp_server(self, message: str) -> Dict[str, Any]:
        """Query MCP server for dynamic Google Sheets data"""
        # This would connect to your MCP server
        # For now, returning placeholder
        try:
            # TODO: Implement actual MCP client connection
            # This is where you'd make requests to your MCP server
            # that queries the Google Sheets
            
            return {
                "answer": f"MCP query result for: {message} (placeholder - implement MCP client)",
                "sources": ["Google Sheets via MCP"]
            }
            
        except Exception as e:
            return {
                "answer": f"Error querying MCP server: {str(e)}",
                "sources": []
            }
    
    async def _query_both_sources(self, message: str) -> Dict[str, Any]:
        """Query both knowledge base and MCP server, then synthesize"""
        try:
            # Get responses from both sources
            rules_task = self._query_knowledge_base(message)
            data_task = self._query_mcp_server(message)
            
            rules_response, data_response = await asyncio.gather(rules_task, data_task)
            
            # Simple synthesis - you can make this smarter with another LLM call
            combined_answer = f"""
            Based on the rules: {rules_response['answer']}
            
            Current data: {data_response['answer']}
            """
            
            return {
                "answer": combined_answer.strip(),
                "sources": rules_response['sources'] + data_response['sources']
            }
            
        except Exception as e:
            return {
                "answer": f"Error querying multiple sources: {str(e)}",
                "sources": []
            }
    
    async def _handle_general_query(self, message: str) -> Dict[str, Any]:
        """Handle general questions about Spec3 racing"""
        try:
            response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "user", 
                            "content": f"You are a helpful assistant for Spec3 racing. Answer this question: {message}"
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read())
            return {
                "answer": result['content'][0]['text'],
                "sources": ["General Spec3 Knowledge"]
            }
            
        except Exception as e:
            return {
                "answer": "I'm here to help with Spec3 racing questions! Could you be more specific?",
                "sources": []
            }

# Initialize chatbot
chatbot = Spec3Chatbot()

# API Routes
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Main chat endpoint"""
    try:
        response = await chatbot.process_message(message.message, message.session_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "spec3-chatbot"}

# Serve static files for the web interface
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Simple web interface for testing"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spec3 Racing Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
            .message { margin-bottom: 10px; }
            .user { text-align: right; color: blue; }
            .bot { text-align: left; color: green; }
            .input-container { display: flex; }
            #messageInput { flex: 1; padding: 10px; }
            #sendButton { padding: 10px 20px; }
        </style>
    </head>
    <body>
        <h1>Spec3 Racing Chatbot</h1>
        <div id="chatContainer" class="chat-container"></div>
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Ask about Spec3 racing..." />
            <button id="sendButton" onclick="sendMessage()">Send</button>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                // Add user message to chat
                addMessage('You: ' + message, 'user');
                input.value = '';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    addMessage('Bot: ' + data.response, 'bot');
                    
                    if (data.sources && data.sources.length > 0) {
                        addMessage('Sources: ' + data.sources.join(', '), 'bot');
                    }
                } catch (error) {
                    addMessage('Error: Could not get response', 'bot');
                }
            }
            
            function addMessage(text, className) {
                const container = document.getElementById('chatContainer');
                const div = document.createElement('div');
                div.className = 'message ' + className;
                div.textContent = text;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            }
            
            // Allow Enter key to send message
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)