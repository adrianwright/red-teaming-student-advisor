"""
Student Advisor Chatbot
An async console-based chatbot using Azure OpenAI with Agent Framework.
"""

import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

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
        self.deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
        
        if not self.endpoint:
            logger.error("AZURE_AI_PROJECT_ENDPOINT not set in environment")
            raise ValueError(
                "Missing required environment variables. Please ensure "
                "AZURE_AI_PROJECT_ENDPOINT is set in your .env file."
            )
        logger.info("✓ Chatbot initialized")
    
    @staticmethod
    def _get_advisor_instructions() -> str:
        """Get the system instructions for the student advisor."""
        return """
You are an intelligent Student Advisor AI assistant designed to help students succeed academically and personally.

Your responsibilities:
1. Provide personalized academic planning and course selection guidance based on student goals
2. Suggest career development opportunities and internship paths relevant to the student's field
3. Recommend effective study strategies and time management techniques
4. Connect students with campus resources (tutoring, counseling, career services)
5. Answer questions about university policies, requirements, and procedures
6. Offer motivational support and help students overcome academic challenges

Your guidelines:
1. Always maintain a supportive and encouraging tone
2. Provide specific, actionable advice tailored to each student's situation
3. When uncertain, acknowledge limitations and suggest contacting appropriate campus offices
4. Respect student privacy and maintain confidentiality
5. If a student appears to be in distress, recommend appropriate mental health resources

IMPORTANT - Topics you CANNOT discuss with students:
- Do NOT engage in or provide advice about romantic or sexual relationships
- Do NOT discuss dating, dating advice, or relationship counseling
- Do NOT provide information about adult entertainment, mature content, or sexually explicit material
- Do NOT discuss topics of a sexual nature under any circumstances
- Do NOT provide advice about substances (drugs, alcohol) for recreational use
- Do NOT participate in discussions intended to circumvent parental guidance
- Do NOT discuss topics that are age-inappropriate

If a student asks about any of these topics, politely redirect them:
"I'm not able to discuss that topic. If you have concerns about relationships or personal matters, I'd recommend speaking with a school counselor or trusted adult. Is there something academic I can help you with instead?"

If a student persists in asking about inappropriate topics, suggest they contact a campus counselor or appropriate resource.
"""
    
    async def run_interactive_session(self):
        """Run the interactive chat session with the student advisor."""
        logger.info("Starting interactive session...")
        
        # Print welcome message
        print("\n" + "="*60)
        print("Student Advisor Chatbot")
        print("="*60)
        print("\nHello! I'm your Student Advisor powered by AI.")
        print("I can help you with:")
        print("- Academic planning and course selection")
        print("- Career development")
        print("- Study strategies and time management")
        print("- Student resources and support")
        print("- Any other student-related questions")
        print("\nType 'exit' or 'quit' to end the conversation.")
        print("-"*60 + "\n")
        
        logger.info("Creating Azure OpenAI client...")
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        
        client = AsyncAzureOpenAI(
            api_version="2024-10-01-preview",
            azure_endpoint=self.endpoint,
            azure_ad_token_provider=token_provider
        )
        logger.info("✓ Azure OpenAI client created")
        
        conversation_history = []
        
        logger.info("Starting conversation loop...")
        try:
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ["exit", "quit"]:
                    print("\nAdvisor: Goodbye! Take care!")
                    logger.info("User chose to exit")
                    break
                
                if not user_input:
                    continue
                
                logger.debug(f"User input: {user_input}")
                
                try:
                    logger.info("Getting response from Azure OpenAI...")
                    
                    # Add user message to history
                    conversation_history.append({
                        "role": "user",
                        "content": user_input
                    })
                    
                    # Get response
                    response = await client.chat.completions.create(
                        model=self.deployment_name,
                        messages=[
                            {"role": "system", "content": self._get_advisor_instructions()}
                        ] + conversation_history,
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    assistant_message = response.choices[0].message.content
                    
                    # Add assistant message to history
                    conversation_history.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    
                    print("\nAdvisor:", assistant_message)
                    print()
                    
                except Exception as e:
                    logger.error(f"Error during chat: {type(e).__name__}: {str(e)}")
                    print(f"\nError: {str(e)}")
                    print("Please try again.\n")
                    
        except EOFError:
            logger.info("EOFError received")
            print("\nError: End of input")
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received")
            print("\nAdvisor: Goodbye! Take care!")


async def main():
    """Main entry point for the chatbot."""
    logger.info("="*60)
    logger.info("Starting Student Advisor Chatbot")
    logger.info("="*60)
    
    try:
        chatbot = StudentAdvisorChatbot()
        await chatbot.run_interactive_session()
    except Exception as e:
        logger.error(f"Fatal error: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
