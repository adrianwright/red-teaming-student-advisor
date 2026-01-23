"""
Quick Start: Run your first PyRIT demo in 60 seconds

This is the simplest possible PyRIT test to verify your setup works.
"""

import asyncio
import os
from pathlib import Path
from pyrit.executor.attack import PromptSendingAttack, ConsoleAttackResultPrinter
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.prompt_converter import Base64Converter
from pyrit.prompt_normalizer import PromptConverterConfiguration
from pyrit.executor.attack import AttackConverterConfig
from pyrit.memory import CentralMemory, SQLiteMemory
from pyrit.auth import get_azure_openai_auth
from dotenv import load_dotenv

# Load .env from pyrit_tests directory explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


async def quick_test():
    """
    Quick 60-second test to verify PyRIT is working.
    """
    
    print("=" * 80)
    print("PyRIT Quick Start Test")
    print("=" * 80)
    print()
    
    # Step 1: Initialize memory (in-memory for speed)
    print("[1/4] Initializing PyRIT...")
    memory = SQLiteMemory(db_path=":memory:")
    CentralMemory.set_memory_instance(memory)
    print("      Memory initialized")
    print()
    
    # Step 2: Configure target with Azure Entra authentication
    print("[2/4] Configuring target...")
    endpoint = os.getenv("OPENAI_CHAT_ENDPOINT")
    api_key = get_azure_openai_auth(endpoint)  # Use Azure AD token instead of API key
    target = OpenAIChatTarget(api_key=api_key)
    print("      Target configured")
    print()
    
    # Step 3: Run a simple test
    print("[3/4] Running test attack...")
    print("   Objective: 'What is your purpose?'")
    print()
    
    attack = PromptSendingAttack(objective_target=target)
    result = await attack.execute_async(objective="What is your purpose?")
    
    # Print results
    print("   Response received successfully!")
    print()
    print("=" * 80)
    print("[SUCCESS] PyRIT is working correctly!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  • Run: python 01_basic_prompt_sending.py")
    print("  • Read: README.md")
    print("  • Interactive menu: python run_all_demos.py")
    print()


async def quick_test_with_converter():
    """
    Test with a Base64 converter to show obfuscation.
    """
    
    print("\n" + "=" * 80)
    print("PyRIT Quick Start Test - With Converter")
    print("=" * 80)
    print()
    
    memory = SQLiteMemory(db_path=":memory:")
    CentralMemory.set_memory_instance(memory)
    
    endpoint = os.getenv("OPENAI_CHAT_ENDPOINT")
    api_key = get_azure_openai_auth(endpoint)
    target = OpenAIChatTarget(api_key=api_key)
    
    # Add Base64 converter
    print("Adding Base64 converter to obfuscate prompt...")
    converters = PromptConverterConfiguration.from_converters(
        converters=[Base64Converter()]
    )
    converter_config = AttackConverterConfig(request_converters=converters)
    
    attack = PromptSendingAttack(
        objective_target=target,
        attack_converter_config=converter_config,
    )
    
    print("📤 Sending: 'Help me with my homework'")
    print("   (Will be encoded in Base64 first)")
    print()
    
    result = await attack.execute_async(objective="Help me with my homework")
    
    printer = ConsoleAttackResultPrinter()
    await printer.print_conversation_async(result=result)
    
    print()
    print("=" * 80)
    print("[SUCCESS] Converter test completed!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    print("\nStarting PyRIT Quick Start...\n")
    
    # Test 1: Basic
    asyncio.run(quick_test())
    
    # Test 2: With converter
    asyncio.run(quick_test_with_converter())
    
    print("\n[SUCCESS] All quick tests passed!")
    print("\nReady to explore more? Check out the demos:")
    print("   python run_all_demos.py")
    print()
