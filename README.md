# 🎓 Student Advisor Chatbot

An AI-powered student advisor chatbot built with **Azure AI Foundry** and **GPT-4.1**, featuring agent-based conversations and comprehensive security testing capabilities.

## 📋 Overview

This project demonstrates:
- ✅ Azure AI Foundry (Hub & Project) deployment using Bicep
- ✅ GPT-4.1 model deployment with Azure OpenAI
- ✅ Python console application with AI agent interactions
- ✅ Comprehensive AI red teaming with multiple approaches

## 🔐 Red Teaming Approaches

This project includes **two distinct approaches** for security testing:

### 📁 **`original_approach/`** - Manual Red Teaming
- **28 hand-crafted attack vectors** across 9 categories
- **Simple keyword-based** refusal detection
- **Fast execution** with clear, readable test cases
- **Direct control** over each test scenario
- **Perfect for**: Understanding baseline security, quick validation

### 📁 **`pyrit_approach/`** - Enterprise PyRIT Framework  
- **Microsoft's PyRIT framework** for advanced AI red teaming
- **Thousands of attack vectors** from curated datasets
- **AI-powered intelligent scoring** and multi-turn adversarial attacks
- **Enterprise-scale testing** with persistent memory and reporting
- **Perfect for**: Comprehensive security assessment, compliance, ongoing monitoring

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
├── original_approach/          # Manual red teaming approach
│   ├── red_teaming.py         # 28 hand-crafted attack vectors
│   ├── test_agent_connection.py # Connection testing
│   └── README.md              # Original approach documentation
├── pyrit_approach/            # Enterprise PyRIT framework approach
│   ├── pyrit_enhanced_testing.py # Advanced AI-powered testing
│   ├── pyrit_config.yaml     # PyRIT configuration
│   ├── requirements.txt       # PyRIT-specific dependencies
│   └── README.md              # PyRIT approach documentation
├── chatbot.py                 # Student advisor chatbot app  
├── deploy.ps1                 # Deployment script
├── requirements.txt           # Base Python dependencies
├── RED_TEAMING_PLAN.md       # Security testing strategy
├── .env.template             # Environment variables template
├── .env                      # Generated configuration (not in git)
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🔐 Security Testing

Choose your red teaming approach based on your needs:

### 🎯 Quick Security Validation (Original Approach)
```bash
cd original_approach
python red_teaming.py
```
- **28 focused attack vectors** targeting student advisor scenarios
- **Fast execution** (~2-3 minutes)
- **Clear results** with pass/fail breakdown

### 🏢 Comprehensive Security Assessment (PyRIT)
```bash  
cd pyrit_approach
pip install -r requirements.txt
python pyrit_enhanced_testing.py
```
- **Thousands of attack vectors** from Microsoft's PyRIT datasets
- **AI-powered intelligent scoring** and analysis
- **Enterprise reporting** with persistent database storage

See individual README files in each folder for detailed usage instructions.

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

## 📚 Key Technologies

- **Azure AI Foundry**: Enterprise AI platform for building and deploying agents
- **Azure OpenAI**: GPT-4.1 language model  
- **Azure AI Agents**: Multi-turn conversation orchestration with versioning
- **Microsoft Agent Framework (MAF)**: Modern agent development framework
- **PyRIT**: Microsoft's AI red teaming and security assessment framework
- **Infrastructure as Code**: Bicep templates for repeatable deployments

## 🔬 Testing Results

### Original Approach Results
- ✅ **100% Pass Rate** on focused security tests (7/7 tests)
- ✅ **Proper Refusal Handling** for inappropriate requests
- ✅ **Appropriate Response** to legitimate academic questions

### Agent Performance
- **Prohibited Requests**: "I'm not able to discuss that topic. If you have concerns about personal matters, I'd recommend speaking with a school counselor."
- **Academic Questions**: Detailed, helpful responses with structured guidance

## 🧹 Cleanup

To delete all Azure resources:

```powershell
az group delete --name rg-studentadvisor-dev --yes --no-wait
```

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
