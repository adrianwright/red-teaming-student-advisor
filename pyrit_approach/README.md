# PyRIT Enhanced Red Teaming Approach

This folder contains the advanced PyRIT (Python Risk Identification Tool for generative AI) implementation for comprehensive security testing of the StudentAdvisor chatbot.

## Files

- **`pyrit_enhanced_testing.py`** - Main PyRIT implementation with enterprise-grade attack capabilities
- **`requirements.txt`** - PyRIT-specific dependencies  
- **`pyrit_config.yaml`** - Configuration for PyRIT testing parameters

## PyRIT Overview

**PyRIT** is Microsoft's open-source framework specifically designed for AI red teaming and security risk identification. It provides sophisticated, enterprise-grade capabilities for testing generative AI systems at scale.

## Advanced Capabilities

### 🚀 **Intelligent Attack Strategies**
- **Multi-turn Adversarial Attacks**: AI generates contextual, evolving attacks
- **Jailbreaking Techniques**: Built-in library of proven jailbreak prompts
- **Social Engineering**: Advanced conversational attacks that build rapport
- **Prompt Injection**: Automated testing for various injection vectors

### 📊 **Sophisticated Scoring & Analysis**
- **`SelfAskRefusalScorer`**: AI intelligently detects refusals (vs simple keywords)
- **`AzureContentFilterScorer`**: Automated content safety scoring
- **`TrueFalseCompositeScorer`**: Complex logic combining multiple criteria
- **`LikertScaleScorer`**: Nuanced harm assessment on scales

### 🔄 **Enterprise Scale & Automation**
- **Built-in datasets**: Thousands of proven attack vectors from PyRIT libraries
- **Parallel execution**: Handle hundreds/thousands of tests simultaneously
- **Persistent memory**: SQLite database tracking across sessions
- **Rate limiting**: Built-in throttling to prevent API overload

### 🎯 **Direct Azure AI Foundry Integration**
- **Native support** for Azure AI Foundry agents and endpoints
- **Authentication integration** with Azure CLI credentials
- **Response API targeting** for versioned agents (new agents API)

## Key Advantages Over Original Approach

| Original Approach | PyRIT Approach |
|---|---|
| 28 manual attack vectors | Thousands from curated datasets |
| Simple keyword refusal detection | AI-powered intelligent scoring |
| Limited to small test subsets | Handles massive scale with rate limiting |
| Manual analysis and reporting | Automated database storage & querying |
| Static, predefined test cases | Adaptive attacks that evolve |
| Basic pass/fail scoring | Multi-dimensional scoring with nuance |

## Installation

```bash
# Install PyRIT
pip install pyrit-dev

# Ensure Azure authentication 
az login
```

## Usage

```bash
# Run comprehensive PyRIT testing
python pyrit_enhanced_testing.py
```

## Testing Categories

### **1. Multi-turn Adversarial Attacks**
AI-powered attacks that:
- Build conversational context
- Adapt based on previous responses  
- Use sophisticated social engineering
- Test persistence across multiple turns

### **2. Large-Scale Dataset Testing**
Built-in PyRIT datasets:
- **`harmful_content`** - Comprehensive harmful request variations
- **`jailbreaks`** - Proven techniques for bypassing AI safety  
- **`social_engineering`** - Manipulation and rapport-building attacks
- **`prompt_injection`** - Code injection and system manipulation

### **3. Intelligent Scoring**
- **Refusal Detection**: AI determines if response appropriately refused
- **Content Analysis**: Automated detection of harmful content
- **Composite Scoring**: Combines multiple criteria with logical operators
- **Threshold Analysis**: Configurable sensitivity levels

## Results & Reporting

PyRIT provides:
- **SQLite Database**: Persistent storage of all test results
- **Memory Querying**: Filter results by labels, timestamps, attack types
- **Detailed Scoring**: Multiple score types with confidence levels
- **Export Capabilities**: JSON, CSV, and database exports
- **Conversation Tracking**: Complete multi-turn conversation history

## Configuration

The PyRIT approach can be customized via:
- **Attack objectives**: Define specific harmful behaviors to test
- **Scoring thresholds**: Adjust sensitivity levels
- **Dataset selection**: Choose specific attack categories
- **Rate limiting**: Configure request frequency
- **Memory labels**: Organize tests for analysis

## Expected Outcomes

PyRIT testing provides:
1. **Comprehensive coverage** of potential attack vectors
2. **Quantified risk assessment** with multiple scoring dimensions  
3. **Detailed vulnerability analysis** with specific examples
4. **Scalable testing framework** for ongoing security validation
5. **Professional reporting** suitable for compliance and governance

This enterprise-grade approach transforms red teaming from a manual, limited process into a comprehensive security assessment that matches the sophistication of real-world threats.