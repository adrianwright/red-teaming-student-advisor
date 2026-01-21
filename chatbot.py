"""
Student Advisor Chatbot
A console-based chatbot using Azure OpenAI for educational guidance.
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from azure.identity import AzureCliCredential, get_bearer_token_provider

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
        """Create Azure OpenAI client for the student advisor."""
        logger.info("Connecting to Azure OpenAI...")
        
        # Use AzureCliCredential for authentication
        credential = AzureCliCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        
        client = AsyncAzureOpenAI(
            api_version="2024-10-21",
            azure_endpoint=self.endpoint.rstrip('/'),
            azure_ad_token_provider=token_provider
        )
        
        logger.info("✓ Azure OpenAI Client configured")
        return client
    
    async def run_interactive_session(self):
        """Run the interactive chat session with the student advisor."""
        logger.info("Starting interactive session...")
        
        # Print welcome message
        print("\n" + "="*60)
        print("Student Advisor Chatbot")
        print("="*60)
        print("\nHello! I'm your Student Advisor powered by Azure AI.")
        print("I can help you with:")
        print("- Academic planning and course selection")
        print("- Career development")
        print("- Study strategies and time management")
        print("- Student resources and support")
        print("- Any other student-related questions")
        print("\nType 'exit' or 'quit' to end the conversation.")
        print("-"*60 + "\n")
        
        client = await self.create_or_get_client()
        
        try:
            conversation_history = [
                {"role": "system", "content": self._get_advisor_instructions()}
            ]
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() in ['exit', 'quit']:
                        logger.info("User chose to exit")
                        print("Advisor: Goodbye! Take care!")
                        break
                    
                    conversation_history.append({"role": "user", "content": user_input})
                    
                    logger.info("Getting response from Azure OpenAI...")
                    response = await client.chat.completions.create(
                        model=self.deployment,
                        messages=conversation_history,
                        max_tokens=1000,
                        temperature=0.7
                    )
                    
                    assistant_message = response.choices[0].message.content
                    conversation_history.append({"role": "assistant", "content": assistant_message})
                    
                    print(f"Advisor: {assistant_message}\n")
                    
                except KeyboardInterrupt:
                    logger.info("User interrupted conversation")
                    print("\n\nAdvisor: Goodbye! Take care!")
                    break
                except Exception as e:
                    logger.error(f"Error during response: {e}")
                    print(f"Error: {str(e)}")
                    print("Please try again.\n")
        finally:
            logger.info("Closing connection...")


async def main():
    """Main entry point for the chatbot."""
    logger.info("="*60)
    logger.info("Starting Student Advisor Chatbot")
    logger.info("="*60)
    
    try:
        chatbot = StudentAdvisorChatbot()
        await chatbot.run_interactive_session()
    except Exception as e:
        logger.error(f"Fatal error: {type(e).__name__}")
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
