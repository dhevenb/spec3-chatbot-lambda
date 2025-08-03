# Spec3 Racing Chatbot

A comprehensive AI-powered chatbot designed specifically for the Spec3 racing community. This intelligent assistant provides real-time access to racing rules, regulations, parts information, and community knowledge through advanced AI capabilities and seamless integration with multiple data sources.

## 🏁 What is Spec3 Racing?

Spec3 is a grassroots racing series that provides an affordable entry point into competitive motorsports. The series uses standardized rules and regulations to ensure fair competition while keeping costs manageable for participants.

## 🤖 Chatbot Overview & Capabilities

The Spec3 Racing Chatbot is an intelligent AI assistant that serves as a comprehensive knowledge resource for the Spec3 racing community. Built with cutting-edge AI technology, it provides instant access to critical information that racers, teams, and enthusiasts need.

### Core Capabilities

#### 📚 **Knowledge Base Integration (RAG - Retrieval Augmented Generation)**
- **AWS Bedrock Knowledge Base**: The chatbot is connected to a comprehensive knowledge base containing the complete Spec3 rulebook, regulations, and technical specifications
- **Vector Search**: Advanced semantic search capabilities that understand context and intent, not just keywords
- **Real-time Retrieval**: Instantly retrieves relevant information from thousands of documents and rules
- **Source Attribution**: Every response includes references to the specific rules, regulations, or documents used

#### 🔄 **Multi-Source Data Integration**
- **Static Knowledge**: Access to official Spec3 rulebooks, regulations, and technical documentation
- **Dynamic Data**: Real-time access to parts catalogs, pricing information, and event schedules via MCP (Model Context Protocol) server
- **Hybrid Queries**: Intelligent routing that combines static rules with current dynamic data for comprehensive answers

#### 🧠 **Intelligent Query Classification**
The chatbot automatically classifies user queries into different categories:
- **Rules Queries**: Questions about regulations, technical specifications, and rulebook content
- **Dynamic Data Queries**: Requests for current parts, pricing, schedules, and event information
- **Hybrid Queries**: Complex questions that require both rule knowledge and current data
- **General Queries**: General Spec3 racing knowledge and community information

#### 💬 **Advanced Conversation Features**
- **Session Management**: Maintains context across conversation threads
- **Natural Language Processing**: Understands racing terminology and technical jargon
- **Contextual Responses**: Provides answers that consider the full context of the conversation
- **Multi-turn Conversations**: Handles complex, multi-part questions and follow-ups

### What the Chatbot Can Help With

#### 🏆 **Racing Rules & Regulations**
- Technical specifications and requirements
- Safety regulations and compliance
- Competition rules and procedures
- Penalty systems and enforcement
- Classifications and eligibility

#### 🔧 **Technical Support**
- Parts compatibility and specifications
- Setup recommendations and tuning advice
- Maintenance schedules and procedures
- Troubleshooting common issues
- Performance optimization tips

#### 📅 **Event & Schedule Information**
- Race schedules and locations
- Registration deadlines and procedures
- Event-specific rules and requirements
- Weather updates and contingency plans
- Practice session information

#### 💰 **Cost & Parts Management**
- Current parts pricing and availability
- Budget planning and cost estimation
- Alternative parts and cost-saving options
- Vendor information and recommendations
- Inventory tracking and management

#### 👥 **Community Support**
- New racer orientation and guidance
- Team formation and collaboration
- Mentorship opportunities
- Community events and gatherings
- Best practices and tips from experienced racers

## 🏗️ Architecture & Technology Stack

### Backend Infrastructure
- **FastAPI**: High-performance Python web framework for the main application
- **AWS Lambda**: Serverless functions for scalable, event-driven processing
- **AWS Bedrock**: Advanced AI/ML platform for knowledge base and model inference
- **AWS CDK**: Infrastructure as Code for automated deployment and management

