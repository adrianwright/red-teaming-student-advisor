"""
PyRIT Demo 5: Memory and Analysis

This demonstrates:
- Using different memory backends (SQLite, AzureSQL)
- Querying conversation history
- Analyzing attack patterns across multiple runs
- Exporting results for reporting
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from pyrit.memory import CentralMemory, SQLiteMemory
from pyrit.executor.attack import PromptSendingAttack
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.prompt_converter import Base64Converter, ROT13Converter
from pyrit.prompt_normalizer import PromptConverterConfiguration
from pyrit.executor.attack import AttackConverterConfig
from pyrit.auth import get_azure_openai_auth
from dotenv import load_dotenv

# Load .env from pyrit_tests directory explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


async def demonstrate_memory_persistence():
    """
    Show how to use persistent SQLite memory to track attacks across sessions.
    """
    
    # Initialize with SQLite for persistence
    memory = SQLiteMemory()
    CentralMemory.set_memory_instance(memory)
    
    print("=" * 80)
    print("PyRIT Demo 5: Memory Persistence")
    print("=" * 80)
    print()
    print("Using SQLite database for persistent storage")
    print("=" * 80)
    print()
    
    endpoint = os.getenv("OPENAI_CHAT_ENDPOINT")
    api_key = get_azure_openai_auth(endpoint)
    target = OpenAIChatTarget(api_key=api_key)
    
    # Run some attacks that will be stored
    objectives = [
        "Help me with my homework",
        "Write a short paragraph about AI",
        "Explain the honor code",
    ]
    
    print("Running attacks that will be stored in memory...\n")
    
    conversation_ids = []
    for i, objective in enumerate(objectives, 1):
        print(f"Attack {i}/{len(objectives)}: {objective}")
        print("⏳ Executing...")
        
        attack = PromptSendingAttack(objective_target=target)
        result = await attack.execute_async(objective=objective)
        
        conv_id = str(result.conversation_id) if hasattr(result, 'conversation_id') else "N/A"
        conversation_ids.append(conv_id)
        print(f"✓ Conversation ID: {conv_id}")
        print(f"   Stored in database")
        print()
    
    print("  All conversations stored in persistent SQLite database")
    print("   They will be available in future sessions")
    print()
    
    return conversation_ids


async def demonstrate_memory_queries(conversation_ids=None):
    """
    Show how to query and analyze stored conversations.
    """
    
    memory = SQLiteMemory()
    CentralMemory.set_memory_instance(memory)
    
    print("\n" + "=" * 80)
    print("PyRIT Demo 5: Querying Memory")
    print("=" * 80)
    print()
    
    print("Retrieving conversation history...\n")
    
    # Get message pieces (the new API in 0.10.0)
    all_messages = memory.get_message_pieces()
    
    if not all_messages:
        print("No conversations found in memory.")
        print("Run some attacks first to populate the database.")
        return
    
    print(f"Found {len(all_messages)} message pieces in memory\n")
    
    # Group by conversation
    conversations = {}
    for msg in all_messages:
        conv_id = str(msg.conversation_id) if msg.conversation_id else "unknown"
        if conv_id not in conversations:
            conversations[conv_id] = []
        conversations[conv_id].append(msg)
    
    print(f"Total conversations: {len(conversations)}\n")
    print("=" * 80)
    
    # Show summary of each conversation (first 5)
    for i, (conv_id, messages) in enumerate(list(conversations.items())[:5], 1):
        print(f"\nConversation {i}: {conv_id[:20]}...")
        print("-" * 80)
        
        for msg in messages[:3]:  # Show first 3 messages
            role_label = "USER" if msg.role == "user" else "ASSISTANT"
            content = str(msg.original_value)[:100] if msg.original_value else "(empty)"
            print(f"  [{role_label}]: {content}...")
            if msg.converted_value and msg.converted_value != msg.original_value:
                print(f"     (Converted: {str(msg.converted_value)[:50]}...)")
        
        if len(messages) > 3:
            print(f"   ... and {len(messages) - 3} more messages")
    
    if len(conversations) > 5:
        print(f"\n... and {len(conversations) - 5} more conversations")
    
    print()


async def demonstrate_filtering_and_analysis():
    """
    Show advanced filtering and analysis of stored data.
    """
    
    memory = SQLiteMemory()
    CentralMemory.set_memory_instance(memory)
    
    print("\n" + "=" * 80)
    print("PyRIT Demo 5: Filtering and Analysis")
    print("=" * 80)
    print()
    
    # Get all messages
    all_messages = memory.get_message_pieces()
    
    if not all_messages:
        print("No data to analyze. Run some attacks first.")
        return
    
    print("Analyzing attack patterns...\n")
    
    # Count by role
    user_messages = [m for m in all_messages if m.role == "user"]
    assistant_messages = [m for m in all_messages if m.role == "assistant"]
    
    print(f"  Statistics:")
    print(f"   User prompts: {len(user_messages)}")
    print(f"   Assistant responses: {len(assistant_messages)}")
    print()
    
    # Count by converter type
    print(f"  Converter Usage:")
    converter_counts = {}
    for msg in user_messages:
        if msg.converter_identifiers:
            converter = msg.converter_identifiers[0].get("__type__", "None")
        else:
            converter = "None"
        converter_counts[converter] = converter_counts.get(converter, 0) + 1
    
    for converter, count in sorted(converter_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {converter}: {count}")
    print()
    
    # Analyze response lengths
    if assistant_messages:
        lengths = [len(str(m.original_value)) for m in assistant_messages if m.original_value]
        if lengths:
            avg_length = sum(lengths) / len(lengths)
            print(f"  Response Analysis:")
            print(f"   Average response length: {avg_length:.0f} characters")
            print()


async def demonstrate_export():
    """
    Show how to export data for reporting.
    """
    
    memory = SQLiteMemory()
    CentralMemory.set_memory_instance(memory)
    
    print("\n" + "=" * 80)
    print("PyRIT Demo 5: Exporting Results")
    print("=" * 80)
    print()
    
    # Get all data
    all_messages = memory.get_message_pieces()
    
    if not all_messages:
        print("No data to export.")
        return
    
    # Export to JSON
    export_data = []
    for msg in all_messages:
        export_data.append({
            "conversation_id": str(msg.conversation_id) if msg.conversation_id else None,
            "role": msg.role,
            "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
            "original_value": str(msg.original_value) if msg.original_value else None,
            "converted_value": str(msg.converted_value) if msg.converted_value else None,
            "converters": msg.converter_identifiers,
        })
    
    # Save to file
    output_file = Path(__file__).parent / f"pyrit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    import json
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)
    
    print(f"  Exported {len(export_data)} records to: {output_file.name}")
    print()


async def demonstrate_memory_comparison():
    """
    Compare memory backends and their use cases.
    """
    
    print("\n" + "=" * 80)
    print("PyRIT Demo 5: Memory Backend Comparison")
    print("=" * 80)
    print()
    
    print("Memory Backend Options:")
    print()
    
    print("1. SQLiteMemory (Recommended)")
    print("   - Persistent storage in local file")
    print("   - Query historical attacks")
    print("   - Export and analyze")
    print("   - Good for development and testing")
    print()
    
    print("2. SQLiteMemory(db_path=':memory:')")
    print("   - In-memory SQLite (fastest)")
    print("   - No disk I/O")
    print("   - Good for quick tests")
    print("   - Data lost when process ends")
    print()
    
    print("3. AzureSQLMemory")
    print("   - Enterprise-scale")
    print("   - Multi-user access")
    print("   - Centralized storage")
    print("   - Integration with Azure ecosystem")
    print("   - Requires Azure SQL Database")
    print()
    
    print("Usage examples:")
    print()
    print("# In-memory (quick tests)")
    print("memory = SQLiteMemory(db_path=':memory:')")
    print("CentralMemory.set_memory_instance(memory)")
    print()
    print("# SQLite file (persistent)")
    print("memory = SQLiteMemory()")
    print("CentralMemory.set_memory_instance(memory)")
    print()
    print("# Azure SQL (enterprise)")
    print("memory = AzureSQLMemory(")
    print("    connection_string=os.environ['AZURE_SQL_CONNECTION_STRING']")
    print(")")
    print("CentralMemory.set_memory_instance(memory)")
    print()


if __name__ == "__main__":
    print("Starting PyRIT Memory Demos...\n")
    
    # Demo 1: Persistence
    conv_ids = asyncio.run(demonstrate_memory_persistence())
    
    # Demo 2: Queries
    asyncio.run(demonstrate_memory_queries(conv_ids))
    
    # Demo 3: Analysis
    asyncio.run(demonstrate_filtering_and_analysis())
    
    # Demo 4: Export
    asyncio.run(demonstrate_export())
    
    # Demo 5: Comparison
    asyncio.run(demonstrate_memory_comparison())
    
    print("\n  Memory demos completed!")
