"""
Student Advisor Chatbot
A console-based chatbot using Azure AI Foundry Agent Framework.
Creates a persistent agent visible in the Foundry UI.
Application Insights connected via Azure infrastructure.
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureAIProjectAgentProvider

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class StudentAdvisorChatbot:
    """Student advisor chatbot using Azure OpenAI."""
    
    def __init__(self):
        """Initialize the chatbot with Azure OpenAI configuration."""
        logger.info("Initializing StudentAdvisorChatbot...")
        
        self.endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        if not self.endpoint:
            raise ValueError("AZURE_AI_PROJECT_ENDPOINT not set in environment")
        
        self.deployment = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o")
        logger.info("✓ Chatbot initialized")
        
    @staticmethod
    def _get_advisor_instructions() -> str:
        """Get the system instructions for the student advisor."""
        return """You are an intelligent Student Advisor AI assistant designed to help students succeed academically and personally.

Your responsibilities:
1. Provide personalized academic planning and course selection guidance based on student goals
2. Suggest career development opportunities and internship paths relevant to the student's field
3. Recommend effective study strategies and time management techniques
4. Connect students with campus resources (tutoring, counseling, career services)
5. Answer questions about university policies, requirements, and procedures
6. Offer motivational support and help students overcome academic challenges

IMPORTANT - Topics you CANNOT discuss:
- Romantic or sexual relationships
- Dating or relationship counseling
- Adult entertainment or sexually explicit material
- Substance use for recreational purposes
- Topics intended to circumvent parental guidance
- Age-inappropriate discussions

If asked about prohibited topics, politely redirect: "I'm not able to discuss that topic. If you have concerns about personal matters, I'd recommend speaking with a school counselor. Is there something academic I can help you with instead?"
"""
    
    async def create_or_get_client(self):
        """Create Azure AI Project agent provider."""
        logger.info("Connecting to Azure AI Foundry...")
        
        # Create credential and provider using agent framework (new agents API)
        credential = AzureCliCredential()
        provider = AzureAIProjectAgentProvider(credential=credential)
        logger.info("✓ Azure AI Project Agent Provider configured")
        return provider, credential
    
    async def run_interactive_session(self):
        """Run the interactive chat session with the student advisor."""
        logger.info("Starting interactive session...")
        
        # Print welcome message
        print("\n" + "="*60)
        print("Student Advisor Chatbot")
        print("="*60)
        print("\nHello! I'm your Student Advisor powered by Azure AI Foundry.")
        print("I can help you with:")
        print("- Academic planning and course selection")
        print("- Career development")
        print("- Study strategies and time management")
        print("- Student resources and support")
        print("- Any other student-related questions")
        print("\nType 'exit' or 'quit' to end the conversation.")
        print("Note: This agent uses the NEW agents API with versioning")
        print("-"*60 + "\n")
        
        # Use new agents pattern with AzureAIProjectAgentProvider
        async with (
            AzureCliCredential() as credential,
            AzureAIProjectAgentProvider(credential=credential) as provider,
        ):
            # Create the versioned agent in Foundry using new agents API
            logger.info("Creating StudentAdvisor agent using NEW agents API...")
            agent = await provider.create_agent(
                name="StudentAdvisor2",
                instructions=self._get_advisor_instructions()
            )
            logger.info(f"✓ New agent created with ID: {agent.id}")
            logger.info("  This uses the modern versioned agents API")
            logger.info("  View in Azure AI Foundry UI: https://ai.azure.com")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['exit', 'quit']:
                        logger.info("User chose to exit")
                        print("Advisor: Goodbye! Take care!")
                        break
                    
                    logger.info("Getting response from Foundry agent...")
                    # Run agent with the user message  
                    result = await agent.run(user_input)
                    
                    print(f"Advisor: {result}\n")
                    
                except KeyboardInterrupt:
                    logger.info("User interrupted conversation")
                    print("\n\nAdvisor: Goodbye! Take care!")
                    break
                except Exception as e:
                    logger.error(f"Error during response: {type(e).__name__}: {str(e)}")
                    print(f"Error: {str(e)}")
                    print("Please try again.\n")


async def main():
    """Main entry point for the chatbot."""
    logger.info("="*60)
    logger.info("Starting Student Advisor Chatbot (New Agents API)")
    logger.info("="*60)
    
    try:
        chatbot = StudentAdvisorChatbot()
        await chatbot.run_interactive_session()
    except Exception as e:
        logger.error(f"Fatal error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
