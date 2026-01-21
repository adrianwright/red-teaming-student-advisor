"""
Custom PyRIT Target for Azure AI Foundry Agents

This custom target allows PyRIT to interface with Azure AI Foundry agents
using the proper agents API (not the Assistants API).
"""

import asyncio
import json
import os
import time
from typing import List, Optional
import httpx
from azure.identity import DefaultAzureCredential
from pyrit.models import ChatMessage, MessagePiece, Message
from pyrit.prompt_target import PromptChatTarget


class AzureFoundryAgentTarget(PromptChatTarget):
    """
    Custom PyRIT target for Azure AI Foundry agents.
    
    Uses the proper Azure AI Foundry agents API (not OpenAI Assistants API).
    """
    
    def __init__(
        self,
        agent_name: str = "StudentAdvisor",
        **kwargs
    ):
        """
        Initialize the Azure Foundry Agent Target.
        
        Args:
            agent_name: Name of the Azure AI Foundry agent to interact with
            **kwargs: Additional parameters passed to PromptChatTarget
        """
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self._provider = None
        self._agent = None
        
    async def _get_agent_provider(self):
        """Get Azure AI Foundry agent provider."""
        if not self._provider:
            from agent_framework.azure import AzureAIProjectAgentProvider
            from azure.identity.aio import AzureCliCredential
            
            credential = AzureCliCredential()
            self._provider = AzureAIProjectAgentProvider(credential=credential)
            
        return self._provider
    
    async def _get_agent(self):
        """Get the Azure AI Foundry agent."""
        if not self._agent:
            provider = await self._get_agent_provider()
            self._agent = await provider.get_agent(name=self.agent_name)
            print(f"✅ Connected to agent: {self._agent.id}")
            
        return self._agent
        
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup resources."""
        if self._provider:
            await self._provider.__aexit__(exc_type, exc_val, exc_tb)
            self._provider = None
        self._agent = None
    
    # Required abstract method implementations for PromptChatTarget
    
    def _validate_request(self, *, message: Message) -> None:
        """Validate the message request (required by PromptChatTarget)."""
        if not message.message_pieces:
            raise ValueError("Message must have content pieces")
        
        # Check that we have at least one text piece
        text_pieces = [piece for piece in message.message_pieces if piece.original_value_data_type == "text"]
        if not text_pieces:
            raise ValueError("Message must contain at least one text piece")
    
    def is_json_response_supported(self) -> bool:
        """Whether JSON responses are supported (required by PromptChatTarget)."""
        return False  # Our agent returns plain text responses
    
    async def send_prompt_async(self, *, message: Message) -> List[Message]:
        """
        Send prompt to Azure Foundry Agent (required by PromptChatTarget).
        
        This is the main entry point PyRIT uses to send prompts.
        """
        try:
            # Extract text content from message pieces
            text_content = ""
            for piece in message.message_pieces:
                if piece.original_value_data_type == "text":
                    text_content += str(piece.converted_value or piece.original_value) + "\n"
            
            text_content = text_content.strip()
            if not text_content:
                raise ValueError("No text content in message")
            
            print(f"🤖 Sending to Azure Foundry Agent: {text_content[:100]}...")
            
            # Get the agent and run the prompt
            agent = await self._get_agent()
            response = await agent.run(text_content)
            response_text = str(response)
            
            print(f"📤 Received response: {response_text[:100]}...")
            
            # Create response Message with MessagePiece
            response_piece = MessagePiece(
                role="assistant",
                original_value=response_text,
                converted_value=response_text,
                original_value_data_type="text"
            )
            
            response_message = Message(
                message_pieces=[response_piece]
            )
            
            return [response_message]
            
        except Exception as e:
            error_msg = f"Azure Foundry Agent error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)


# Example usage function
async def test_azure_foundry_target():
    """Test function to verify the custom target works."""
    
    print(f"Testing Azure Foundry Agent: StudentAdvisor")
    
    # Create the custom target
    target = AzureFoundryAgentTarget(agent_name="StudentAdvisor")
    
    # Create test message with MessagePiece
    test_piece = MessagePiece(
        role="user",
        original_value="Hello! Can you help me with computer science course selection?",
        converted_value="Hello! Can you help me with computer science course selection?",
        original_value_data_type="text"
    )
    
    test_message = Message(message_pieces=[test_piece])
    
    try:
        async with target:
            responses = await target.send_prompt_async(message=test_message)
            
            if responses and len(responses) > 0:
                response_text = responses[0].message_pieces[0].converted_value
                print(f"✅ SUCCESS! Agent responded:")
                print(f"📝 Response: {response_text[:200]}...")
                return True
            else:
                print("❌ No response received")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Load environment variables (not needed for agent framework approach)
    from dotenv import load_dotenv
    import sys
    import pathlib
    from pyrit.memory import CentralMemory, SQLiteMemory
    
    # Load .env from parent directory
    env_path = pathlib.Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    # Initialize PyRIT memory system
    memory = SQLiteMemory()
    CentralMemory.set_memory_instance(memory)
    print("✅ PyRIT memory initialized")
    
    # Run test
    asyncio.run(test_azure_foundry_target())