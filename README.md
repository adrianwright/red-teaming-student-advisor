# 🎓 Student Advisor Chatbot

An AI-powered student advisor chatbot built with **Azure AI Foundry** and **GPT-4.1**, featuring agent-based conversations and evaluation capabilities.

## 📋 Overview

This project demonstrates:
- ✅ Azure AI Foundry (Hub & Project) deployment using Bicep
- ✅ GPT-4.1 model deployment with Azure OpenAI
- ✅ Python console application with AI agent interactions
- 🔜 AI evaluation and red teaming (coming next)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          Azure AI Foundry (Hub)                 │
│  ┌───────────────────────────────────────────┐  │
│  │     Student Advisor Project               │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │   AI Agent with GPT-4.1             │  │  │
│  │  │   - Instructions & Behavior         │  │  │
│  │  │   - Conversation Threading          │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  Connected Resources:                            │
│  - Azure OpenAI (GPT-4.1)                       │
│  - Storage Account                               │
│  - Key Vault                                     │
│  - Application Insights                          │
└─────────────────────────────────────────────────┘
           ▲
           │
    ┌──────┴──────┐
    │   Python    │
    │  Console    │
    │   Chatbot   │
    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Azure Subscription** with permissions to create resources
- **Azure CLI** installed and authenticated (`az login`)
- **Python 3.8+** installed
- **PowerShell** (for deployment script)

### Step 1: Deploy Infrastructure

Deploy the Azure AI Foundry infrastructure using the Bicep template:

```powershell
# Run from the project root directory
.\deploy.ps1
```

This will:
1. Create a resource group
2. Deploy Azure AI Hub and Project
3. Deploy Azure OpenAI with GPT-4.1 model
4. Set up supporting resources (Storage, Key Vault, App Insights)
5. Generate a `.env` file with your configuration

**Deployment takes approximately 5-10 minutes.**

### Step 2: Install Python Dependencies

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### Step 3: Run the Chatbot

```powershell
python chatbot.py
```

## 💬 Using the Chatbot

Once running, you can ask the student advisor questions like:

- "What courses should I take this semester for a Computer Science major?"
- "How do I plan for graduation next year?"
- "What study strategies work best for exam preparation?"
- "Can you help me understand the registration process?"
- "What internship opportunities should I consider?"

Type `quit`, `exit`, or `bye` to end the conversation.

## 📁 Project Structure

```
red-teaming/
├── infrastructure/
│   ├── main.bicep              # Main Bicep template
│   └── parameters.json         # Deployment parameters
├── chatbot.py                  # Student advisor chatbot app
├── deploy.ps1                  # Deployment script
├── requirements.txt            # Python dependencies
├── .env.template              # Environment variables template
├── .env                       # Generated configuration (not in git)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## ⚙️ Configuration

The deployment automatically generates a `.env` file with these values:

```env
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP_NAME=<your-resource-group>
AZURE_PROJECT_NAME=<your-ai-project-name>
AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
AZURE_OPENAI_DEPLOYMENT=gpt-41
AZURE_LOCATION=<azure-region>
```

## 🔧 Customization

### Modify Agent Behavior

Edit the `agent_instructions` in [chatbot.py](chatbot.py) to customize:
- Agent personality and tone
- Specific knowledge domains
- Response guidelines
- Conversation flow

### Change Model Parameters

In [chatbot.py](chatbot.py), adjust:
```python
self.client.agents.create(
    model=self.model_deployment,
    temperature=0.7,  # Creativity (0.0-1.0)
    top_p=0.95        # Diversity (0.0-1.0)
)
```

### Deploy to Different Region

Edit [infrastructure/parameters.json](infrastructure/parameters.json):
```json
{
  "location": {
    "value": "westus"  // Change to your preferred region
  }
}
```

## 🧪 Next Steps: Evaluation & Red Teaming

After testing your chatbot, you can add:

1. **Quality Evaluation**: Measure response relevance, groundedness, and coherence
2. **Safety Evaluation**: Test for harmful content, bias, and fairness
3. **Red Teaming**: Adversarial testing for security vulnerabilities

These features will be added in the next phase using Azure AI Evaluation SDK.

## 🧹 Cleanup

To delete all Azure resources:

```powershell
az group delete --name rg-studentadvisor-dev --yes --no-wait
```

## 📚 Key Technologies

- **Azure AI Foundry**: Enterprise AI platform for building and deploying agents
- **Azure OpenAI**: GPT-4.1 language model
- **Azure AI Agents**: Multi-turn conversation orchestration
- **Infrastructure as Code**: Bicep templates for repeatable deployments

## 🐛 Troubleshooting

### Authentication Issues
```powershell
# Re-authenticate with Azure
az login
az account show
```

### Missing Environment Variables
Ensure `.env` file exists with all required values. Re-run `deploy.ps1` if needed.

### Model Deployment Errors
GPT-4.1 may not be available in all regions. Check [Azure OpenAI model availability](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) and update the location parameter.

### Python Package Issues
```powershell
# Upgrade pip and reinstall
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📖 Learn More

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Building AI Agents](https://learn.microsoft.com/azure/ai-studio/how-to/develop/agents)
- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)

## 📄 License

This project is provided as-is for educational purposes.

---

**Ready to add evaluations?** Let me know and we'll implement red teaming and safety evaluation features next!