### AI & Machine Learning
- **Claude 3 Sonnet**: Primary language model for natural conversation
- **Amazon Titan Embed**: Vector embeddings for semantic search
- **Knowledge Base RAG**: Retrieval Augmented Generation for accurate, sourced responses
- **Query Classification**: Intelligent routing to appropriate data sources

### Data Sources
- **AWS Bedrock Knowledge Base**: Vectorized rulebook and documentation
- **MCP Server**: Model Context Protocol for dynamic Google Sheets data
- **Real-time APIs**: Live data for parts, pricing, and schedules

### Deployment & Scalability
- **Serverless Architecture**: Automatic scaling based on demand
- **CDN Integration**: Global content delivery for fast response times
- **Health Monitoring**: Comprehensive monitoring and alerting
- **CORS Support**: Cross-origin resource sharing for web integration

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- AWS CLI configured with appropriate permissions
- Node.js (for CDK deployment)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/spec3-chatbot.git
   cd spec3-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export AWS_REGION=us-east-1
   export BEDROCK_KB_ID=your-knowledge-base-id
   export MCP_SERVER_URL=http://localhost:8000
   ```

4. **Run the development server**
   ```bash
   python main.py
   ```

5. **Access the web interface**
   - Open your browser to `http://localhost:8000`
   - Start chatting with the Spec3 assistant!

### AWS Deployment

The chatbot is designed to be deployed using AWS CDK for production use:

1. **Navigate to the CDK project**
   ```bash
   cd ../Spec3ChatbotCDK
   ```

2. **Install CDK dependencies**
   ```bash
   npm install
   ```

3. **Deploy the infrastructure**
   ```bash
   npm run deploy
   ```

4. **Configure the knowledge base**
   - Upload Spec3 rulebook and documentation
   - Configure vector embeddings
   - Set up data sources

## 📁 Project Structure

```
spec3-chatbot/
├── main.py                 # FastAPI application with web interface
├── requirements.txt        # Python dependencies
├── static/                 # Static web assets
├── lambda-functions/       # AWS Lambda functions
│   ├── chatbot-lambda/     # Main chatbot processing
│   ├── knowledge-base-lambda/  # Knowledge base management
│   ├── health-check-lambda/    # Health monitoring
│   └── facebook-group-webscraper/  # Community data collection
└── venv/                   # Python virtual environment
```

## 🔧 Configuration

### Environment Variables
- `AWS_REGION`: AWS region for services (default: us-east-1)
- `BEDROCK_KB_ID`: AWS Bedrock Knowledge Base ID
- `MCP_SERVER_URL`: Model Context Protocol server URL
- `MODEL_ARN`: AWS Bedrock model ARN for inference

### Knowledge Base Setup
1. Create a Bedrock Knowledge Base with Spec3 documentation
2. Configure vector embeddings using Amazon Titan
3. Upload rulebooks, regulations, and technical documentation
4. Set up retrieval configuration for optimal results

## 🤝 Contributing

We welcome contributions from the Spec3 racing community! Whether you're a racer, engineer, or enthusiast, your input helps make this chatbot more valuable for everyone.

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution
- **Knowledge Base Content**: Help expand the rulebook and documentation coverage
- **Query Classification**: Improve the intelligence of query routing
- **UI/UX**: Enhance the web interface and user experience
- **Integration**: Add new data sources and APIs
- **Testing**: Improve test coverage and reliability

## 📞 Support & Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Join community discussions about improvements
- **Documentation**: Check the wiki for detailed guides
- **Email**: Contact the development team for direct support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Spec3 Racing Community**: For the inspiration and domain expertise
- **AWS Bedrock Team**: For the powerful AI/ML platform
- **Open Source Contributors**: For the amazing tools and libraries
- **Racing Enthusiasts**: For testing and feedback

---

**Built with ❤️ for the Spec3 racing community**

*Racing is not just a sport, it's a way of life. This chatbot is here to help make that life a little easier.* 