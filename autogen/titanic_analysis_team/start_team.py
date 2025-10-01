#!/usr/bin/env python3
"""
Simple launcher for the Titanic Analysis Team
The team automatically understands what to do based on your input.
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    """Main launcher function"""
    print("🚢 Titanic Analysis Team - Intelligent Launcher")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        print("Please set your OpenAI API key in the .env file")
        return
    
    print("🤖 The team will automatically understand what to do based on your input!")
    print("No need to choose options - just ask your question!")
    print("=" * 60)
    
    try:
        from enhanced_chat import enhanced_chat
        asyncio.run(enhanced_chat())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
